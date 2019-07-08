#
# Credit to http://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
#
# Slice data structure:
#{ 
#  'id' : int,
#  'name' : string,
#  'polygon' : [
#                ( lat:float, lng:float )
#			  ]
#}
# !! Polygons should remain array of tuples (json array)
#    for api compatibility (GMaps, shapely)
#
from flask import Flask, jsonify, abort, request, make_response, url_for
from flask.ext.cors import CORS
from lap_slicer import splitByID, deleteByID
from urlparse import urlparse,parse_qs
import json

app = Flask(__name__, static_url_path = "")
CORS(app)
#
# Load from our local data files
#
fp=open('slices.json','r');

try:
    slices=json.load(fp)
except ValueError:
    slices=[ { "id" : 0 }];
    write_data(slices)
fp.close()

fp=open('tracks.json','r')
try:
    tracks=json.load(fp)
except ValueError:
    tracks=[]
fp.close()

#
# Auth/Error handling
#

@app.errorhandler(400)
def get_password(username):
    if username == 'matt':
        return 'rocks'
    return None

@app.errorhandler(400)
def unauthorized():
    return make_response(jsonify( { 'error': 'Unauthorized access' } ), 403)
    # return 403 instead of 401 to prevent browsers from displaying the default auth dialog
    
@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

#
# Utility Functions
#

def make_public_slice(slice):
    new_slice = {}
    for field in slice:
        if field == 'id':
            new_slice['uri'] = url_for('get_slice', slice_id = slice['id'], _external = True)
        new_slice[field] = slice[field]
    return new_slice

def valid_request(request):
    app.logger.debug('checking input')
    if not request.json:
        app.logger.debug('not json')
        return False
    if 'name' in request.json and type(request.json['name']) != unicode:
        app.logger.debug('no name')
        return False
    if 'polygon' in request.json and type(request.json['polygon']) is not list:
        app.logger.debug('polygon not list')
        return False
    if 'polygon' in request.json and len(request.json['polygon']) < 3:
        app.logger.debug('polygon len < 3')
        return False
    if 'polygon' in request.json:
        for lat, lng in request.json.get('polygon',[]):
            if type(lat) is not float or type(lng) is not float:
                app.logger.debug('invalid lat/lng')
                return False
    if 'done' in request.json and type(request.json['done']) is not bool:
        app.logger.debug('done not bool')
        return False
    if 'youtube_url' in request.json and type(request.json['youtube_url']) is not unicode:
        app.logger.debug('youtube url not string')
        return False
	
    app.logger.debug('valid request')
    return True

def write_data(slices):
    fp=open('slices.json','w+')
    slices=json.dump(slices,fp)
    fp.close()

def getYoutubeID(request,default):
    url=request.json.get('youtube_url',default)
    app.logger.debug('Youtube url: {}'.format(url))
    if not url:
	    return url

    vid=parse_qs(urlparse(url).query)['v'][0]

    return vid
#
# API
#

@app.route('/tracks', methods = ['GET'])
def get_tracks():
    return jsonify( { 'tracks': tracks })

@app.route('/track/slices', methods = ['GET'])
def get_slices():
    return jsonify( { 'slices': map(make_public_slice, slices) } )

@app.route('/track/slices/<int:slice_id>', methods = ['GET'])
def get_slice(slice_id):
    slice = filter(lambda t: t['id'] == slice_id, slices)
    if len(slice) == 0:
        abort(404)
    return jsonify( { 'slice': make_public_slice(slice[0]) } )

@app.route('/track/slices', methods = ['POST'])
def create_slice():
    if not valid_request(request):
        abort(400)
    id=slices[-1]['id'] + 1

    slice = {
        'id': id,
        'name': request.json.get('name',''),
        'polygon': request.json.get('polygon', []),
        'youtube_id': getYoutubeID(request,''),
        'done': False
    }
    slices.append(slice)
    write_data(slices)

    # Insert our calculated timeslices
    tslices=splitByID(id)
    slice = filter(lambda t: t['id'] == id, slices)
    slice[0]['tslices']=tslices
    write_data(slices)

    return jsonify( { 'slice': make_public_slice(slice[0]) } ), 201

@app.route('/track/slices/<int:slice_id>', methods = ['PUT'])
def update_slice(slice_id):
    slice = filter(lambda t: t['id'] == slice_id, slices)
    if len(slice) == 0 or valid_request(request):
        abort(404)

    slice[0]['done'] = request.json.get('done', slice[0]['done'])
    slice[0]['name'] = request.json.get('name', slice[0]['name'])
    slice[0]['polygon'] = request.json.get('polygon', slice[0]['polygon'])
    slice[0]['youtube_id'] = getYoutubeID(request,slice[0]['youtube_id'])
    write_data(slices)
    return jsonify( { 'slice': make_public_slice(slice[0]) } )
    
@app.route('/track/slices/<int:slice_id>', methods = ['DELETE'])
def delete_slice(slice_id):
    slice = filter(lambda t: t['id'] == slice_id, slices)
    if len(slice) == 0:
        abort(404)
    slices.remove(slice[0])
    deleteByID(slice_id)
    write_data(slices)
    return jsonify( { 'result': True } )
   
if __name__ == '__main__':
    app.run(debug = True)

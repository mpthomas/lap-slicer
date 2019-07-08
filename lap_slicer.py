from shapely.geometry import Polygon, Point
import json, os


def createPolygon(coordinates):
	poly=Polygon(coordinates)
	print 'Created polygon with coordinates {}'.format(list(poly.exterior.coords))
	return poly

def pointInPolygon(polygon, coordinates):
	point=Point(coordinates)
	return polygon.contains(point)

def getTimeslices(polygon,log):
	timeslices=[]
	fp=open(log,'r')
	timing=False

	for line in fp:
		found=False
		splitup=str.split(line,',')

		try:
			float(splitup[0])
		except ValueError:
			continue

		time=float(splitup[0])
		lap=float(splitup[1])
		lat=float(splitup[5])
		lng=float(splitup[6])

		if pointInPolygon(polygon, [lat,lng]):
			if not timing:
				timing=True
				start=time
			found=True

		if not found:
			if timing:
				timeslices.append([start,time])
			timing=False
			
	return timeslices

def splitVideo(id,timeslices):
	vidfiles=open('vidfiles.txt','w+')
	ctr=0

	for start, end in timeslices:
		print "Start: %s End: %s\n" % (str(start),str(end))
		cmd='ffmpeg -ss {} -i videos/testvideo.mp4 -t {} -c copy -y videos/outvid{}.mp4'.format(start,(end-start),ctr)
		os.system(cmd)
		vidfiles.write('file \'videos/outvid{}.mp4\'\n'.format(ctr))
		ctr+=1

	vidfiles.close()
	cmd='ffmpeg -f concat -i vidfiles.txt -c copy -y videos/sliced{}.mp4'.format(id)
	os.system(cmd)
	os.remove('vidfiles.txt')

def splitByID(id):
	log="testdata.csv"

	fp=open('slices.json','r');

	try:
		slices=json.load(fp)
	except ValueError:
		fp.close()
		return False

	fp.close()

	for slice in slices:
		if slice["id"] != id:
			continue
		poly=createPolygon(slice["polygon"])
		break

	tslices=getTimeslices(poly,log)

	#print '{}'.format(tslices)

	splitVideo(id,tslices)

	return tslices

def deleteByID(id):
	os.remove('videos/sliced{}.mp4'.format(id))


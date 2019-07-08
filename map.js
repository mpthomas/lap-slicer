var map;
var map_polygon;

function initMap(lat,lng) {
  map = new google.maps.Map(document.getElementById('map'), {
    center: new google.maps.LatLng(lat,lng),
    zoom: 4
  });
}

function centerMap(lat,lng,zoom=4) {
	map.setCenter(new google.maps.LatLng(lat,lng));
	map.setZoom(zoom);
}

function drawPolygon(coordinates) {
	var poly_coordinates = [];

	if(map_polygon) {
	   map_polygon.setMap(null);
    }

	for(i=0;i<coordinates.length;i++) {
		poly_coordinates[i]=new google.maps.LatLng(coordinates[i][0],coordinates[i][1]);
	}

	map_polygon = new google.maps.Polygon({
		paths: poly_coordinates,
		draggable: true,
		editable: true,
		strokeColor: '#FF0000',
		strockOpacity: 0.8,
		strokeWeight: 2,
		fillColor: '#FF0000',
		fillOpacity: 0.35
	});

	map_polygon.setMap(map);
}

var player;

function newSlice() {
var track=$("#track-list option:selected").data("track");
	centerMap(track.polygon[0][0],track.polygon[0][1],16);
	drawPolygon(track.polygon);
}

function createTracklist() {
	$.getJSON("http://localhost:5000/tracks",function(data) {
	  $.each(data['tracks'], function(i, track) {
	  	$("#track-list").append('<option id=' + track.id + '>' + track.name + '</option>');
		$("#track-list").find("#"+track.id).data("track",track);
	  });
	});

	$("#track-list").change(function() {
		var track=$("#track-list option:selected").data("track");
		centerMap(track.polygon[0][0],track.polygon[0][1],16);
		drawPolygon(track.polygon);
    });
}

function doSliceREST(method,url,data) {
   $.ajax({
     type:method,
  	 url: url,
	 contentType:"application/json; charset=utf-8",
	 data: JSON.stringify(data),
	 dataType:"json",
	 success: function() {
		 listSlices();
		}
	 });
}

function createSlice() {
	var slice={};
	slice.name=$("#track-label").val();
	slice.youtube_url=$("#youtube_url").val();
	slice.polygon=[];

	var i=0;

	for(i=0;i<map_polygon.getPath().getLength();i++) {
		var lat=map_polygon.getPath().getAt(i).lat();
		var lng=map_polygon.getPath().getAt(i).lng();
		slice.polygon.push([lat,lng]);
	}

	doSliceREST("POST","http://localhost:5000/track/slices",slice);
}

function listSlices() {
	$.getJSON("http://localhost:5000/track/slices",function(data) {
		$("#slice-list li").remove();
		$.each(data['slices'], function(i, slice) {
			$("#slice-list").append('<li id="slice-' + slice.id+'"><button id="delete">delete</button><button id="play">play</button> <a href="#">' + slice.name + '</a></li>');

			$("#slice-"+slice.id + " a").data("slice",slice);
			$("#slice-"+slice.id + " a").click(function() {
				loadSlice(slice.id);
			});

			$("#slice-"+ slice.id + " #delete").click(function() {
				deleteSlice(slice.id);
			});

			$("#slice-"+ slice.id + " #play").click(function() {
				loadSlice(slice.id);
				playVideo(slice.id);
			})
		});
	});
}

function loadSlice(id) {
	var slice=$("#slice-"+id+" a").data("slice");

	centerMap(slice.polygon[0][0],slice.polygon[0][1],16);
	drawPolygon(slice.polygon);
}

function deleteSlice(id) {
	var slice=$("#slice-"+id+ " a").data("slice");
	doSliceREST("DELETE",slice.uri,slice);
	centerMap(slice.polygon[0][0],slice.polygon[0][1],16);
	drawPolygon(slice.polygon);
}

function playVideo(id) {
	if($("iframe").length > 0) {
    	var slice=$("#slice-"+id+" a").data("slice");
		var iframe=$("#player").prop("src","http://www.youtube.com/embed/"+slice.youtube_id+"?enablejsapi=1");
		$("#player").data("slice",slice);
		//playSlice(0,slice.tslices,player);
	}else{
		$("#video-player video").remove();
		$("#video-player").append('<video id="video" width="640" height="360" autoplay><source src="videos/sliced'+id+'.mp4" type="video/mp4"></video>');
	}
}
function playSlice(index,tslices){
	if(index >= tslices.length) { 
		player.pauseVideo(); 
		return;
	}
	console.log("playSlice(): index: "+index+" Start: "+tslices[index][0]);
	//player.playVideo();
	player.seekTo(tslices[index][0],true);
	//setTimeout(playSlice(i+1,tslices,player), (tslices[i][1]-tslices[i][0])*1000);
	index++;

	setTimeout(function() {
		playSlice(index,tslices);
	},(tslices[index-1][1]-tslices[index-1][0])*1000);
}

/*
/* YouTube Stuff */
/* */

function onYouTubeIframeAPIReady() {
	player = new YT.Player('player', {
//      height: '390',
//      width: '640',
//      videoId: 'M7lc1UVf-VE',
		playerVars: {
			html5: 1
		},
		events: {
			'onReady': onPlayerReady,
			'onStateChange': onPlayerStateChange
		}
	});
}

var index=0;
function onPlayerReady(event) {
    var slice=$("#player").data("slice");
	player.playVideo();
	//playSlice(index,slice.tslices);
    //event.target.playVideo();
}

      // 5. The API calls this function when the player's state changes.
      //    The function indicates that when playing a video (state=1),
      //    the player should play for six seconds and then stop.
var done = false;
function onPlayerStateChange(event) {
    var slice=$("#player").data("slice");
    if (event.data == -1 && !done) {
        //setTimeout(stopVideo, 6000);
///		playSlice(i++,slice.tslices,event.target);
		player.pauseVideo()
		playSlice(index,slice.tslices);
   		done=true; 
   }else if(event.data == YT.PlayerState.PAUSED && done) {
//		playSlice(i++,slice.tslices.event.target);
   }
}

function stopVideo() {
    player.stopVideo();
}

function pauseVideo() {
	player.pauseVideo();
}


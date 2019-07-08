#lap-slicer

A small utility to assist in editing and analysis of in-car track video. Often a driver may want to see lap-over-lap performance through a certain turn or section of the track. Rather than trying to fast forward over and over, this tool will create a single video of a specific area of the track (selected via google maps polygons).

This can also be used if you are interested in cutting out just a single slice. For example, you have a long video and log of a flight and you just want to capture when the moving object passes through a certain area.

##Features

Generate a video file containing only the video segment when a car or device is within a specific geographical area (corner, straight, etc)

## Installing/Getting Started

####Installation Requirments
ffmpeg http://www.ffmpeg.org
apache or other web server

####Initial Configuration
1. Create a google maps developer token/key (free). Set your domain policy for the key as appropriate (localhost most likely) https://cloud.google.com/maps-platform/

2. Create a maps_token.js in the root directory
`var map_token=yourtoken`

3. Create your telementry log file in testdata.csv in the format below:
`"Time","Lap","GPS_Update","GPS_Delay","Accuracy(m)","Latitude","Longitude","Altitude (m)","Speed (MPH)","Heading","X","Y","Z" 0.000,0,1,0.000,5.0,27.4497603,-81.3487420,19,11.6,270.7,0.00,0.00,0.00`

4. Create testvideo.mp4 in videos/ subfolter. This is the complete video of your session.

	Note: Start of video must align with the start of the telemetry log. Otherwise slicing will not "sync" properly.

5. Configure your webserver to serve up your installation directory

6. In tracks.json add geocordinates for the particular track or location you are interested in. Currently Roebling Road Raceway and Sebring International Raceway are included.

#### Usage
1. Start the backend

	`python sliceapi.py`

1. Open your browser to maps.html . You should see a frame with maps installed.

2. Select the labeled track or location (these can be modified in tracks.json)

3. Adjust the polygon in the google map frame

4.  Give the selection a label and hit save. On the backend this will trigger the video edit, which is saved under the videos/ folder.

## TODO
- Add ability to play recently created video. Play button exists as placeholder, but it does nothing.
- Integrate with the youtube player. I have created a rough POC and it is possible to "control" the player.
- Clean up the UI significantly
## License
MIT

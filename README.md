# pi-timelapse
An always-on timelapse using Raspberry Pi camera and Picamera library. Creates 2-3 timelapse movies per day around 3 minutes long (depending on daylight hours). Once a movie is made it archives it on NAS and copies it to a remote webserver for viewing. Webserver code to be posted soon. Example implementation: http://elephantmountain.ca

Features dark detection so it will stop capturing when it's dark outside. 

Dependencies:
PiCamera library, Python Imaging Library (PIL),
ImageMagick,
Gstreamer

###Files

**camera.py** takes a picture every 6 seconds and saves it as a timestamped .jpg in /buffer. It is called once when the Pi is booted and keeps interating on its own.

**tl.py** is called via CRON several times during the day. It empties the /tl folder, copies the timestamped JPGs from /buffer into /tl, then renames the files to a sequence of numbers. Then it uses Gstreamer to weave the images into a movie, which only takes around 30 minutes (on a Pi 2) because Gstreamer is awesome. It then copies the movie to an archive folder on NAS and to a remove webserver for viewing.

**hourly.py** saves an hourly image to a folder on NAS for making into long-term timelapse

**minutely.py** uploads the latest captured .jpg to the webserver once every minute

**keepAlive.py** is called regularly by CRON to restart the camera.py script in case it dies


###Sample CRON:
<code>
**m h  dom mon dow   command**

0 11 * * * /usr/bin/python /home/pi/scripts/tl.py

0 17 * * * /usr/bin/python /home/pi/scripts/tl.py

0 21 * * * /usr/bin/python /home/pi/scripts/tl.py

0 * * * * /usr/bin/python /home/pi/scripts/hourly.py

* * * * * /usr/bin/python /home/pi/scripts/minutely.py

*/5 * * * * /home/pi/scripts/keepalive.sh

</code>

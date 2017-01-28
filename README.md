# pi-timelapse
An always-on timelapse webcam using a Raspberry Pi, Pi camera module and the Picamera Python library. Creates 2-3 timelapse movies per day around 3 minutes long (depending on daylight hours). Once a movie is made it archives it on NAS and copies it to a remote webserver for viewing. Webserver code to be posted soon. Example implementation: http://elephantmountain.ca

###Dependencies

- PiCamera library  https://picamera.readthedocs.io/en/release-1.12/
- Python Imaging Library (PIL) http://www.pythonware.com/products/pil/
- ImageMagick https://www.imagemagick.org/script/index.php
- Gstreamer https://gstreamer.freedesktop.org/

###Files

* **camera.py** takes a picture every 6 seconds and saves it as a timestamped .jpg in /buffer. It is called once when the Pi is booted and keeps iterating on its own. Limits the number of images in /buffer/ by deleting the oldest if there are more than n. Doesn't keep any images if they are too dark so only daylight shows in the videos. White balance is fixed since auto whitebalance makes the colors go wonky during twilight hours, during storms etc.

* **tl.py** is called via CRON several times during the day. It empties the /tl/ folder, copies the timestamped JPGs from /buffer/ into /tl/, then renames the files to a sequence of numbers. Then it uses Gstreamer to weave the images into a movie, which only takes around 30 minutes (on a Pi 2) because Gstreamer is awesome. It then copies the movie to an archive folder on NAS and to a remove webserver for viewing.

* **hourly.py** saves an hourly image to a folder on NAS for making into long-term timelapse

* **minutely.py** uploads the latest captured .jpg to the webserver once every minute

* **keepAlive.py** is called regularly by CRON to restart the camera.py script in case it dies

* **whiteBalance.py** can be used if you want to adjust the white balance settings by capturing the current auto-whitebalance setting. The camera.py must be killed first (killall python) and you'll need a temp folder for the temporary images it creates (~/scripts/temp/). Then copy the whitebalance numbers it spits out into the capture() function in camera.py (camera.awb_gains).




###CRON
<code>

0 11 * * * /usr/bin/python /home/pi/scripts/tl.py

0 17 * * * /usr/bin/python /home/pi/scripts/tl.py

0 21 * * * /usr/bin/python /home/pi/scripts/tl.py

0 * * * * /usr/bin/python /home/pi/scripts/hourly.py

* * * * * /usr/bin/python /home/pi/scripts/minutely.py

*/5 * * * * /home/pi/scripts/keepalive.sh

</code>


###Installation

- clone these files into a ~/scripts directory
- add the above to CRON
- add camera.py to your init.d so it runs on boot (https://www.raspberrypi.org/forums/viewtopic.php?f=48&t=70520)
- create the directories needed for storing images. Mine are /media/usbstik/buffer/ and /media/usbstik/tl/
- change the file path if needed in camera.py and tl.py
- comment out anything you aren't using like the archiving or sending to webserver. If you are using these you'll need to set up SSH shortcuts to those systems in order for the SCP commands in these scripts to work

Quite a bit of local storage is required because we are saving thousands of images each day, each of which can be several MB. I'm using a 32GB usb stick which mounts to /media/usbstik on boot. I'm also archiving a copy of timelapse movies (via SCP) to a directory on my NAS, which has 2TB.

# pi-timelapse
An always-on timelapse using Raspberry Pi camera and Picamera library

Dependencies:
PiCamera Python library,
ImageMagick,
Gstreamer

**camera.py** takes a picture every 5 seconds and saves it as a timestamped .jpg in /buffer. It is called once when the Pi is booted and keeps interating on its own.

**tl.py** is called via CRON several times during the day. It copies the contents of /buffer to /tl, then renames the files to a sequence of numbers instead of timestamps. Then it weaves the images into a movie using Gstreamer, which (amazingly) only takes -30 min. It then copies the movie to an archive folder on the LAN and to a remove webserver for viewing.


tl.py

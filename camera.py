import os
import glob
import time, threading
import picamera
import fnmatch
from datetime import datetime, timedelta
from fractions import Fraction
from PIL import Image

bufferSize = 3600 # 6 hours

currentFilename = ""
storagePath = "/media/usbstik/buffer"

print('Starting er up..')

def capture():
    with picamera.PiCamera() as camera:
        # camera.start_preview()
        global currentFilename
	camera.vflip = False
	camera.resolution = (1920, 1080)
        camera.awb_mode = "off" # "cloudy"
	camera.awb_gains = (Fraction(485, 256), Fraction(169, 128))
	camera.drc_strength = 'high'
	camera.exposure_mode = "auto"
	camera.contrast = 30
	camera.sharpness = 80	
	camera.iso = 200
	time.sleep(2)
        for filename in camera.capture_continuous(storagePath + 'img{timestamp:%Y-%m-%d-%H-%M-%S}.jpg'):
	    currentFilename = filename
	    bufferCount = len(fnmatch.filter(os.listdir(storagePath), '*.jpg'))
            oldest = min(glob.iglob(storagePath+'*.jpg'), key=os.path.getctime)
            print('Captured %s' % filename + ' ct: ' + `bufferCount` )
            if(bufferCount >= bufferSize):
                os.system('rm ' + oldest)
                # print('removed '+oldest)
	    filter(currentFilename)
	    time.sleep(6) # wait 6 sec

def filter(imagePath):
	img = Image.open(imagePath) 
	gsimg = img.convert(mode='L')
	hg = gsimg.histogram()
	# count should be 256 most/all of the time (an index for each shade of grey)
	count = len(hg)
	print sum(hg[:count/2])
	print sum(hg[count/2:]) 
	if( sum(hg[count/2:]) < 200 ):
  		print "the image is too dark"
		os.system('rm ' + imagePath)
	# else:
		# writeSubtitle()

def writeSubtitile(path):
	f = open(imagePath+'subtitle.txt', 'a')
        f.write('')
        f.close

capture()


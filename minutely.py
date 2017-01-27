import os
import glob
import time, threading
import picamera
import fnmatch
from datetime import datetime, timedelta

def minutely():
	newest = max(glob.iglob('/media/usbstik/buffer/*.jpg'), key=os.path.getctime)
        print(newest)
	if newest:
                newestFile = newest.split("/")[4]
                svrPath = "/home/elephant/public_html/img/"
                newFile = "latest.jpg"
                os.system('scp ' + newest + ' shit:/home/elephant/public_html/img/')
                print("ssh shit 'cd %s'; mv %s %s; chown elephant %s;' " % (svrPath, newestFile, newFile, newFile) )
                os.system("ssh shit 'cd %s; mv %s %s; chown elephant %s;' " % (svrPath, newestFile, newFile, newFile) )
		# todo: first copy existing file to 30 min ago, hour ago...

minutely()

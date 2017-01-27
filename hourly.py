import os
import glob
import time, threading
import picamera
import fnmatch
from datetime import datetime, timedelta

def hourly():
        time.sleep(60) # for when it's first run and /buffer is empty
        print('------ hourly')
        newest = max(glob.iglob('/media/usbstik/buffer/*.jpg'), key=os.path.getctime)
        if newest:
                os.system('cp ' + newest + ' /media/usbstik/archive')

hourly()

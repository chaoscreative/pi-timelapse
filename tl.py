import time
import os
import ftplib
import logging
logging.basicConfig(filename='/home/pi/scripts/tl.log',level=logging.DEBUG)

path = '/media/usbstik/';  #initialise the path with the current directory.

def checkAge():
	# get most recent file
	files = [os.path.join(path+'buffer/', x) for x in os.listdir(path+'buffer')]
	latest = max(files , key = os.path.getctime)
	fileCreation = os.path.getmtime(latest)
	# see if it is > 30 min old
	now = time.time()
	halfhour_ago = now - 30*60
	logging.info(latest)
	logging.info(fileCreation)
	logging.info(halfhour_ago)
	if fileCreation < halfhour_ago:
    		return False
	return True

def prepFiles():
	numFiles = len(os.walk( path+ 'buffer').next()[2])
	logging.info('clearing out %s files from /tl' % (numFiles) )
	os.system('rm '+path+'tl/*') # clear out
	logging.info('moving buffer to tl')
	os.system('mv '+path+'buffer/* '+path+ 'tl/') # move buffer over
	logging.info('renaming /tl contents to numbered files')
	i = 0;
	files = os.listdir(path+'tl');  
	for file in files:
		os.system('mv '+path+'tl/'+file+' '+path+'tl/'+('%04d' % i)+'.jpg'); #to rename file
		i = i + 1;
	if i == 0:
		return False
	else:
		return True 

def mkMovie():
	numFiles = len(os.walk( path+ 'tl').next()[2])
	logging.info('Making movie from %s jpgs' % (numFiles) )
	filename = 'timelapse_'+time.strftime("%Y%m%d-%H%M%S")+'.mp4'
	# os.system('gst-launch-1.0 multifilesrc location='+path+'tl/%04d.jpg index=1 caps="image/jpeg,framerate=12/1" ! jpegdec ! omxh264enc ! avimux ! filesink location='+path+'/tl/timelapse.avi')
	os.system('gst-launch-1.0 multifilesrc location='+path+'tl/%04d.jpg index=1 caps="image/jpeg,width=1920,height=1080,framerate=23/1" ! jpegdec ! x264enc bitrate=3072 ! mp4mux ! filesink location='+path+'/tl/'+filename)
	return filename

def sendMovie(filename):
	# save a copy of movie to NAS
	logging.info('sending to pi')
	os.system('scp '+path+'tl/'+filename+' pi:/media/timelapse/')

def ulFile(filename):
	# send movid to website server
	svrPath = "/home/elephant/public_html/vid/"
	newFile = "today11.mp4"
	logging.info('putFile ' + filename)
	logging.info('scp %stl/%s shit:%s;' % (path, filename, svrPath) );
	os.system('scp %stl/%s shit:%s;' % (path, filename, svrPath) )

	#  fix ownership; delete all but most recent 50 vids
	os.system("ssh shit 'cd %s; chown elephant %s; ls -tp | grep -v '/$' | tail -n +50 | xargs -I {} rm -- {} ' " % (svrPath, filename) )
	logging.info("==== done! ====")
	
logging.info("-------------------------------------------")
logging.info(time.strftime("%m/%d/%Y %H:%M:%S"))

#if checkAge():
if prepFiles():
	filename = mkMovie()
	sendMovie(filename)
	ulFile(filename)

#else:
	# TODO use Request to send call to Slack notification
	#os.system('curl -X POST --data-urlencode 'payload={"channel": "#timelapse", "username": "webhookbot", "text": "This is posted to #timelapse and comes from a bot named webhookbot.", "icon_emoji": ":ghost:"}' https://hooks.slack.com/services/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


# convert -resize 800x600 -delay 10 -loop 0 [criteria]*.jpg animation.gif

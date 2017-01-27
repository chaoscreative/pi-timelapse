import time
import picamera

with picamera.PiCamera() as camera:
    camera.resolution = (1280, 720)
    camera.framerate = 30
    # Wait for the automatic gain control to settle
    time.sleep(2)
    # Now fix the values
    camera.shutter_speed = camera.exposure_speed
    camera.exposure_mode = 'off'
    g = camera.awb_gains
    camera.awb_mode = 'off'
    camera.awb_gains = g
    # Finally, take several photos with the fixed settings
    camera.capture_sequence(['temp/image%02d.jpg' % i for i in range(10)])
    print('awb gain: ')
    print(g)

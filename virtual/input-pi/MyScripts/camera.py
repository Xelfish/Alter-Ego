#This executes the camera on the Input-PI
from picamera import PiCamera
import time
from files import *

camera = PiCamera(resolution=(1280, 1280), framerate=30)
cameraSettings = get_json_settings('MyScripts/project-settings.json')['input-pi']['camera']
#camera.iso = 800#cameraSettings["iso"]
#camera.shutter_speed = camera.exposure_speed
#camera.exposure_mode = 'off'

def take_picture(camera):
    time.sleep(cameraSettings['interval'])
    print ("Taking a picture...")
    path = get_new_file_name("MyPics/")
    camera.capture(path)

camera.start_preview()

for i in range(2):
    take_picture(camera)
    print(i)

camera.stop_preview()



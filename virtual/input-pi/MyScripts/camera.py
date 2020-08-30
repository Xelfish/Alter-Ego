#This executes the camera on the Input-PI
from picamera import PiCamera
import time
from files import *

cameraSettings = get_json_settings('MyScripts/project-settings.json')['input-pi']['camera']
camera = PiCamera(resolution=(cameraSettings['res']['x'],cameraSettings['res']['y']))
#camera.iso = cameraSettings["iso"]
#camera.shutter_speed = camera.exposure_speed
#camera.exposure_mode = 'off'

def setZoom():
    x = y = cameraSettings["zoom"] / 2
    width = height = 1.0 - x * 2
    return (x, y, width, height)

def take_picture(camera):
    path = get_new_file_name("MyPics/")
    camera.capture(path)

camera.zoom = setZoom()

camera.start_preview()

for i in range(10):
    time.sleep(cameraSettings['interval'])
    print("Taking a picture: " + str(i) + "...")
    take_picture(camera)

camera.stop_preview()



#This executes the camera on the Input-PI
from picamera import PiCamera
import time
from fractions import Fraction
from files import *

cameraSettings = get_json_settings('MyScripts/project-settings.json')[get_pi_id()]['camera']
camera = PiCamera(resolution=(cameraSettings['res']['x'],cameraSettings['res']['y']))
camera.brightness = 55

def monitorCamSettings(camera):
    print("iso: ", camera.iso)
    print(camera.exposure_speed)
    print(camera.exposure_mode)
    print(camera.digital_gain)
    print(camera.analog_gain)
    print(camera.brightness) 

def setZoom():
    x = y = cameraSettings["zoom"] / 2
    width = height = 1.0 - x * 2
    return (x, y, width, height)

def take_picture(camera):
    path = get_new_file_name("MyPics/")
    camera.capture(path)

#FIXME: check Shutterspeed and White Balance

camera.zoom = setZoom()
monitorCamSettings(camera)

camera.start_preview()

for i in range(10):
    time.sleep(cameraSettings['interval'])
    print("Taking a picture: " + str(i + 1) + "...")
    take_picture(camera)

camera.stop_preview()



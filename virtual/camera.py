#This executes the camera on the Input-PI
from picamera import PiCamera
import time
from fractions import Fraction
from files import *

def set_camera_settings(camera, settings):
    camera.exposure_mode = "off"
    camera.framerate = Fraction(int(settings["interval"]), 1)
    camera.iso = 400
    camera.shutter_speed = 2000
    camera.brightness = 55
    camera.zoom = setZoom(settings)

def monitorCamSettings(camera):
    print("iso: ", camera.iso)
    print("exposure speed: ", camera.exposure_speed)
    print("frame rate: ", camera.framerate)
    print(camera.exposure_mode)
    print(camera.digital_gain)
    print(camera.analog_gain)
    print(camera.brightness) 

def setZoom(settings):
    x = y = settings["zoom"] / 2
    width = height = 1.0 - x * 2
    return (x, y, width, height)

def take_picture(camera):
    path = get_new_file_name("MyPics/")
    camera.capture(path)

#FIXME: check Shutterspeed and White Balance

def main():
    ID = get_pi_id()
    cameraSettings = get_json_settings('MyScripts/project-settings.json')[ID]['camera']
    camera = PiCamera(resolution=(cameraSettings['res']['x'],cameraSettings['res']['y']))
    #set_camera_settings(camera, cameraSettings)
    monitorCamSettings(camera)
    for i in range(1):
        print(ID + " taking a picture: " + str(i + 1) + "...")
        take_picture(camera)
        time.sleep(cameraSettings['interval'])

if __name__ == "__main__":
    main()
    




from picamera import PiCamera
from time import sleep
import os

def make_padded_number(number):
    fileNumberString = str(number)
    return fileNumberString.zfill(4)

def get_new_file_name(dir):
    fileNumber = 0
    while (os.path.isfile(dir + "image" + make_padded_number(fileNumber) + ".jpg")):
        fileNumber += 1
    return (dir + "image" + make_padded_number(fileNumber) + ".jpg")

def take_picture(camera):
    sleep(0.3)
    print ("Taking a picture...")
    path = get_new_file_name("MyPics/")
    camera.capture(path)
    
camera = PiCamera(resolution=(1280, 720), framerate=30)
camera.iso = 800
camera.start_preview()
camera.shutter_speed = camera.exposure_speed
camera.exposure_mode = 'off'

for i in range(5):
    take_picture(camera)
    print(i)

camera.stop_preview()



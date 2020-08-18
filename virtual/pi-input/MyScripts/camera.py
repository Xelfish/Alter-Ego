from picamera import PiCamera
from time import sleep

camera = PiCamera()

camera.start_preview()
for i in range(5):
    sleep(5)
    camera.capture('MyPics/image%s.jpg' % i)
    print("Image shot!")
camera.stop_preview()
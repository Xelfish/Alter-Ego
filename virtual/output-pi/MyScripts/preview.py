from picamera import PiCamera
import time
from files import *

ID = get_pi_id()
cameraSettings = get_json_settings('MyScripts/project-settings.json')[ID]['camera']
camera = PiCamera(resolution=(cameraSettings['res']['x'],cameraSettings['res']['y']))
camera.preview()
time.sleep(20)
camera.stop()
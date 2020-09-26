#This executes a script that cleans excessive pictures on the respective PI
import os
from files import *

def clearFolder(max_amount):
    pics = os.listdir("MyPics")
    if len(pics) > max_amount:
        sorted_pics = sorted(pics, key=lambda x: os.path.getmtime(os.path.join("MyPics",x) ))
        old_pics = sorted_pics[:int(max_amount/2)]
        for pic in old_pics:
            print(os.path.join("MyPics", pic))
            os.remove(os.path.join("MyPics", pic))

def main():
    ID = get_pi_id()
    cameraSettings = get_json_settings('MyScripts/project-settings.json')[ID]['camera']
    camera = PiCamera(resolution=(cameraSettings['res']['x'],cameraSettings['res']['y']))
    set_camera_settings(camera, cameraSettings)
    clearFolder(cameraSettings["max-pics"])
    
if __name__ == "__main__":
    main()
    




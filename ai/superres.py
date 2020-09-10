import cv2
from cv2 import dnn_superres
from modules.util.files import *

video_settings = get_json_settings("project-settings.json")["video"]
SIZE = (video_settings["size"]["x"], video_settings["size"]["y"])
FORMAT = video_settings["format"]
CODEC = video_settings["codec"]
FPS = video_settings["fps"]

#TODO: Build Open-CV with Cuda Support

def upscale_video(sourcePath, destPath):
    formattedDestPath = destPath + "." + FORMAT
    cam = cv2.VideoCapture(sourcePath)
    fourcc = cv2.VideoWriter_fourcc(*CODEC)
    print("Creating video: ", destPath, "...")
    video= cv2.VideoWriter(formattedDestPath, fourcc, int(FPS), SIZE) 
    while True:
        material, frame = cam.read()
        if not material:
            break 
        print("Upscaling Frame...")
        upscaled_frame = superscale_frame(frame)
        fixed_size=cv2.resize(frame, SIZE)
        print("Frame written!")
        video.write(fixed_size) 
    cam.release() 
    video.release()
    print("Video done")
    cv2.destroyAllWindows()

def superscale_frame(image):
    super_res = dnn_superres.DnnSuperResImpl_create()
    path = get_model_path()
    super_res.readModel(path)
    super_res.setModel(superres_settings["model"], str(superres_settings["scale"])
    result = super_res.upsample(image)
    return result

def get_model_path():
    superres_settings = get_json_settings("project-settings.json")["api"]["superres"]
    name = superres_settings["model"].upper()
    scale = str(superres_settings["scale"])
    fullname = name + "_" + "x" + scale
    return "ai/models/" + fullname + ".pb"
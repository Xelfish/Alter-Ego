import cv2
from cv2 import dnn_superres
from modules.util.files import *

video_settings = get_json_settings("project-settings.json")["video"]
superres_settings = get_json_settings("project-settings.json")["api"]["superres"]
SIZE = (video_settings["size"]["x"], video_settings["size"]["y"])
FORMAT = video_settings["format"]
CODEC = video_settings["codec"]
FPS = video_settings["fps"]

#TODO: Build Open-CV with Cuda Support

def upscale_video(sourcePath, destPath):
    formattedDestPath = destPath + "." + FORMAT
    cam = cv2.VideoCapture(sourcePath)
    fourcc = cv2.VideoWriter_fourcc(*CODEC)
    print("Upscaling video: ", destPath, "...")
    superscale = get_superscaler()
    video= cv2.VideoWriter(formattedDestPath, fourcc, int(FPS), SIZE) 
    while True:
        material, frame = cam.read()
        if not material:
            break 
        upscaled_frame = superscale_frame(frame, superscale)
        fixed_size=cv2.resize(upscaled_frame, SIZE)
        video.write(fixed_size) 
    cam.release() 
    video.release()
    print("Video done")
    cv2.destroyAllWindows()
    return formattedDestPath

def get_superscaler():
    super_res = dnn_superres.DnnSuperResImpl_create()
    path = get_model_path()
    super_res.readModel(path)
    super_res.setModel(superres_settings["model"], superres_settings["scale"])
    return super_res

def superscale_frame(image, superscale):
    result = superscale.upsample(image)
    return result

def get_model_path():
    superres_settings = get_json_settings("project-settings.json")["api"]["superres"]
    name = superres_settings["model"].upper()
    scale = str(superres_settings["scale"])
    fullname = name + "_" + "x" + scale
    return "ai/models/" + fullname + ".pb"
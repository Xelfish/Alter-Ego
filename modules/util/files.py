# utility functions to handle and load files
import os
import json

def get_json_settings(path):
    fileDir = os.path.dirname(os.path.realpath('__file__'))
    filename = os.path.join(fileDir, path)
    with open(path) as settings:
        settings = json.load(settings)
    return settings

def make_padded_number(number):
    fileNumberString = str(number)
    return fileNumberString.zfill(4)   

def get_new_file_name(targetdir, basename="image", filetype="jpg"):
    fileNumber = 0
    while (os.path.isfile(targetdir + basename + make_padded_number(fileNumber) + "." + filetype)):
        fileNumber += 1
    return (targetdir + basename + make_padded_number(fileNumber) + "." + filetype)

def rename_video(oldname, newname):
    # given the oldname rename the still and the respective video with the newname
    pass

def get_os():
    return os

def get_video_name(path):
    base = os.path.basename(path)
    return os.path.splitext(base)[0]

def get_secret():
    with open("./secret.txt") as secret:
        content = secret.read()
        return content

def save_video(video):
    open(get_new_file_name('test/output/deepfake/', 'deepfake', 'mp4'), 'wb').write(video)
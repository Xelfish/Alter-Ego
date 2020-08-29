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

def get_new_file_name(targetdir, basename="image"):
    fileNumber = 0
    while (os.path.isfile(targetdir + basename + make_padded_number(fileNumber) + ".jpg")):
        fileNumber += 1
    return (targetdir + basename + make_padded_number(fileNumber) + ".jpg")

def rename_and_match_still_and_video(oldname, newname):
    # given the oldname rename the still and the respective video with the newname
    pass

def get_video_name(path):
    base = os.path.basename(path)
    return os.path.splitext(base)[0]

def get_secret():
    with open("./secret.txt") as secret:
        content = secret.read()
        return content
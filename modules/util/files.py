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

def get_new_file_name(dir):
    fileNumber = 0
    while (os.path.isfile(dir + "image" + make_padded_number(fileNumber) + ".jpg")):
        fileNumber += 1
    return (dir + "image" + make_padded_number(fileNumber) + ".jpg")


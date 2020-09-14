# utility functions to handle and load files
import os
import json

def get_json_settings(path="project-settings.json"):
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
    directory = "test/output/deepfake/"
    newpath = directory + newname + ".mp4"
    os.rename(directory + oldname, newpath)
    return newpath

def get_os():
    return os

def get_pi_id():
    with open("./id.txt") as ID:
        content = ID.read()
        return content

def get_file_name(path):
    base = os.path.basename(path)
    return os.path.splitext(base)[0]

def get_secret():
    with open("./secret.txt") as secret:
        content = secret.read()
        return content

def build_path_from_settings(path, settings, keys):
    #find dynamic maybe recursive algorithm.
    next_entry = settings[keys[0]] 
    if type(next_entry) == dict:   
        return build_path_from_settings(path + next_entry["root"], next_entry, keys[1:])
    else:
        return path + next_entry

def save_video(video):
    open(get_new_file_name('test/output/deepfake/', 'deepfake', 'mp4'), 'wb').write(video)

def find_file(directory, name):
    pass
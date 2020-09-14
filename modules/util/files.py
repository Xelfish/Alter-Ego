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

def get_os():
    return os

def get_pi_id():
    with open("./id.txt") as ID:
        content = ID.read()
        return content

def get_file_name(path):
    base = os.path.basename(path)
    return os.path.splitext(base)[0]

def get_secret(name):
    with open("secrets/" + name + ".txt") as secret:
        content = secret.read()
        return content

def build_path_from_settings(path, settings, keys):
    #find dynamic maybe recursive algorithm.
    next_entry = settings[keys[0]] 
    if type(next_entry) == dict:   
        return build_path_from_settings(path + next_entry["root"], next_entry, keys[1:])
    else:
        return path + next_entry

def get_file_format(path):
    base = os.path.basename(path)
    return os.path.splitext(base)[1]

def rename_video(oldpath, newname):
    FORMAT = get_file_format(oldpath)
    directory = os.path.dirname(oldpath)
    newpath = os.path.join(directory, newname + FORMAT) 
    os.rename(oldpath, newpath)
    return newpath

def save_video(video, path):
    newpath = get_new_file_name(path, 'deepfake', 'mp4')
    with open(newpath, 'wb') as video:
       video.write(video)
    return newpath
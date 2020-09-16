# This is the main entry-point for Alter Ego

import time
import threading

from modules.image import *
from modules.ai_operations import *
from modules.util.files import *
from modules.communication import *

# setup

settings = get_json_settings('project-settings.json')

inPi = settings["input-pi"]
outPi = settings["output-pi"]
commands =  settings["commands"]
timing = settings["timing"]

# concurrency helpers

def parallel(func):
    def parallel_func(*args, **kw):
        t = threading.Thread(None, target=func, args=args, kwargs=kw)
        t.setName(func.__name__ + " as Parallel")
        t.start()
    return parallel_func
    
def parallel_daemon(func):
    def parallel_func(*args, **kw):
        t = threading.Thread(None, target=func, args=args, kwargs=kw, daemon=True)
        t.setName(func.__name__ + " as Parallel Daemon")
        t.start()
    return parallel_func

def monitor_threads():
    print ("Number of Threads: ", threading.active_count())
    for thread in threading.enumerate():
        print(thread)

# Parallel High-Level Tasks

def run_camera_in():
    print("STARTED: Run Camera Input")
    execOnPi(inPi, commands['camera'])

def run_camera_out():
    print("STARTED: Run Camera Output")
    execOnPi(outPi, commands['camera'])
    pass

def run_ftp_listener_in():
    print("STARTED: FTP Listener Input Pics")
    ftp = connectToFtp(inPi)
    watch_directory_for_change("/home/pi/MyPics", on_new_file_in, remote=ftp)

def run_ftp_listener_out():
    ftp = connectToFtp(outPi)
    watch_directory_for_change("/home/pi/MyPics", on_new_file_out, remote=ftp)
    pass

def run_deepfake_listener():
    print("STARTED: Listen for Deepfake Input")
    watch_directory_for_change(build_path_from_settings("", settings, ["dir", "faces", "in"]), prepare_deepfake)

#FIXME: Refactor for better readability
@parallel_daemon
def watch_directory_for_change(directory, on_new_file, interval=timing["interval"], remote=None):
    path_to_watch = directory
    target = get_os()
    if remote:
        target = remote
    print("starting to watch ", path_to_watch, "...")
    before = dict([(f, None) for f in target.listdir(path_to_watch)])
    while True:
        printpath = path_to_watch
        if remote: 
            printpath = printpath + " : " + str(remote.get_channel().get_id())
        after = dict([(f, None) for f in target.listdir(path_to_watch)])
        added = [f for f in after if not f in before]
        if len(added) > 0:
            time.sleep(interval*2)
            path = path_to_watch + "/" + added[0]
            print(path)
            if remote: 
                newFile = remote.open(path) 
            else:
                newFile = open(path, "rb")
            #Interrupt when new video comes.    
            on_new_file(newFile)
        before = after
        time.sleep(interval/2)

def on_new_file_in(newFile):
    print("new file detected: ", newFile)
    preSize = (settings["image"]["size"]["preprocess"]["width"], settings["image"]["size"]["preprocess"]["height"])
    resizedImage = resizeImage(loadImage(newFile), preSize)
    path = saveImage(resizedImage, build_path_from_settings("", settings, ["dir", "faces", "pre"]))
    faces = validate_face(newFile)
    print(faces)
    if faces:
        for face in faces:
            print("is a face")
            cropImage = cropSquare(resizedImage, face)
            finalImage = resizeImage(cropImage)
            newPath = saveImage(finalImage, build_path_from_settings("", settings, ["dir", "faces", "in"]))
    else: print("is not a face")

def on_new_file_out(newFile):
    print("new file detected: ", newFile)
    valid = validate_face(newFile)
    print(valid)
    if valid:
        print("It's a face")
        image = loadImage(newFile)
        path = saveImage(image, build_path_from_settings("", settings, ["dir", "faces", "out"]))
        show_intro()
        print ("Checking BETAFACE")
        identity = get_matching_deepfake_identity(open(path, 'rb'))
        if identity:
            print("Identitity found!: " + identity)
            show_deepfake(identity)
        else:
            print("no identity found...Exiting.")
        time.sleep(settings["timing"]["timeout"])
    else: 
        print("Not a face")

#TODO: Check identity before processing a deepfake
@parallel
def prepare_deepfake(image):
    print("Uploading Image to Deepfake API...")
    url = generate_deepfake(image)
    start = time.time()
    time.sleep(timing["process"])
    path = get_deepfake_from_url(url)
    print("Downloaded Deepfake at: " + path + "in: " + str((time.time() - start) / 60))
    process_deepfake(path)
    
def get_deepfake_from_url(url):
    while True: 
        response = download_deepfake(url)
        if response.ok:
            path = save_video(response.content, build_path_from_settings("", settings, ["dir", "deepfake"]))
            return path
        time.sleep(10)

def process_deepfake(path):
    name = generate_identity_name()
    renamedVideoPath = rename_video(path, name)
    upscaledVideoPath = build_path_from_settings("", settings, ["dir", "deepfake", "upscaled"]) + name
    file_paths = prepare_deepfake_preview(renamedVideoPath, build_path_from_settings("", settings, ["dir", "deepfake", "preview"]))
    face_ids = []
    for file in file_paths:
        image = open(file, "rb")
        face_ids.append(get_face_id_by_post(image))
    set_deepfake_identity(face_ids, name)
    finalFormattedPath = scale_deepfake(renamedVideoPath, upscaledVideoPath)
    remotePath = "/home/pi/MyVids/" + get_file_name(finalFormattedPath) + get_file_format(finalFormattedPath)
    save_on_ftp(outPi, finalFormattedPath, remotePath)
    pass

@parallel_daemon
def execOnPi(pi, command):
    sshCommand(pi,command)

def show_intro():
    sourcePath = "MyVids/intro.mp4"
    playDeepfake = commands["play"] + sourcePath
    sshCommand(outPi, playDeepfake)
    pass

def show_deepfake(identity):
    sourcePath = "/home/pi/MyVids/" + identity + ".mp4"
    playDeepfake = commands["play"] + sourcePath
    sshCommand(outPi, playDeepfake)
    pass

def main():
    run_camera_in()
    #run_camera_out()
    run_ftp_listener_in()
    #run_deepfake_listener()
    #run_ftp_listener_out()
    while True:
        time.sleep(60)
        monitor_threads()

# Operations before loop
# CORE Async Loop
if __name__ == '__main__':
    main()

# Operations after loop

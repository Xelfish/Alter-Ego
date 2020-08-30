# This is the main entry-point for Alter Ego

import socket
import asyncio
import paramiko
import json
import time
from multiprocessing import Process, freeze_support
import threading

from modules.image import *
from modules.ai_operations import *
from modules.util.files import *

# setup

settings = get_json_settings('project-settings.json')

inPi = settings["input-pi"]
outPi = settings["output-pi"]
commands =  settings["commands"]
timing = settings["timing"]

# concurrency helpers

def getLoop():
    asyncLoop = asyncio.get_running_loop()
    return asyncLoop

def parallel(func):
    def parallel_func(*args, **kw):
        if __name__ == "__main__":
            p = Process(target=func, args=args)
            p.start()
    return parallel_func

def thread_parallel(func):
    def parallel_func(*args, **kw):
        try:
            p = Process(target=func, args=args)
            p.start()
        except KeyboardInterrupt:
            sys.exit()
    return parallel_func

def fire_and_forget(func):
    def parallel_func(*args, **kw):
        p = Process(target=func, args=args)
        p.daemon = True
        p.start()
    parallel_func.__module__ = "__main__"
    return parallel_func

def run_new_process(func, *args):
    p = Process(target=func, args=args)
    p.daemon = True
    p.start()
    return p

# run "camera" on IN and OUT Pis with ssh
#@parallel
def run_camera_in():
    print("STARTED: Run Camera Input")
    execOnPi(inPi, commands['camera'])

def run_camera_out():
    # async camera task for output PI
    pass

def oneHundred():
    print("Gawh... I am so tire...zzz")
    time.sleep(10)
    print("Aaah... I slept so well")

# Run FTP Folder listener on IN and OUT Pis
def run_ftp_listener_in():
    print("STARTED: FTP Listener Input Pics")
    ftp = connectToFtp(inPi)
    watch_directory_for_change("/home/pi/MyPics", on_new_file_in, remote=ftp)

def run_ftp_listener_out():
    # listen for pictures from Input-PI and if new picture comes in run event
    pass

# Run Deepfake generator
def run_deepfake():
    print("STARTED: Listen for Deepfake Input")
    watch_directory_for_change("test/output/resized", prepare_deepfake)

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
        print("listening on: ", printpath, "...")
        after = dict([(f, None) for f in target.listdir(path_to_watch)])
        added = [f for f in after if not f in before]
        if len(added) > 0:
            time.sleep(interval)
            path = path_to_watch + "/" + added[0]
            print(path)
            if remote: 
                newFile = remote.open(path, "rb") 
            else:
                newFile = open(path, "rb")
            #on_new_file(newFile)
            threading.Thread(None, target=on_new_file_in, args=(newFile,), daemon=True).start()
            #run_new_process(on_new_file, newFile)
        before = after
        time.sleep(interval/2)


def on_new_file_in(newFile):
    print("new file detected: ", newFile)
    if validate_face(newFile):
        print("is a face")
        image = loadImage(newFile)
        resizedImage = resizeImage(image)
        newPath = saveImage("test/output/resized/")
        time.sleep(timing["timeout"])
    else: print("is not a face")


def prepare_deepfake(image):
    print("Uploading Image to Deepfake API...")
    loop = getLoop()
    url = generate_deepfake(image)
    time.sleep(timing["process"])
    while True: 
        response = download_deepfake(url)
        if response.ok:
            path = save_video(response.content)
            process_deepfake(path)
            break
        time.sleep(1)

def process_deepfake(path):
    pass

# Remote Communication tasks

def openSSH(pi):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.connect(pi["ip"], username=pi["user"], password=pi["password"])
    return client

def execOnPi(pi, command):
    client = openSSH(pi)
    print('started exec of ' + command + '...')
    stdin, stdout, stderr = client.exec_command(command, get_pty=True)
    # TODO: Implement KeyBoardInterrupt for Child process
    for line in iter(stdout.readline, ""):
        print(line, end="")
    print('finished.')
    client.close()

def connectToFtp(pi):
    client = openSSH(pi)
    ftp = client.open_sftp()
    return ftp

# listen for api response and save output video to media-server

    # download Video and take sample still-frames

    # run samples through face recognition and pair face with video

    # upload face with video pair

# listen for pictures from OUT and find matching face when a new picture is detected

    # send media-server URL to PI and command "display"

def main():
    processes = []
    try: 
        processes.append(threading.Thread(target=run_camera_in))
        processes.append(threading.Thread(target=run_ftp_listener_in))
        processes.append(threading.Thread(target=run_deepfake))
        for p in processes:
            p.start()
    except KeyboardInterrupt:
        sys.exit()



# Operations before loop
# CORE Async Loop
if __name__ == '__main__':
    main()

# Operations after loop

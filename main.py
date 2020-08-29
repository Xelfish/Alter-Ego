# This is the main entry-point for Alter Ego

import socket
import asyncio
import paramiko
import json

from modules.image import *
from modules.ai_operations import *
from modules.util.files import *

# setup

settings = get_json_settings('project-settings.json')

inPi = settings["input-pi"]
outPi = settings["output-pi"]
commands =  settings["commands"]
timing = settings["timing"]

def getLoop():
    asyncLoop = asyncio.get_running_loop()
    return asyncLoop

# run "camera" on IN and OUT Pis with subprocess or ssh
async def run_camera_in():
    print("STARTED: Run Camera Input")
    await getLoop().run_in_executor(None, execOnPi, inPi, commands['camera'])

async def run_camera_out():
    # async camera task for output PI
    pass
#TODO: create FTP Folder listener
async def run_ftp_listener_in():
    print("STARTED: FTP Listener Input Pics")
    ftp = await getLoop().run_in_executor(None, connectToFtp, inPi)
    await watch_directory_for_change("/home/pi/MyPics", on_new_file_in, remote=ftp)

async def run_ftp_listener_out():
    # listen for pictures from Input-PI and if new picture comes in run event
    pass

async def run_deepfake():
    print("STARTED: Listen for Deepfake Input")
    await watch_directory_for_change("test/output/resized", get_deepfake)

async def get_deepfake(image):
    print("Uploading Image to Deepfake API...")
    loop = getLoop()
    url = await loop.run_in_executor(None, generate_deepfake, image)
    await asyncio.sleep(20)
    while True: 
        response = await loop.run_in_executor(None, download_deepfake, url)
        if response.ok:
            path = save_video(response.content)
            await process_deepfake(path)
            break
        await asyncio.sleep(1)

async def process_deepfake(path):
    pass
# refactor this to be remote and normal
async def watch_directory_for_change(directory, on_new_file, interval=timing["interval"], remote=None):
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
            await asyncio.sleep(interval)
            path = path_to_watch + "/" + added[0]
            print(path)
            if remote: 
                newFile = remote.open(path, "rb") 
            else:
                newFile = open(path, "rb")
            await on_new_file(newFile)
        before = after
        await asyncio.sleep(interval/2)

async def on_new_file_in(newFile):
    loop = getLoop()
    # collect valid faces
    print("new file detected: ", newFile)
    if await loop.run_in_executor(None, validate_face, newFile):
        print("is a face")
        image = await loop.run_in_executor(None, loadImage, newFile)
        resizedImage = resizeImage(image)
        newPath = await loop.run_in_executor(None, saveImage, resizedImage, "test/output/resized/")
        await asyncio.sleep(timing["timeout"])
    else: print("is not a face")
        # bundle images as training data

        # send bundle to A.I. Api for training

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

#run concurrent tasks
async def tasks():
    task_run_camera = asyncio.create_task(run_camera_in())
    task_run_ftp_listener_in = asyncio.create_task(run_ftp_listener_in())
    task_run_deepfake = asyncio.create_task(run_deepfake())
    await task_run_camera
    await task_run_ftp_listener_in
    await task_run_deepfake

# Operations before loop

# CORE Async Loop
asyncio.run(tasks())

# Operations after loop

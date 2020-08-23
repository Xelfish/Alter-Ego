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

print(settings)

inPi = settings["input-pi"]
outPi = settings["output-pi"]
commands =  settings["commands"]

def getLoop():
    asyncLoop = asyncio.get_running_loop()
    return asyncLoop

# run "camera" on IN and OUT Pis with subprocess or ssh
async def run_camera_in():
    await getLoop().run_in_executor(None, execOnPi, inPi, commands['camera'])

async def run_camera_out():
    # async camera task for output PI
    pass
#TODO: create FTP Folder listener
async def run_ftp_listener_in():
    ftp = await getLoop().run_in_executor(None, connectToFtp, inPi)
    await watch_directory_for_change(ftp, on_new_file_in)

async def run_ftp_listener_out():
    # listen for pictures from Input-PI and if new picture comes in run event
    pass

async def watch_directory_for_change(ftp_connection, on_new_file, interval=1.0):
    path_to_watch = "/home/pi/MyPics"
    print("starting to watch ", path_to_watch, "...")
    before = dict([(f, None) for f in ftp_connection.listdir(path_to_watch)])
    while True:
        await asyncio.sleep(interval)
        after = dict([(f, None) for f in ftp_connection.listdir(path_to_watch)])
        added = [f for f in after if not f in before]
        if added:
            path = path_to_watch + "/" + added[0]
            print(path)
            print(ftp_connection.getcwd())
            newFile = ftp_connection.open(path) 
            await on_new_file(newFile)
        before = after

async def on_new_file_in(newFile):
    loop = getLoop()
    # collect valid faces
    print("new file detected: ", newFile)
    if await loop.run_in_executor(None, validate_face, newFile):
        print("is a face")
        image = await loop.run_in_executor(None, loadImage, newFile)
        resizedImage = resizeImage(image)
        newPath = saveImage(resizedImage, "test/output/resized/")
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
    print('started...')
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
    await task_run_camera
    await task_run_ftp_listener_in

# Operations before loop

# CORE Async Loop
asyncio.run(tasks())

# Operations after loop

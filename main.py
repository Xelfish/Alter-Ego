# This is the main entry-point for Alter Ego

import socket
from ftplib import FTP
import asyncio
import paramiko
import json

#setup

with open("project-settings.json") as settings:
    settings = json.load(settings)

inPi = settings["input-pi"]
commands =  settings["commands"]

# run "camera" on IN and OUT Pis with subprocess or ssh

async def run_camera():
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, execOnPi, inPi, commands['camera'])

def execOnPi(pi, command):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.connect(pi["ip"], username=pi["user"], password=pi["password"])
    print('started...')
    stdin, stdout, stderr = client.exec_command(command, get_pty=True)
    for line in iter(stdout.readline, ""):
        print(line, end="")
    print('finished.')
    client.close()

#TODO: create FTP Folder-listener
async def connectToFtp(pi):
    with FTP(pi["ip"], pi["user"], pi["password"]) as ftpIn:
        print(ftpIn.pwd())

# connect with ftp to both pis and setup listener pattern on output-folder
# listen for pictures from IN and when new picture comes in run it through "face-recognition" API

    # collect valid faces

    # compress images 

    # bundle images as training data

    # send bundle to A.I. Api for training

# listen for api response and save output video to media-server

    # download Video and take sample still-frames

    # run samples through face recognition and pair face with video

    # upload face with video pair

# listen for pictures from OUT and find matching face when a new picture is detected

    # send media-server URL to PI and command "display"

#run concurrent tasks
async def tasks():
    task_run_camera = asyncio.create_task(run_camera())
    await task_run_camera

# CORE Async Loop CORE Async Loop
asyncio.run(tasks())

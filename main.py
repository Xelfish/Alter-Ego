# This is the main entry-point for Alter Ego

import socket
from ftplib import FTP
import asyncio
import paramiko
import json

with open("project-settings.json") as settings:
    settings = json.load(settings)

inPi = settings["input-pi"]
commands =  settings["commands"]

# TODO: Find a way to pass parameters from (project-settings) to child-processes

# TODO: implement asyncronous architecture with "asyncio"


# run "camera" or other script on IN and OUT Pis with subprocess or ssh
# TODO: Avoid that this function blocks execution flow
async def execOnPi(pi, command):
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

    # send bundle to AI-Api for training

# listen for api response and save output video to media-server

    # download Video and take sample still-frames

    # run samples through face recognition and pair face with video

    # upload face with video pair

# listen for pictures from OUT and when new picture comes in find matching face

    # send media-server URL to PI and command "display"

#run concurrent tasks
async def main():
    exec_camera_1 = asyncio.create_task(execOnPi(inPi, commands["camera"]))
    exec_ftp_1 = asyncio.create_task(connectToFtp(inPi))
    await exec_camera_1
    await exec_ftp_1
    
asyncio.run(main())

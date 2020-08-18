# This is the main entry-point for Alter Ego

import socket
from ftplib import FTP
import asyncio
#implement more powerful ssh client handler
import subprocess
import paramiko
import json

with open("project-settings.json") as settings:
    settings = json.load(settings)

inPi = settings["input-pi"]
# connect to the two PIs and Initialize them (project-settings)

# implement asyncronous architecture with "asyncio"
# run "camera" on IN and OUT Pis with subprocess or ssh
#TODO: Make asyncronous
def execOnPi(pi, command):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.connect(pi["ip"], username=pi["user"], password=pi["password"])
    print('started...')
    stdin, stdout, stderr = client.exec_command(command)
    # TODO: Get live Output stream from external script
    for line in iter(stdout.readline, ""):
        print(line, end="")
    print('finished.')
    client.close()

execOnPi(inPi, settings["commands"]["camera"])
# connect with ftp to both pis and setup listener pattern on output-folder
with FTP(inPi["ip"], inPi["user"], inPi["password"]) as ftpIn:
    print(ftpIn.pwd())

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


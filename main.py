# This is the main entry-point for Alter Ego

import socket
from ftplib import FTP
import asyncio
#implement more powerful ssh client handler
import subprocess
import paramiko
import json

with open("project-settings.json") as settings:
    aeSettings = json.load(settings)

inPi = aeSettings["input-pi"]
# connect to the two PIs and Initialize them (project-settings)

# implement asyncronous architecture with "asyncio"
# run "camera" on IN and OUT Pis with subprocess or ssh
ssh = subprocess.Popen(["ssh", inPi["user"] + "@" + inPi["ip"], aeSettings["commands"]["camera"]],
                       shell=False,
                       stdin=subprocess.PIPE,
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE
                    )
stdout, stderr = ssh.communicate(inPi["password"].encode("UTF-8"))
print(stdout)

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


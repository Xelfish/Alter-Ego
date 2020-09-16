import subprocess
import sys
import os

VIDEONAME = sys.argv[1]

def turnScreenOff():
    subprocess.Popen(["xscreensaver-command", "-activate"])

def turnScreenOn():
    subprocess.Popen(["xscreensaver-command", "-exit"])

def playVideo(video_path):
    os.system("export DISPLAY=:0")
    subprocess.call(["cvlc", "--fullscreen", "--intf", "dummy", "--play-and-exit", VIDEONAME])
    command = "cvlc --fullscreen --intf 'dummy' --play-and-exit " + VIDEONAME
    print(command)
    pass

def main(): 
    turnScreenOn()
    playVideo(VIDEONAME)
    #turnScreenOff()

if __name__ == "__main__":
    main()
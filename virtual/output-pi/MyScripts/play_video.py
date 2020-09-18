import subprocess
import sys
import os

VIDEONAME = sys.argv[1]

def turnScreenOff():
    subprocess.Popen(["xscreensaver-command", "-activate"])

def turnScreenOn():
    subprocess.Popen(["xscreensaver-command", "-exit"])

def playVideo(video_path):
    subprocess.call(["cvlc", "--fullscreen", "--intf", "dummy", "--play-and-exit", VIDEONAME])
    command = "cvlc --fullscreen --intf 'dummy' --play-and-exit " + VIDEONAME
    print(command)
    pass

def check_file_integrity(file):
    os.system("ffmpeg -v error -i {} -f null - >error.log 2>&1".format(file))
    return os.path.getsize("error.log") == 0


def main():

    if check_file_integrity(VIDEONAME):
        turnScreenOn()
        playVideo(VIDEONAME)
    #turnScreenOff()

if __name__ == "__main__":
    main()
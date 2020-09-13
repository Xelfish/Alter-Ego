import subprocess
import sys

VIDEONAME = sys.argv[1]

def turnScreenOff():
    subprocess.Popen(["vcgencmd", "display_power", "0"])

def turnScreenOn():
    subprocess.Popen(["vcgencmd", "display_power", "1"])

def playVideo(video_path):
    subprocess.Popen(["cvlc", "--fullscreen", "--intf", "dummy", "--play-and-exit", VIDEONAME])
    pass

def main(): 
    #turnScreenOn()
    playVideo(VIDEONAME)
    #turnScreenOff()

if __name__ == "__main__":
    main()
import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../modules")
from communication import *
from util.files import *

settings = get_json_settings("project-settings.json")

def restartPi(pi):
    command = "sudo reboot"
    print("restarting: ", pi["name"])
    sshCommand(pi, command)

def main():
    pi = input("Which PI would you like to reboot?")
    if (pi == "in"):
        restartPi(settings["input-pi"])
    elif (pi == "out"):
        restartPi(settings["output-pi"])
    else:
        print("No valid pi. Aborting task...")

if __name__ == "__main__":
    main()
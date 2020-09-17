import sys
import os
import time
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../modules")
from communication import *
from util.files import *

settings = get_json_settings("project-settings.json")

def runCamera(pi):
    while True:
        print("running: ", pi["name"])
        sshCommand(pi, settings["commands"]["camera"])

def main():
    if len(sys.argv) > 1:
        target = sys.argv[1]
        if target == "in":
            runCamera(settings["input-pi"])
        if target == "out":
            runCamera(settings["output-pi"])
    else:
        print("Error. Could not find a target.")
        print("Please use: npm run-script camera -- (in/out)")

if __name__ == "__main__":
    main()
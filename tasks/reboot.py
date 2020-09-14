import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../modules")
from communication import *
from util.files import *

settings = get_json_settings("project-settings.json")



def main():
    #Implement Ask for input.
    print(settings)
    pass

if __name__ == "__main__":
    main()
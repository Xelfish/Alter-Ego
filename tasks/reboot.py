import sys

#FIXME: relative imports
from .modules.util.files import *
from .modules.communication import *

settings = get_json_settings("project-settings.json")



def main():
    #Implement Ask for input.
    print(settings)
    pass

if __name__ == "__main__":
    main()
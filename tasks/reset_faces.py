import sys
import os

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from modules.ai_operations import reset_face_ids
from modules.util.files import get_json_settings

settings = get_json_settings("project-settings.json")

def main():
    if len(sys.argv) > 1:
        reset_face_ids(sys.argv[1])
    else:
        reset_face_ids(settings["api"]["beta-face"]["namespace"])

if __name__ == "__main__":
    main()
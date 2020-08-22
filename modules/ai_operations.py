import requests
from modules.util.files import *

# This is the main module for ai-tasks

api = get_json_settings('project-settings.json')["api"]

def validate_face(image):
    response = requests.post(
    api["face_recognition"]["url"],
    files={
        'image': image,
    },
    headers={'api-key': api["face_recognition"]["key"]})
    result = response.json()['output']
    if result:
        return (len(result["faces"]) == 1)
    else: return False


def match_face(subject, matchingCandidates):
    # match face with existing face
    pass
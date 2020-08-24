import requests
from modules.util.files import *
from modules.image import *

# This is the main module for ai-tasks

api = get_json_settings('project-settings.json')["api"]

def validate_face(image):
    print("Starting Validation")
    response = requests.post(
    api["face_recognition"]["url"],
    files={
        'image': image,
    },
    headers={'api-key': api["face_recognition"]["key"]})
    result = response.json()
    print(result)
    if result and not ("err" in result.keys()):
        faces = result["output"]["faces"]
        if len(faces) == 1:
            face = faces[0]
            if float(face["confidence"]) > 0.97:
                return evaluate_face_ratio(image, face["bounding_box"])
    return False


def get_deep_fake(image):
    print("sending request...")
    response = requests.post(
        api["deepfake"]["url"],
        files={"image": image}
    )
    print("response: ", response)

def get_face_id_for_person(deepfakeStill):
    # for entered deepfake still API returns a unique face-id
    pass

def find_matching_face(image)
    # find the matching face_id in the API-Database
    pass
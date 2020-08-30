# This is the main module for AI related processing and API Interactions

import requests
from modules.util.files import *
from modules.image import *
import datetime

api = get_json_settings('project-settings.json')["api"]

def validate_face(image):
    response = requests.post(
    api["face_recognition"]["url"],
    files={
        'image': image,
    },
    headers={'api-key': api["face_recognition"]["key"]})
    result = response.json()
    print(response)
    print(result)
    if result and not ("err" in result.keys()):
        faces = result["output"]["faces"]
        if len(faces) == 1:
            face = faces[0]
            if float(face["confidence"]) > 0.97:
                return evaluate_face_ratio(image, face["bounding_box"])
    return False

def get_matching_deepfake_identity(image):
    uuid_target = get_face_id_by_post(image)
    name = recognize_face(uuid_target)
    return name

def generate_deepfake(image):
    print("sending request...")
    print(datetime.datetime.now())
    response = requests.post(
        api["deepfake"]["url"]["videourl"],
        files={"image":image}
    )
    if response.ok:
        print("response: ", response.json()["video"])
        print(datetime.datetime.now())
        return response.json()["video"]
    else:
        print (response)

def download_deepfake(url):
    print("trying to download " + url + "...")
    response = requests.get(url, allow_redirects=True)
    return response
    pass

def set_deepfake_identity(faceIds, deepfakeId):
    name = deepfakeId + "@" + api["beta-face"]["namespace"]
    # needs faceIds(list)
    # needs personId("name@namespace")
    # assigns an Identity to different faces
    pass

def get_face_id_by_post(image):
    # needs an image (formData)
    # returns faces (list) with face-uuid (entry)
    pass

def recognize_face(id):
    # needs IDs (list)
    # needs Targets (list)
    # returns matches (list) with entry "identity"
    pass

def generate_identity_name():
    # given current time and date generate a unique identity "ego-ddhhmmss"
    name = timedate.getdate()
    return name

def compose_namespace(name):
    pass

def extract_name(identity):
    pass

def get_admin_info():
    apiInfo = {"api_key":api["beta-face"]["key"], "api_secret": get_secret()}
    response = requests.get(get_betaface_url(api["beta-face"]["url"]["admin"]), params=apiInfo)
    return response.content

def get_betaface_url(suffix):
    prefix = api["beta-face"]["url"]["base"]
    return prefix + suffix
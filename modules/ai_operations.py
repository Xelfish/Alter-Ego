import requests
from modules.util.files import *
from modules.image import *
import datetime


# This is the main module for ai-tasks

api = get_json_settings('project-settings.json')["api"]

def validate_face(image):
    print("Starting Validation...")
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

def get_matching_deepfake_id(image):
    uuid_target = get_face_id_by_post(image)
    find_matching_face(uuid_target)

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
    print("trying to download...")
    response = requests.get(url, allow_redirects=True)
    return response
    pass

def post_deepfake_identity(deepfake):
    name = generate_identity_name()
    image = deepfake
    # Post image and get face-uuid
    uuid = get_face_id_by_post(image)
    request(uuid)
    # set person identity in name space

def get_face_id_by_post(image):
    # for entered deepfake still API returns a unique face-id
    uuid = requests.post(
        get_betaface_api(api["beta-face"]["url"]["media"]["file"]),
        data = {image}
    )
    return uuid
    pass

def find_matching_face(uuid):
    # find the matching face_id in the API-Database
    pass

def generate_identity_name():
    # given current time and date generate a unique identity "ego-ddhhmmss"
    name = timedate.getdate()
    return name

def get_admin_info():
    apiInfo = {"api_key":api["beta-face"]["key"], "api_secret": get_secret()}
    response = requests.get(get_betaface_api(api["beta-face"]["url"]["admin"]), params=apiInfo)
    return response.content

def get_betaface_api(suffix):
    prefix = api["beta-face"]["url"]["base"]
    return prefix + suffix
# This is the main module for AI related processing and API Interactions

import requests
from modules.util.files import *
from modules.image import *
from ai.superres import *
import os
import datetime
import re

api = get_json_settings('project-settings.json')["api"]


#TODO: Modify algorithm: return bounding box of detected faces
def validate_face(image, size):
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
        if len(faces) > 0 and len(faces) < 4:
            bounding_boxes = [f["bounding_box"] for f in faces if float(f["confidence"]) > 0.95 and f["bounding_box"][3] > size]
            return bounding_boxes
    return False

def get_matching_deepfake_identity(image):
    uuid_target = get_face_id_by_post(image)
    name = recognize_face(uuid_target)
    if name: 
        identity = extract_name(name)
        return identity
    else: 
        return False

#TODO: Build Try and Catch
def generate_deepfake(image):
    print("sending request...")
    print(datetime.datetime.now())
    response = requests.post(
        api["deepfake"]["url"]["videourl"],
        files={"file": image}
    )
    if response.ok:
        print("response: ", response.json()["video"])
        print(datetime.datetime.now())
        return response.json()["video"]
    else:
        print (response)

#TODO: Build more robust session algorithm to avoid timeouts...
def swap_deepfake_reference(video):
    print("sending post request to swap video...")
    response = requests.post(
        api["deepfake"]["url"]["swapref"],
        files={"file": video}
    )
    print(response)
    if response.ok:
        print("Video swapped successfully")
    else: 
        print("Error occurred during the upload")

def download_deepfake(url):
    print("trying to download " + url + "...")
    response = requests.get(url, allow_redirects=True)
    return response
    pass

def set_deepfake_identity(faceIds, deepfakeId):
    name = compose_namespace(deepfakeId)
    response = requests.post(
        get_betaface_url(api["beta-face"]["url"]["person"]),
        json = {
            "api_key": api["beta-face"]["key"],
            "faces_uuids": faceIds,
            "person_id": name
        }
    )
    if response.ok:
        print("Successfully set new Identity: ", name)
        return True
    else:
        print(response)
        return False

def get_face_id_by_post(image):
    print("Get face with file: ", image)
    payload = {"api_key": api["beta-face"]["key"], "file": image}
    response = requests.post(
        get_betaface_url(api["beta-face"]["url"]["media"]["file"]), 
        data={"api_key": api["beta-face"]["key"]},
        files={'file': image}
    )
    print(response)
    if response.ok:
        if response.json()["media"]["faces"]:
            face = response.json()["media"]["faces"][0]
            print("New Face ID: ", face["face_uuid"])
            return face["face_uuid"]
        else:
            print("Could not recognize a face")

def recognize_face(uuid):
    target = "all@" + api["beta-face"]["namespace"]
    response = requests.post(
        get_betaface_url(api["beta-face"]["url"]["recognize"]),
        json = {
            "api_key":  api["beta-face"]["key"],
            "faces_uuids": [
                uuid
            ],
            "targets": [
                #"all@celebrities.betaface.com",
                target
            ]
        }
    )
    print (response.json())
    if response.ok:
        matches = response.json()["results"][0]["matches"]
        for match in matches:
            print(match["person_id"], ": ", match["confidence"])
        best_match = matches[0]
        if best_match["confidence"] > 0.80:
            return best_match["person_id"]

def generate_identity_name():
    now = datetime.datetime.now()
    hours = str(now.hour).zfill(2)
    minutes = str(now.minute).zfill(2)
    seconds = str(now.second).zfill(2)
    day = str(now.day).zfill(2)
    name = "ego" + "_" + day + "_" + hours + "_" + minutes + "_" + seconds
    print("New EGO: ", name)
    return name

def compose_namespace(name):
    return  name + "@" + api["beta-face"]["namespace"]

def extract_name(identity):
    pattern = re.compile("@" + api["beta-face"]["namespace"] + "$")
    name = re.sub(pattern, "" , identity)
    print("extracted identity: " + name)
    return name

def get_betaface_url(suffix):
    prefix = api["beta-face"]["url"]["base"]
    return prefix + suffix

def get_betaface_usage():
    response = requests.get(
        get_betaface_url(api["beta-face"]["url"]["admin"]),
        params = {
            "api_key": api["beta-face"]["key"],
            "api_secret": get_secret("betaface")
        }
    )
    if response.ok: 
        usage = response.json()["usage_daily"]
        for u in usage:
            print(u)

def scale_deepfake(sourcePath, destPath):
    return upscale_video(sourcePath, destPath)
    pass
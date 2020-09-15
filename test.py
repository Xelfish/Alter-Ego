import asyncio
import time
import threading

from multiprocessing import Process

from modules.image import *
from modules.util.files import *
from modules.ai_operations import *
from ai.superres import *
import main

settings = get_json_settings('project-settings.json')

def time_function(function, *args):
    start = time.time()
    function(*args)
    print("It took ", time.time() - start , "to finish.")

def testResize():
    image = loadImage("test/input/mario.jpg")
    newImagePath = resizeImage(image)
    openImage(image)
    newImage = loadImage(newImagePath)
    openImage(newImage)

def testDownloadDeepfake(url):
    video = download_deepfake(url)
    save_video(video)

def testNameGen():
    generate_identity_name()

def testRenameDeepFake():
    rename_video("test/output/deepfakes/adb77a0b-140a-48a5-951e-2bfafe7a7565.mp4", generate_identity_name())

def testDeepFake(name):
    img = loadImage('test/input/' + name)
    rimg = resizeImage(img)
    path = saveImage(rimg, "test/input/resized/")
    generate_deepfake(open(path, 'rb'))

def testExtractIdentity():
    extract_name("test@alterego")

def testSetNewIdentity():
    name = generate_identity_name()
    path = rename_video("deepfake0000.mp4", name)
    paths = prepare_deepfake_preview (path)
    face_ids = []
    for path in paths:
        image = open(path, "rb")
        face_ids.append(get_face_id_by_post(image))
    set_deepfake_identity(face_ids, name)

def testFreezeVideo(path):
    paths = prepare_deepfake_preview(path)
    print(paths)

def testBetafaceApi():
    image = open("test/input/pratt.jpg", "rb")
    uuid = get_face_id_by_post(image)
    recognize_face(uuid)

def testFaceRecognition():
    name = "trump.jpg"
    img = open("./test/input/" + name, "rb")
    face = validate_face(img)
    if face:
        print(face)
        cropped = cropSquare(loadImage(img), face)
        saveImage(cropped, "test/input/cropped/")


def testSuperRes():
    time_function(upscale_video, "test\\input\\deep-pasi.mp4", "test\\output\\deepfake\\upscaled\\deepfake.mp4")

def testMultithreading():
    count = 0
    while True: 
        count += 1
        print("tick. Current threads: ", threading.active_count())
        threading.Thread(None, target=validate_face, args=(open("test\input\pratt.jpg", "rb").read(),)).start()
        time.sleep(1)


def testRecursivePathBuilder():
    path = build_path_from_settings("", settings, ["dir", "deepfake", "upscaled"])
    print(path)

def connectionToOutputPi():
    settings = get_json_settings()
    ftp = main.connectToFtp(settings["output-pi"])
    print(ftp)

if __name__ == "__main__":
    print("This is the output of a TEST command")
    testFaceRecognition()
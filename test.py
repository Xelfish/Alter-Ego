import asyncio
import time
import threading

from multiprocessing import Process

from modules.image import *
from modules.util.files import *
from modules.ai_operations import *
from modules.communication import *
from ai.superres import *
import main

settings = get_json_settings('project-settings.json')

def time_function(function, *args):
    start = time.time()
    function(*args)
    print("It took ", time.time() - start , "to finish.")
    print("In Minutes: " + str((time.time() -  start) / 60))

def testResize():
    image = loadImage("test/input/mario.jpg")
    newImagePath = resizeImage(image)
    openImage(image)
    newImage = loadImage(newImagePath)
    openImage(newImage)

def testDownloadDeepfake(url):
    video = download_deepfake(url)
    save_video(video.content, build_path_from_settings("", settings, ["dir", "deepfake"]))

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
    paths = prepare_deepfake_preview(path, "test/output/deepfakes/stills/")
    print(paths)

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
    path = build_path_from_settings("", settings, ["dir", "deepfake"])
    print(path)

def connectionToOutputPi():
    settings = get_json_settings()
    ftp = main.connectToFtp(settings["output-pi"])
    print(ftp)

def testMiddlePipeline():
    video = "test\\output\\deepfakes\\ego_15_14_33_53.mp4"
    main.process_deepfake(video)

def testBetafaceSetIdentity(names):
    for name in names: 
        file_paths = [
            "test\\input\\face-matching\\" + name + "1.jpg",
            "test\\input\\face-matching\\" + name + "2.jpg",
            "test\\input\\face-matching\\" + name + "3.jpg"
            ]
        face_ids = []
        for file in file_paths:
            image = open(file, "rb")
            face_ids.append(get_face_id_by_post(image))
        set_deepfake_identity(face_ids, name)

def testBetafaceApi():
    print ("The Real one")
    image = open("test\\output\\faces\\in\\image_gimp01.jpg", "rb")
    uuid = get_face_id_by_post(image)
    recognize_face(uuid)
    image = open("test\\output\\faces\\in\\image0021.jpg", "rb")
    uuid = get_face_id_by_post(image)
    recognize_face(uuid)
    image = open("test\\input\\spock.jpg", "rb")
    uuid = get_face_id_by_post(image)
    recognize_face(uuid)

def testRemoteVideoDisplay():
    sshCommand(settings["output-pi"], settings["commands"]["play"] + "/home/pi/MyVids/intro.mp4")

if __name__ == "__main__":
    print("This is the output of a TEST command")
    #testFaceRecognition()
    #testBetafaceApi()
    #time_function(testMiddlePipeline)
    #testFreezeVideo("test\output\deepfakes\deepfake_seb2.mp4")
    #testDownloadDeepfake("https://magdalenastorage.blob.core.windows.net/download/4470c691-b03b-4556-b4e2-44dd58c855ea.mp4")
    #testBetafaceSetIdentity(["freitag"])
    #testBetafaceApi()
    testRemoteVideoDisplay()
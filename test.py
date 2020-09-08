import asyncio
import time
import threading

from multiprocessing import Process

from modules.image import *
from modules.util.files import *
from modules.ai_operations import *
from ai.superres import *

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

async def testAsync(seconds):
    await asyncio.sleep(seconds)

async def async1(id, secs):
    loop = asyncio.get_running_loop()
    await testAsync(secs)
    print(id, ' done after ', secs, '...')

async def async2(id,secs):
    loop = asyncio.get_running_loop()
    await testAsync(secs)
    #await loop.run_in_executor(None, testAsync, secs)
    print(id, ' done after ', secs, '...')

def testDownloadDeepfake(url):
    video = download_deepfake(url)
    save_video(video)

def testNameGen():
    generate_identity_name()

def testRenameDeepFake():
    rename_video("deepfake0002.mp4", generate_identity_name())

def testDeepFake(name):
    img = loadImage('test/input/' + name)
    rimg = resizeImage(img)
    path = saveImage(rimg, "test/output/resized/")
    generate_deep_fake(open(path, 'rb'))

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
    name = "genius-monkey.jpg"
    img = open("./test/input/" + name, "rb")
    print(name)
    if validate_face(img):
        print("That's a valid Face!")
    else: print("Not a valid Face...")

def testSuperRes():
    time_function(upscale_video, "test\\input\\deep-pasi.mp4", "test\\output\\deepfake\\upscaled\\deepfake.avi")

def longtask(countId):
    for i in range(10):
        print("Thread started on ", countId, ": ", i)

def testMultithreading():
    count = 0
    while True: 
        count += 1
        print("tick. Current threads: ", threading.active_count())
        threading.Thread(None, target=validate_face, args=(open("test\input\pratt.jpg", "rb").read(),)).start()
        time.sleep(1)

def testMultiprocessing():
    if __name__ == "__main__":
        Process(target=subprocess).start()

async def testAsyncConcurrency():
    task1 = asyncio.create_task(async1('task 1 1', 2))
    task2 = asyncio.create_task(async2('task 2 1', 2.2))
    task3 = asyncio.create_task(async2('task 2 2', 1.8))
    task4 = asyncio.create_task(async1('task 1 2', 2.1))
    task5 = asyncio.create_task(async2('task 2 3', 2.2))

    await task1
    await task2
    await task3
    await task4
    await task5

async def testAsyncConcurrency2():
    await async1('task 1', 1)
    await async1('task 2', 1)
    await async1('task 3', 1)
    await async1('task 4', 1)
    await async1('task 5', 1)

def oneHundred():
    for i in range(1,100):
        print("R: ", i)

async def helloFromMars():
    await asyncio.sleep(3.5)
    print("hello from Mars")

def syncSleeper():
    time.sleep(2)
    print("...Aaah I slept so well")

def subprocess():
    print("Subprocess of DOOOOOOOM")

async def helloFromEarth():
    await helloFromMars()
    await asyncio.sleep(1.0)
    print("hello back from Earth")

def testRecursivePathBuilder():
    path = build_path_from_settings("", settings, ["dir", "deepfake", "upscaled"])
    print(path)

print("This is the output of a TEST command")
#testFreezeVideo("test/input/hottie.mp4")
testSuperRes()
#testRecursivePathBuilder()
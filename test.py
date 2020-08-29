import asyncio
import time
from modules.image import *
from modules.util.files import *
from modules.ai_operations import *

settings = get_json_settings('project-settings.json')

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

def testDeepFake(name):
    img = loadImage('test/input/' + name)
    rimg = resizeImage(img)
    path = saveImage(rimg, "test/output/resized/")
    generate_deep_fake(open(path, 'rb'))

def testFreezeVideo(path):
    prepare_deepfake_preview(path)

def testBetafaceApi():
    print(get_admin_info())
    image = open("./test/input/pratt.jpg", "rb")
    print(get_face_id_by_post(image))

def testFaceRecognition():
    name = "genius-monkey.jpg"
    img = open("./test/input/" + name, "rb")
    print(name)
    if validate_face(img):
        print("That's a valid Face!")
    else: print("Not a valid Face...")

async def testConcurrency():
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

async def testConcurrency2():
    await async1('task 1', 1)
    await async1('task 2', 1)
    await async1('task 3', 1)
    await async1('task 4', 1)
    await async1('task 5', 1)

async def helloFromMars():
    await asyncio.sleep(3.5)
    print("hello from Mars")

def syncSleeper():
    time.sleep(2)
    print("...Aaah I slept so well")

async def helloFromEarth():
    await helloFromMars()
    await asyncio.sleep(1.0)
    print("hello back from Earth")

print("This is the output of a TEST command")
#testDownloadDeepfake(" https://magdalenastorage.blob.core.windows.net/download/c4c5834e-752c-4dd6-8b42-e5d9fb2a09c4.mp4")
#print(settings)
#testFreezeVideo("test/input/alterego.mp4")
#testDeepFake("pickachu2.jpg")
#testFaceRecognition()
testBetafaceApi()
#testResize()
#asyncio.run(testConcurrency())
#asyncio.run(testConcurrency2())
#testDeepFake("pratt.jpg")
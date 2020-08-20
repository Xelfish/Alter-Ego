import asyncio
import time
from modules.image import *
from modules.util.files import *

settings = get_json_settings('project-settings.json')
print(settings)

def testResize():
    image = loadImage("test/input/mario.jpg")
    newImagePath = resizeImage(image)
    openImage(image)
    newImage = loadImage(newImagePath)
    openImage(newImage)

async def helloFromMars():
    await asyncio.sleep(3.5)
    print("hello from Mars")

async def helloFromEarth():
    await helloFromMars()
    await asyncio.sleep(1.0)
    print("hello back from Earth")

print("This is the output of a TEST command")
testResize()
asyncio.run(helloFromEarth())
    
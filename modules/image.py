# This is the main module for image manipulations
from PIL import Image
from modules.util.files import *

settings = get_json_settings('project-settings.json')['image']
RESIZE_FORMAT = (settings["resize"]["width"], settings["resize"]["height"])

#TODO: Develop list of image processing

def loadImage(path):
    return Image.open(path)

def openImage(image):
    image.show()

def resizeImage(sourceImage):
    destinationImage = sourceImage.resize(RESIZE_FORMAT)
    filename = get_new_file_name('test/output/resized/')
    destinationImage.save(filename)
    return filename

def prepare_deepfake_preview():
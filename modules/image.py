# This is the main module for image and video manipulations
import sys
import io
from PIL import Image
import cv2
from modules.util.files import *
from rembg.bg import remove

settings = get_json_settings('project-settings.json')['image']
RESIZE_FORMAT = (settings["size"]["deepfake"]["width"], settings["size"]["deepfake"]["height"])

def evaluate_face_ratio(image, bounding_box):
    faceArea = get_bounding_box_area(bounding_box)
    imageArea = get_image_area(loadImage(image))
    ratio = faceArea/imageArea
    print (ratio)
    return ratio > settings["face-ratio"]["min"] and ratio < settings["face-ratio"]["max"]

def loadImage(path):
    return Image.open(path)

def openImage(image):
    image.show()

def resizeImage(sourceImage, size=RESIZE_FORMAT):
    destinationImage = sourceImage.resize(size)
    return destinationImage

def saveImage(image, path):
    path = get_new_file_name(path)
    image.save(path)
    return path


def squareBox(box):
    (left, top, right, bottom) = box
    width = right - left
    height = bottom - top
    if (height > width):
        ratio = width / height
        difference = (1 - ratio) * height
        return (left - (difference/2), top, right + (difference/2), bottom)
    if (width > height):
        ratio = height / width
        difference = (1 - ratio) * width
        return (left, top - (difference/2), right, bottom + (difference/2))
    return box

def translate(box, offset):
    (left, top, right, bottom) = box
    width = right - left
    height = bottom - top
    (leftOff, topOff) = offset
    return (
        left + leftOff * width, 
        top + topOff * height, 
        right + leftOff * width, 
        bottom + topOff * height
    )

def addBleed(box, factor):
    (left, top, right, bottom) = box
    width = right - left
    height = bottom - top
    newBox = (
        left - width * factor,
        top - height * factor,
        right + width * factor,
        bottom + height * factor
    )
    return newBox

def cropSquare(image, box):
    [left, top, width, height] = box
    box = (left, top, left + width, top + height)
    adjustedBox = translate(addBleed(squareBox(box), 0.3), (0, - 0.1))
    croppedImage = image.crop(adjustedBox)
    return croppedImage

def prepare_deepfake_preview(sourcePath, folder):
    targetFrames = {tf for tf in settings["preview"]["frames"]}
    cam = cv2.VideoCapture(sourcePath) 
    frameCount = 0
    paths = [] 
    while True:
        material, frame = cam.read()
        if not material:
            break 
        if frameCount in targetFrames:
            name = get_new_file_name(folder, get_file_name(sourcePath) + "_")
            print ('Creating ' + name + " from f. " + str(frameCount) + "...") 
            cv2.imwrite(name, frame) 
            paths.append(name)
        frameCount += 1
    cam.release() 
    cv2.destroyAllWindows()
    return paths

def get_bounding_box_area(bounding_box):
    left, top, right, bottom = bounding_box
    area = right * bottom
    return area

def get_image_area(image):
    width, height = image.size
    area = width * height
    return area

def remove_background(sourcePath):
    settings = get_json_settings("project-settings.json")
    destPath = build_path_from_settings("", settings, ["dir", "faces", "in"]) + get_file_name(sourcePath) + "_t.png"
    print("Removing background from: " + sourcePath + "...")
    with open(sourcePath, 'rb') as img:
        with open(destPath, 'wb+') as finalimg:
            finalimg.write(remove(img.read()))
    return destPath
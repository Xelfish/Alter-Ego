import cv2
from cv2 import dnn_superres


def superscale():
    # Create an super_res object
    super_res = dnn_superres.DnnSuperResImpl_create()

    # Read image
    image = cv2.imread('test/input/mario.jpg').astype('uint8')

    # Read the desired model
    path = "ai/models/ESPCN_x4.pb"
    super_res.readModel(path)

    # Set the desired model and scale to get correct pre- and post-processing
    super_res.setModel("espcn", 4)

    # Upscale the image
    result = super_res.upsample(image)

    # Save the image
    cv2.imwrite("test/output/upscaled.png", result)
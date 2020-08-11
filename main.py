# This is the main entry-point for Alter Ego

# IMPORT of necessary Libraries


# load Data from "project-settings.json" and store it as an object

# connect to the two PIs and Initialize them (project-settings)

# run "camera" on IN and OUT Pis

# listen for pictures from IN and when new picture comes in run it through "face-recognition" API

    # collect valid faces

    # compress images 

    # bundle images as training data

    # send bundle to AI-Api for training

# listen for api response and save output video to media-server

    # download Video and take sample still-frames

    # run samples through face recognition and pair face with video

    # upload face with video pair

# listen for pictures from OUT and when new picture comes in find matching face

    # send media-server URL to PI and command "display"


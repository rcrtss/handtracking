import cv2
import numpy
from HandTracker import HandTracker
from send_coordinates import send_coordinates


# Create a VideoCapture object
video_capture = cv2.VideoCapture(0)

# Check if the camera is opened successfully
if not video_capture.isOpened():
    print("Error opening video stream or file")

# Set relative path to pretrained model to use
model_path = 'hand_landmarker.task'

# Create hand tracker object
hand_tracker = HandTracker(video_capture, model_path)

# Main loop
while True:
    hand_tracker.calculate_finger_position(display=False)
    x, y = hand_tracker.get_coordinates()
    send_coordinates(x,y)





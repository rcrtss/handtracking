import cv2
import mediapipe as mp
import time
import numpy as np
from LPFilter import LowPassFilter

def landmarks_list_to_array(landmark_list, rows, cols):
    return np.asarray([(lmk.x * cols, lmk.y * rows, lmk.z * cols)
                       for lmk in landmark_list.landmark])

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()

mpDraw = mp.solutions.drawing_utils

number_of_hands = 2
number_of_landmarks = 21
number_of_axis = 3

x = 0
y = 0

LPF_H0 = LowPassFilter(alpha=0.3)
LPF_H1 = LowPassFilter(alpha=0.3)

while True:
    _, frame = cap.read()
    height = frame.shape[0]
    width = frame.shape[1]

    data = hands.process(frame)
    results = data.multi_hand_landmarks

    frame_landmarks = np.zeros([number_of_hands, number_of_landmarks, number_of_axis])

    canvas = frame
    # Comment line above and uncomment below to have a black blackground instead of the input frame
    # canvas = np.zeros((height, width, 3), np.uint8)

    if results:
        for idx, landmarks in enumerate(results):
            landmarks_array = landmarks_list_to_array(landmarks, height, width)
            frame_landmarks[idx, :len(landmarks_array)] = landmarks_array

    if(frame_landmarks[0][8][0]):
        x,y = LPF_H0.apply(int(frame_landmarks[0][8][0]),int(frame_landmarks[0][8][1]))
    canvas = cv2.circle(canvas, (x,y), radius=5, color=(0, 0, 255), thickness=-1)

    if(frame_landmarks[1][8][0]):
        x,y = LPF_H1.apply(int(frame_landmarks[1][8][0]),int(frame_landmarks[1][8][1]))
    canvas = cv2.circle(canvas, (x,y), radius=5, color=(0, 0, 255), thickness=-1)

    canvas = cv2.flip(canvas, 1)
    cv2.imshow('tracked',canvas)
    cv2.waitKey(1)
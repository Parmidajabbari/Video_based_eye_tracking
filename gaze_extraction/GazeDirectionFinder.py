import l2cs
from l2cs import Pipeline, render
import cv2
import os
from l2cs import Pipeline, render
import cv2
import torch
import numpy as np

CWD = os.getcwd()
model_path = os.path.join(CWD, '../gaze_extraction/models', 'L2CSNet_gaze360.pkl')
print(model_path)
gaze_pipeline = Pipeline(
    weights=model_path,
    arch='ResNet50',
    device=torch.device('cpu')  # or 'gpu'
)

def extract_directon(frame):
    results = gaze_pipeline.step(frame)
    frame = render(frame, results)
    
    pitch = results.pitch
    yaw = results.yaw
    bboxes = results.bboxes
    landmarks = results.landmarks
    scores = results.scores
    # print(salam)
    return frame

# cap = cv2.VideoCapture(0)
# while(True):
#     _, frame = cap.read()    
#     # Process frame and visualize
#     results = gaze_pipeline.step(frame)
#     # print(type(results.pitch))
#     results.pitch.fill(0)
#     frame = render(frame, results)
#     cv2.imshow('frame', frame)
#     cv2.waitKey(0)

# print(type(frame))


# print(yaw,pitch)

# def gazeto3d(one, two):
#     gaze_gt = np.zeros([3])
#     gaze_gt[0] = -np.cos(two) * np.sin(one)
#     gaze_gt[1] = -np.sin(two)
#     gaze_gt[2] = -np.cos(two) * np.cos(one)
#     return gaze_gt

# x1 = gazeto3d(yaw, pitch)

# x2 = gazeto3d(pitch, yaw)
# print(x1, x2)

# import turtle
# window_width = turtle.window_width()

# window_height = turtle.window_height()

# x1 = int(x1*window_width)
# x1[1] = int(x1[1]*window_height)
# x2[0] = int(x2[0]*window_width)
# x2[1] = int(x2[1]*window_height)
# print(window_width, window_height)

# img1 = cv2.circle(frame, (x1[0], x1[1]), radius=0, color=(0, 0, 255), thickness=2)
# img2 = cv2.circle(frame, (x2[0], x2[1]), radius=0, color=(0, 0, 255), thickness=2)
# cv2.imshow('thiw',frame)
# cv2.imshow('thiw',img1)
# cv2.imshow('thiw',img2)

# while True:
#     video_stream = cv2.VideoCapture(0) 
#     success, frame = video_stream.read()
#     if not success:
#         break
#     ret, buffer = cv2.imencode('.jpg', frame)
#     cv2.imshow('frame', frame)
#     frame = buffer.tobytes()
#     results = gaze_pipeline.step(frame)
#     frame = render(frame, results)
#     cv2.imshow('frame', frame)

# cv2.waitKey()
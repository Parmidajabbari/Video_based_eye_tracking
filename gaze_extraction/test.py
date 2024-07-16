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
cap = cv2.VideoCapture(0)
while(True):
    _, frame = cap.read()    
    # Process frame and visualize
    results = gaze_pipeline.step(frame)
    frame = render(frame, results)
    cv2.imshow('frame', frame)
    cv2.waitKey(0)
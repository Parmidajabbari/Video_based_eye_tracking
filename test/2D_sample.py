
import torch
from torchvision import transforms
from model import Model
import cv2
import numpy as np
from sklearn.linear_model import LinearRegression
import time

# Load the trained model
neural_network_model = Model()
neural_network_model.load_state_dict(torch.load('/Users/danialazimi/Desktop/CV_implementations/GazeTR/Transformer/checkpoints/Iter_30_trans6.pt', map_location=torch.device('cpu')))
# neural_network_model.load_state_dict(torch.load('/Users/danialazimi/Desktop/CV_implementations/GazeTR/data/GazeTR-H-ETH.pt', map_location=torch.device('cpu')))
neural_network_model.eval()

# Initialize the webcam
cap = cv2.VideoCapture(0)  # Use 0 for the default camera

calibration_points = [(100,100), (667,100), (1400,100),
                      (100,665), (667,665), (1400,665),
                      (100,900), (667,900), (1400,900),]
recorded_gaze_points = []

gaze_screen_x, gaze_screen_y = 0, 0
# Initialize the screen coordinates for gaze prediction

# Loop for calibration
face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
frame_rate = 4
prev_time = time.time()


def detect_face(in_frame):
    gray_image = cv2.cvtColor(in_frame, cv2.COLOR_BGR2GRAY)
    
    # Detect faces
    faces = face_classifier.detectMultiScale(gray_image, 1.1, 5, minSize=(40, 40))
    
    # Initialize variables to store the detected face, eyes, and face grid
    detected_face = None
    
    # Limit the detection to one face and two eyes
    for (x, y, w, h) in faces:
        if detected_face is None:
            detected_face = (x, y, w, h)    
        # Break out of the loop after detecting one face
        break
    return detected_face


for point in calibration_points:
    while True:  
        ret, frame = cap.read()

        current_time = time.time()
        # Check if the time elapsed since the last frame is less than the desired frame rate
        if current_time - prev_time < 1 / frame_rate:
            continue  # Skip this frame if it's too earlY
        # Update the previous time
        prev_time = current_time    

        # Display the calibration point on the frame
        cv2.circle(frame, point, 20, (0, 0, 255), -1)

        # Display the frame with calibration point
        cv2.imshow('Calibration', frame)
        
        detected_face = detect_face(frame)
        if detected_face :
            # Extract the face and eyes regions
            (x, y, w, h) = detected_face
            face_img = frame[y : y + h, x : x + w]
        face_img = cv2.resize(face_img, (224, 224))    
        face_img = cv2.resize(face_img, (224, 224))    
        # Convert the frame to a PyTorch tensor
        transform = transforms.ToTensor()
        frame_tensor = transform(face_img)
        with torch.no_grad():
            gaze = neural_network_model.forward({"face": frame_tensor.unsqueeze(0)})
        gaze_direction = gaze.squeeze().detach().numpy()
        yaw, pitch = gaze_direction

            # Exit the loop when the user presses 'c' (record the gaze point) or 'q' to quit calibration
        key = cv2.waitKey(1)
        if key & 0xFF == ord('c'):
            recorded_gaze_points.append((yaw, pitch))
            break
        elif key & 0xFF == ord('q'):
            break  # Quit the calibration loop

# Compute calibration mapping (e.g., using linear regression) to map model predictions to screen coordinates
recorded_gaze_points = np.array(recorded_gaze_points)
calibration_points = np.array(calibration_points)

regression_model = LinearRegression()
regression_model.fit(recorded_gaze_points, calibration_points)

# Function to map gaze predictions to screen coordinates using the model
def map_to_screen_coordinates(yaw, pitch, model):
    gaze_prediction = np.array([[yaw, pitch]])
    screen_coordinates = model.predict(gaze_prediction)
    return screen_coordinates[0]


# Real-time gaze prediction and display
# Control frame rate
frame_rate = 4  # 4 frames per second
prev_time = time.time()

while True:
    ret, frame = cap.read()
    current_time = time.time()
    if current_time - prev_time >= 1 / frame_rate:
        prev_time = current_time

        detected_face = detect_face(frame)
        if detected_face :
            # Extract the face and eyes regions
            (x, y, w, h) = detected_face
            face_img = frame[y : y + h, x : x + w]
        face_img = cv2.resize(face_img, (224, 224))    
        face_img = cv2.resize(face_img, (224, 224))    
        # Convert the frame to a PyTorch tensor
        transform = transforms.ToTensor()
        frame_tensor = transform(face_img)
        with torch.no_grad():
            gaze = neural_network_model.forward({"face": frame_tensor.unsqueeze(0)})
        gaze_direction = gaze.squeeze().detach().numpy()
        yaw, pitch = gaze_direction

        # Map model predictions to screen coordinates using the calibration mapping
        screen_x, screen_y = map_to_screen_coordinates(yaw, pitch, regression_model)

        # Display gaze point as a circle on the frame
        cv2.circle(frame, (int(screen_x), int(screen_y)), 10, (0, 0, 255), -1)

        # Display the frame with gaze estimation and gaze point
        cv2.imshow('Gaze Estimation', frame)

    # Exit the loop by pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()

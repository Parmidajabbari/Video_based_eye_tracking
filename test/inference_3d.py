import torch
from torchvision import transforms

import cv2
from model import Model
import time
import math
# GazeTR = Model()
model = Model()
# model.load_state_dict(torch.load('/Users/danialazimi/Desktop/CV_implementations/GazeTR/data/GazeTR-H-ETH.pt', map_location=torch.device('cpu')))
model.load_state_dict(torch.load('/Users/danialazimi/Downloads/Iter_30_after30_trans6.pt',  map_location=torch.device('cpu')))
model.eval()

# Real-time gaze prediction and display
# Control frame rate
frame_rate = 1  # 4 frames per second
prev_time = time.time()

cap = cv2.VideoCapture(0)  # 0 represents the default webcam, change it if necessary

while True:
    ret, frame = cap.read()
    current_time = time.time()
    if current_time - prev_time >= 1 / frame_rate:
        prev_time = current_time
   
        # Resize the frame to 224x224 pixels and convert to RGB
        processed_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        processed_frame = cv2.resize(frame, (224, 224))

        # Convert the frame to a PyTorch tensor
        transform = transforms.ToTensor()
        frame_tensor = transform(processed_frame)

        # Perform inference
        with torch.no_grad():
            gaze = model.forward({"face": frame_tensor.unsqueeze(0)})
        gaze_direction = gaze.squeeze().detach().numpy()

        yaw , pitch = gaze_direction
        # Constants for screen dimensions and center point
        screen_width = 1920  # Adjust based on your screen resolution
        screen_height = 1080  # Adjust based on your screen resolution
        # center_x = screen_width // 2
        # center_y = screen_height // 2
        # # Define maximum yaw and pitch values (in radians) that correspond to screen boundaries
        # max_yaw = math.radians(30)  # Example: +/- 30 degrees
        # max_pitch = math.radians(20)  # Example: +/- 20 degrees
        # # Map yaw and pitch to screen coordinates
        # gaze_x = center_x + int(yaw / max_yaw * (screen_width / 2))
        # gaze_y = center_y - int(pitch / max_pitch * (screen_height / 2))

        # # Ensure that gaze_x and gaze_y stay within the screen boundaries
        # end_x = max(0, min(gaze_x, screen_width))
        # end_y = max(0, min(gaze_y, screen_height))
        center_x = screen_width // 2
        center_y = 0  # Camera is at the top middle, so y-coordinate is 0

        # Camera distance from the screen (in centimeters)
        camera_distance = 40.0  # 40 cm

        # Convert yaw and pitch to radians
        yaw_rad = math.radians(yaw)
        pitch_rad = math.radians(pitch)

        # Calculate horizontal and vertical distances
        horizontal_distance = camera_distance * math.tan(yaw_rad)
        vertical_distance = camera_distance * math.tan(pitch_rad)

        # Calculate gaze coordinates on the screen
        gaze_x = int(center_x + (horizontal_distance * screen_width / 2))
        gaze_y = int(center_y - (vertical_distance * screen_height / 2))

        # Ensure that gaze_x and gaze_y stay within the screen boundaries
        end_x = max(0, min(gaze_x, screen_width))
        end_y = max(0, min(gaze_y, screen_height))

        # Now, gaze_x and gaze_y represent the coordinates on the screen where the user's gaze points.


        # print("gaze direction shape:  ", gaze_direction.shape , ':::',gaze_direction)

        # # Calculate the end point for the gaze direction vector
        # frame_height, frame_width, _ = frame.shape
        # center_x, center_y = frame_width // 2, frame_height // 2

        # ##### whatttttt?
        # yaw =  yaw
        # pitch = pitch
        # # yaw =     (-1*yaw ) 
        # # pitch  =  (-1*pitch )
        # print(yaw,pitch)
        # # Define regions based on yaw and pitch
        # if yaw >= 0 and pitch >= 0:
        #     # Top-right region
        #     color = (0, 0, 255)  # Red color
        #     region_name = "Top-Right"
        #     end_x, end_y = center_x +  int(frame_width / 4), center_y - int(frame_height / 4)
        # elif yaw >= 0 and pitch < 0:
        #     # Bottom-right region
        #     color = (0, 255, 0)  # Green color
        #     region_name = "Bottom-Right"
        #     end_x, end_y = center_x +  int(frame_width / 4), center_y + int(frame_height / 4)
        # elif yaw < 0 and pitch >= 0:
        #     # Top-left region
        #     color = (255, 0, 0)  # Blue color
        #     region_name = "Top-Left"
        #     end_x, end_y = center_x -  int(frame_width / 4), center_y - int(frame_height / 4)
        # else:
        #     # Bottom-left region
        #     color = (255, 255, 0)  # Yellow color
        #     region_name = "Bottom-Left"
        #     end_x, end_y = center_x -  int(frame_width / 4), center_y + int(frame_height / 4)
        # print('frame height', frame_height)    
        # print(region_name)
        color = (255, 255, 0)
        radius = 20  # Adjust the radius as needed
        thickness = 20  # Adjust the thickness as needed
        cv2.circle(frame, (end_x, end_y), radius, color, thickness)



        # end of the frame process and gaze estimation

        cv2.imshow("Gaze Estimation", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()




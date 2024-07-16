import sys
import time
import cv2
import os
import numpy as np
import mediapipe as mp
from collections import deque
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import io
matplotlib.use('Agg')   # This needs to be done before importing pyplot
import matplotlib.patches as patches
from PIL import Image
import numpy as np


from hsemotion_onnx.facial_emotions import HSEmotionRecognizer

def process_frames_emotion(face_image):
    # In here we make an array that gives us every emotion number
    emotions = [None]*8
    # Anger: emotions[0], Contempt: emotions[1], Disgust: emotions[2], Fear: emotions[3]
    # Happiness: emotions[4], Neutral: emotions[5], Sadness: emotions[6], Surprise: emotions[7]

    mp_face_mesh = mp.solutions.face_mesh
    mp_drawing = mp.solutions.drawing_utils
    drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
    face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5)

    model_name = 'enet_b0_8_best_vgaf'
    fer = HSEmotionRecognizer(model_name=model_name)

    maxlen = 15
    recent_scores = deque(maxlen=maxlen)

    total_start = time.time()
    image_rgb = cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)
    start = time.time()
    results = face_mesh.process(image_rgb)
    elapsed = (time.time() - start)
    print('Face mesh elapsed:', elapsed)
    gray = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
    if results.multi_face_landmarks:
        height, width, _ = face_image.shape
        for face_landmarks in results.multi_face_landmarks:
            if False:
                mp_drawing.draw_landmarks(
                    image=face_image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACE_CONNECTIONS,
                    landmark_drawing_spec=drawing_spec,
                    connection_drawing_spec=drawing_spec)
            x1 = y1 = 1
            x2 = y2 = 0
            for id, lm in enumerate(face_landmarks.landmark):
                cx, cy = lm.x, lm.y
                if cx < x1:
                    x1 = cx
                if cy < y1:
                    y1 = cy
                if cx > x2:
                    x2 = cx
                if cy > y2:
                    y2 = cy
            if x1 < 0:
                x1 = 0
            if y1 < 0:
                y1 = 0
            x1, x2 = int(x1 * width), int(x2 * width)
            y1, y2 = int(y1 * height), int(y2 * height)
            face_img = image_rgb[y1:y2, x1:x2, :]
            if np.prod(face_img.shape) == 0:
                print('Empty face ', x1, x2, y1, y2)
                continue

            start = time.time()
            emotion, scores = fer.predict_emotions(face_img, logits=True)
            elapsed = (time.time() - start)
            #
            # recent_scores = []
            # (DOWN) we need to get mean in here because if we don't it changes every moment but we can set a threshould for example in every 10 frames pop one
            recent_scores.append(scores)

            scores = np.mean(recent_scores, axis=0)
            
            emotions = scores
            
            # data = emotions[0:4]
            # categories = ['A', 'B', 'C', 'D', 'E']
            # plt.bar(categories, plt_data)
            # plt.title('Emotions')
            # plt.xlabel('Categories')
            # plt.ylabel('Values') 
            # plt.savefig('/Volumes/work/Deep Learning/EyeTrackingResearch/code/Video_based_eye_tracking/emotion_extraction/emotionFinder_output.png', bbox_inches='tight')
            
            # Creating the bar chart
            
            #####################################################################
            # fig, ax = plt.subplots(figsize=(5, 3))
            # data = emotions[0:4]
            # categories = ['A', 'B', 'C', 'D', 'E']
            # ax.bar(categories, data)
            # ax.axis('off')  # Hide axes
            # plt.tight_layout()
            # # Save figure to a BytesIO object
            # buf = BytesIO()
            # plt.savefig(buf, format='png', transparent=True)
            # buf.seek(0)
            # # Load this image into OpenCV
            # bar_chart_img = np.array(plt.imread(buf, format='png'))
            # buf.close()

            # # Close plt to free memory
            # plt.close(fig)

            # # bar_chart_img is in RGBA format (OpenCV uses BGR)
            # # So we convert the read image from RGBA to BGRA
            # bar_chart_img = cv2.cvtColor(bar_chart_img, cv2.COLOR_RGBA2BGRA)

            # # Resize the bar chart as needed
            # # As an example, the bar chart width is set to half of the photo's width
            # bar_chart_scaled_width = image.shape[1] // 2
            # bar_chart_scaled_height = int(bar_chart_scaled_width * bar_chart_img.shape[0] / bar_chart_img.shape[1])
            # bar_chart_resized = cv2.resize(bar_chart_img, (bar_chart_scaled_width, bar_chart_scaled_height))

            # # Define the position to overlay the bar chart image on top left corner
            # x_offset = 0
            # y_offset = 0

            # # Extract the region of interest (ROI) from the main image
            # roi = image[y_offset:y_offset+bar_chart_resized.shape[0], x_offset:x_offset+bar_chart_resized.shape[1]]

            # # Overlay the bar chart onto the ROI
            # # Since we're sure both are the same size, no masking is required.
            # image[y_offset:y_offset+bar_chart_resized.shape[0], x_offset:x_offset+bar_chart_resized.shape[1]] = \
            #     image[y_offset:y_offset+bar_chart_resized.shape[0], x_offset:x_offset+bar_chart_resized.shape[1]] * \
            #     (1 - bar_chart_resized[:, :, 3:] / 255) + bar_chart_resized[:, :, :3] * (bar_chart_resized[:, :, 3:] / 255)
            
            #####################################################################
            # Display the image
            # Create the bar graph
            
            # values = [emotions[0],emotions[2:]]
            # categories = ['Anger', 'Disgust', 'Fear', 'Happiness', 'Neutral', 'Sadness',  'Surprise']
            # values = emotions
            values = [emotions[0],emotions[2],emotions[3],emotions[4],emotions[5],emotions[6],emotions[7]]
            categories = ['Anger', 'Disgust', 'Fear', 'Happiness', 'Neutral', 'Sadness',  'Surprise']

            # values = [1,2,3,4,5]
            # Create the bar graph without showing it
            # Create the bar graph without showing it
            fig, ax = plt.subplots(figsize=(7, 6), dpi=300)  # Adjust the figure size if needed
            # bars = ax.barh(categories, values, color=['red', 'green', 'black', 'blue', 'orange', 'purple', 'brown', 'yellow'])  # Change bar colors
            bars = ax.barh(categories, values, color=['red', 'black', 'blue', 'orange', 'purple', 'brown', 'yellow'])  # Change bar colors

            ax.set_xlabel('')  # X-axis label
            ax.set_ylabel('Emotion')  # Y-axis label
            ax.set_title('Emotions')  # Plot title
            ax.invert_yaxis()  # Hide axes to only show the bar graph

            # Convert the plot to a PIL Image
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', bbox_inches='tight', dpi=300, transparent=True)
            buffer.seek(0)
            plot_img = Image.open(buffer)
            ####################
            current_directory = '/Volumes/work/Deep Learning/EyeTrackingResearch/code/Video_based_eye_tracking/webapp'
            print(current_directory)
            # Get the current working directory
            file_path = os.path.join(current_directory, "saved_image.jpg")  # Create the file path for the image
            
            if plot_img.mode in ('RGBA', 'LA') or (plot_img.mode == 'P' and 'transparency' in plot_img.info):
                plot_img = plot_img.convert('RGB')
                
            plot_img.save(file_path) 
            ####################
            # Convert the plot image to RGB mode
            # plot_img = plot_img.convert('RGB')

            # Resize the plot image to match the size where it will be pasted
            # plot_img = plot_img.resize((200, 200))  # Replace 100, 100 with the desired size

            # Convert PIL Images to numpy arrays
            original_img_np = np.array(face_image)
            plot_img_np = np.array(plot_img)
            # place the graph on the original image
            position = (430, 10)  # Change the coordinates as needed to position the graph on the image

            # Paste the plot onto the original image
            # original_img_np[position[1]:position[1]+plot_img_np.shape[0], position[0]:position[0]+plot_img_np.shape[1]] = plot_img_np
            
            # image = original_img_np
            
            # (UP) this part plays a crucial rule
            
            emotion = np.argmax(scores)
            print(scores, fer.idx_to_class[emotion], 'Emotion elapsed:', elapsed)

            # cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)
            fontScale = 1
            min_y = y1
            if min_y < 0:
                min_y = 10
            cv2.putText(face_image, fer.idx_to_class[emotion], (x1, min_y), cv2.FONT_HERSHEY_PLAIN, fontScale=fontScale,
                        color=(0, 255, 0), thickness=1)
    elapsed = (time.time() - total_start)
    print('Total frame processing elapsed:', elapsed)
    face_mesh.close()
    return face_image, emotions, plot_img_np

def process_video(videofile=0):
    mp_face_mesh = mp.solutions.face_mesh
    mp_drawing = mp.solutions.drawing_utils
    drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
    #face_mesh=mp_face_mesh.FaceMesh(max_num_faces=1,min_detection_confidence=0.5,min_tracking_confidence=0.5)
    face_mesh=mp_face_mesh.FaceMesh(max_num_faces=1,refine_landmarks=True,min_detection_confidence=0.5,min_tracking_confidence=0.5)

    model_name='enet_b0_8_best_vgaf'
    #model_name='enet_b0_8_va_mtl'
    fer=HSEmotionRecognizer(model_name=model_name)

    maxlen=15 #51
    recent_scores=deque(maxlen=maxlen)

    cap = cv2.VideoCapture(videofile)
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            #print("Ignoring empty camera frame.")
            break

        total_start = time.time()
        # Flip the image horizontally for a later selfie-view display, and convert
        # the BGR image to RGB.
        #image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        start = time.time()
        results = face_mesh.process(image_rgb)
        elapsed = (time.time() - start)
        print('Face mesh elapsed:',elapsed)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        if results.multi_face_landmarks:
            height,width,_=image.shape
            for face_landmarks in results.multi_face_landmarks:
                if False:
                    mp_drawing.draw_landmarks(
                        image=image,
                        landmark_list=face_landmarks,
                        connections=mp_face_mesh.FACE_CONNECTIONS,
                        landmark_drawing_spec=drawing_spec,
                        connection_drawing_spec=drawing_spec)
                x1 = y1 = 1
                x2 = y2 = 0
                for id, lm in enumerate(face_landmarks.landmark):
                    cx, cy = lm.x, lm.y
                    if cx<x1:
                        x1=cx
                    if cy<y1:
                        y1=cy
                    if cx>x2:
                        x2=cx
                    if cy>y2:
                        y2=cy
                if x1<0:
                    x1=0
                if y1<0:
                    y1=0
                x1,x2=int(x1*width),int(x2*width)
                y1,y2=int(y1*height),int(y2*height)
                face_img=image_rgb[y1:y2,x1:x2,:]
                if np.prod(face_img.shape)==0:
                    print('Empty face ', x1,x2,y1,y2)
                    continue
                
                start = time.time()
                emotion,scores=fer.predict_emotions(face_img,logits=True)
                # print(emotion,'\n')
                elapsed = (time.time() - start)
                #
                # recent_scores = []
                recent_scores.append(scores)
                scores=np.mean(recent_scores,axis=0)
                print(scores)
                print('\n')
                
                emotion=np.argmax(scores)
                #Anger: 0, Contempt: 1, Disgust:2, Fear:3, Happiness:4, Neutral:5, Sadness:6,  Surprise:7

                for i in range(0,8):
                    print(fer.idx_to_class[i],'\n')
                    
                print(scores,fer.idx_to_class[emotion], 'Emotion elapsed:',elapsed)
                
                cv2.rectangle(image, (x1,y1), (x2,y2), (255, 0, 0), 2)
                fontScale=1
                min_y=y1
                if min_y<0:
                    min_y=10
                    
                cv2.putText(image, fer.idx_to_class[emotion], (x1, min_y), cv2.FONT_HERSHEY_PLAIN , fontScale=fontScale, color=(0,255,0), thickness=1)
        elapsed = (time.time() - total_start)
        print('Total frame processing elapsed:',elapsed)
        cv2.imshow('Facial emotions', image)
        if cv2.waitKey(5) & 0xFF == 27:
          break

    face_mesh.close()
    cap.release()
    return image

if __name__ == '__main__':
    if len(sys.argv)==2:
        process_video(sys.argv[1])
    else:
        process_video()
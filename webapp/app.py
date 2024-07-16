from flask import Flask, render_template, Response, request, jsonify
import cv2
from VideoProcessor import VideoProcessor
from DisplayProcessor import DisplayProcessor
from landmark_extraction import LandmarkFinder
from data import DataSet

from properties.ApplicationProperties import ApplicationProperties
# from Logging import configure_logging
import base64
import random
import numpy as np
from emotion_extraction import emotionFinder

import subprocess
# Define the wget command as a list of arguments
# wget_command = [
#     'wget',
#     '-O', 'face_landmarker_v2_with_blendshapes.task',  # Output filename
#     'https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task'
# ]

# # Execute the wget command
# try:
#     subprocess.run(wget_command, check=True)
#     print("Download completed successfully.")
# except subprocess.CalledProcessError as e:
#     print(f"Download failed with error: {e}")
    
import logging
# Configure the logging system
logging.basicConfig(
    level=logging.DEBUG,  # Set the desired logging level
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('my_app.log'),  # Log to a file
        logging.StreamHandler()  # Log to the console
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_url_path='/static')
app_properties = ApplicationProperties()
video_stream = cv2.VideoCapture(app_properties.video_source)  # Open default camera (index 0)
video_processor = VideoProcessor(video_stream)
display_processor = DisplayProcessor()
data_set = DataSet.DataSet('./')



forms = {
    'form1': {
        'type': 'video',
        'content': 'static/forms/video.mp4',
        'time_interval': 10  # Time interval in seconds for this form
    },
    'form2': {
        'type': 'slideshow',
        'content': [
            'static/forms/image1.jpeg',
            'static/forms/image2.jpeg'
        ],
        'time_interval': 2  # Time interval in seconds for this form
    },
    'form3': {
        'type': 'document',
        'content': 'static/forms/document.pdf',
        'time_interval': 15  # Time interval in seconds for this form
    },
    'form4': {
        'type': 'special',
        'time_interval': 5  # Time interval in seconds for this form
    },
    'form5': {
        'type': 'stroop',
        'content': [
            'static/forms/image1.jpeg',
            'static/forms/image2.jpeg',
            'stroop.html'
        ],
        'time_interval': 4  # Time interval in seconds for this form
    },
    'sadStroop': {
        'type': 'stroop',
        'content': [
            'static/forms/image1.jpeg',
            'static/forms/image2.jpeg',
            'stroop.html'
        ],
        'time_interval': 6  # Time interval in seconds for this form
    },
    'happyStroop': {
        'type': 'stroop',
        'content': [
            'static/forms/image3.jpeg',
            'static/forms/image4.jpeg',
            'stroop.html'
        ],
        'time_interval': 6  # Time interval in seconds for this form
    }
}


@app.route('/')
def eye_tracker():
    return render_template('eye_tracker.html')

@app.route('/video_feed')
def video_feed():
    return Response(video_processor.generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/save_image', methods=['POST'])
def save_image():
    frame_data = request.json['image_data']    
    frame, raw = video_processor.save_frame(frame_data)
    print("This")
    landmarks, output_frame = video_processor.process_frame(frame)
    landmarks, output_frame = '', frame
    gaze = ['', '']
    if (app_properties.active_form_id == 'form4'):
        gaze = display_processor.get_point()
        print(gaze)
    # display_processor.make_circle_points(3, 4)
    gaze, index = display_processor.get_point()
    
    index = video_processor.get_frame_count()
    data_set.write_frameData_to_csv(index, f"/{index}", landmarks, gaze)

    
    i , image_with_landmarks = video_processor.process_frame(output_frame)
    image_with_emotion, emotions, plot_image = emotionFinder.process_frames_emotion(image_with_landmarks)
    # image_with_emotion = image_with_landmarks
    
    # video_processor.save_processed_frame(image_with_emotion)
    video_processor.save_processed_frame_2(image_with_emotion, plot_image)
    
    # video_processor.save_processed_frame(image_with_emotion)

    _, jpeg_image = cv2.imencode('.jpg', image_with_emotion)

    jpeg_image_data = jpeg_image.tobytes()

    # Encode the JPEG image data as base64
    base64_image_data = base64.b64encode(jpeg_image_data).decode('utf-8')

    # Create a response with the base64-encoded image data
    response = jsonify(image_data=base64_image_data)

    logger.info("Done.")

    return response


@app.route('/get_form')
def get_form():
    form_id = app_properties.active_form_id
    form_data = forms.get(form_id)
    return jsonify(form_data)



@app.route('/generate_page', methods=['POST'])
def generate_page():
    
    data = request.get_json()
    
    window_width = int(data['window_width'])
    display_processor.set_window_width(window_width)
    window_height = int(data['window_height'])
    display_processor.set_window_height(window_height)
    
    
    # gaze = display_processor.get_point()
    
    display_processor.update_counter()

    # Generate random coordinates within the window size
    # x = random.randint(0, window_width)
    # y = random.randint(0, window_height)
    
    # Generate a white page with a red dot at the random coordinates
    image = np.ones((window_height, window_width, 3), dtype=np.uint8) * 255
    cv2.circle(image, (gaze[0], gaze[1]), 5, (0, 0, 255), -1)

    # Convert the image to JPEG format
    _, jpeg_image = cv2.imencode('.jpg', image)
    jpeg_image_data = jpeg_image.tobytes()
    base64_image_data = base64.b64encode(jpeg_image_data).decode('utf-8')

    response = jsonify(image_data=base64_image_data)

    return response

@app.route("/stroop")
def stroop():
    return render_template("stroop.html")

@app.route("/userId")
def getCurrUserID():
    user_id = data_set.get_curr_user_id()  # Assuming `data_set` is defined and returns the current user ID
    return jsonify({'userId': user_id})

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
    # configure_logging()  # Call the logging configuration function
    # app.run(debug=False)



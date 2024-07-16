import cv2
import os
import Util as util
from landmark_extraction import LandmarkFinder
from gaze_extraction import GazeDirectionFinder
from properties.ApplicationProperties import ApplicationProperties


class VideoProcessor:
    def __init__(self, video_stream):
        self.app_properties = ApplicationProperties()
        self.video_stream = video_stream
        # Folder path to save the frames
        self.frame_save_path = self.app_properties.frame_save_path
        self.frame_count = 0
        self.subjectID = 0
    
    def get_frame_count(self):
        return self.frame_count
        
    def circle_image(self, frame, landmarks):
        output_frame = LandmarkFinder.circle_specific_landmarks(frame, landmarks)
        return output_frame
    
    def process_frame(self, frame):
        # print('here')
        landmarks = LandmarkFinder.extract_landmarks(frame)
        detection_result = LandmarkFinder.detection(frame)
        
        anotated_image = LandmarkFinder.draw_landmarks_on_image(frame, detection_result)
        gazeDirection_frame = GazeDirectionFinder.extract_directon(anotated_image)
        print('here')
        
        # return landmarks, self.circle_image(gazeDirection_frame, landmarks)
        return landmarks, gazeDirection_frame
        
    
    
    def generate_frames(self):
        frame_count = 0
        while True:
            success, frame = self.video_stream.read()
            if not success:
                break
            print('shimbalaloot')
            processed_frame = self.process_frame(frame)
            
            # Convert the frame to JPEG format
            ret, buffer = cv2.imencode('.jpg', processed_frame)
            frame = buffer.tobytes()

            # Yield the frame as a response to the client
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

            frame_count += 1


    def save_frame(self, frame_data):
        # Create the directory if it doesn't exist
        os.makedirs(self.frame_save_path, exist_ok=True)
        filename = f'{self.subjectID}_frame_{self.frame_count}.jpg'
        file_path = os.path.join(self.frame_save_path, filename)
        util.save_base64_image(frame_data, file_path)
        self.frame_count = self.frame_count + 1
        saved_image = cv2.imread(file_path)
        return saved_image, frame_data
    
    def save_processed_frame(self, image):
        # Create the directory if it doesn't exist
        os.makedirs(self.frame_save_path+'/processed', exist_ok=True)
        filename = f'{self.subjectID}_frame_{self.frame_count-1}.jpg'
        file_path = os.path.join(self.frame_save_path+'/processed', filename)
        print("filePATHH")
        print(file_path)
        cv2.imwrite(file_path, image)
        return image
    
    def save_processed_frame_2(self, face_image, plot_image):
        # Create the directory if it doesn't exist
        os.makedirs(self.frame_save_path+'/processed', exist_ok=True)
        face_filename = f'{self.subjectID}_face_frame_{self.frame_count-1}.jpg'
        plot_filename = f'{self.subjectID}_plot_frame_{self.frame_count-1}.jpg'
        face_file_path = os.path.join(self.frame_save_path+'/processed', face_filename)
        plot_file_path = os.path.join(self.frame_save_path+'/processed', plot_filename)

        cv2.imwrite(face_file_path, face_image)
        cv2.imwrite(plot_file_path, plot_image)

        return face_image, plot_image
        
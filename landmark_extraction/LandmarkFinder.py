from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
import matplotlib.pyplot as plt
import cv2
from PIL import Image

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


landmarks_number = {
    'left_eye_border': [33, 246, 161, 160, 159, 158, 157, 173, 133, 155, 154, 153, 145, 144, 163, 7],
    'right_eye_border': [362, 398, 384, 385, 386, 387, 388, 466, 263, 249, 390, 373, 374, 380, 381, 382],
    'face_grid': [10, 338, 297, 332, 284, 251, 389, 356, 454, 366, 361, 288, 397, 365, 379, 378, 400, 377, 152, 148, 176, 149, 150, 136, 172, 58, 132, 93, 234, 127, 162, 21, 54, 103, 67, 109],
    'right_pupil': [473, 474, 475, 476, 477],
    'left_pupil': [468, 469, 470, 471, 472]
}
def get_specific_landmarks(rgb_image, detection_result, selected_indexes):
  face_landmarks_list = detection_result.face_landmarks
  annotated_image = np.copy(rgb_image)
  x, y = rgb_image.shape[0], rgb_image.shape[1]
  face_landmarks = face_landmarks_list[0]
  selected_face_landmarks = []
  
  for i in selected_indexes:
    list = face_landmarks[i]
    X = int(np.ceil(y*(list.x)))
    Y = int(np.ceil(x*(list.y)))
    pair = (X, Y)
    selected_face_landmarks.append(pair)
  return selected_face_landmarks

def circle_specific_landmarks(img, landmarks, left_eye_border = True, right_eye_border = True, face_grid = True, right_pupil = True, left_pupil = True):
  target_categories = []
  if (left_eye_border):
    target_categories.append('left_eye_border')
  if (left_eye_border):
    target_categories.append('right_eye_border')
  if (left_eye_border):
    target_categories.append('face_grid')
  if (left_eye_border):
    target_categories.append('right_pupil')
  if (left_eye_border):
    target_categories.append('left_pupil')
    
  for mark in landmarks:
    if mark['name'] in target_categories:
      landmark_points = mark['landmarks']
      for pair in landmark_points:
        img = cv2.circle(img, (pair[0], pair[1]), radius=0, color=(0, 0, 255), thickness=2)
      
  return img

def circle_specific_landmarks_by_index(rgb_image, detection_result, selected_indexes, img):
  selected_face_landmarks = get_specific_landmarks(rgb_image, detection_result, selected_indexes)
  x, y = rgb_image.shape[0], rgb_image.shape[1]
  
  i = 1
  for landmark in selected_face_landmarks:
    X = int(np.ceil(y*(landmark.x)))
    Y = int(np.ceil(x*(landmark.y)))
    img = cv2.circle(img, (X, Y), radius=0, color=(0, 0, 255), thickness=20)
    img = cv2.putText(img, str(i), (X, Y), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)
    i+=1

  return img


def plot_face_blendshapes_bar_graph(face_blendshapes):
  # Extract the face blendshapes category names and scores.
  face_blendshapes_names = [face_blendshapes_category.category_name for face_blendshapes_category in face_blendshapes]
  face_blendshapes_scores = [face_blendshapes_category.score for face_blendshapes_category in face_blendshapes]
  # The blendshapes are ordered in decreasing score value.
  face_blendshapes_ranks = range(len(face_blendshapes_names))

  fig, ax = plt.subplots(figsize=(12, 12))
  bar = ax.barh(face_blendshapes_ranks, face_blendshapes_scores, label=[str(x) for x in face_blendshapes_ranks])
  ax.set_yticks(face_blendshapes_ranks, face_blendshapes_names)
  ax.invert_yaxis()

  # Label each bar with values
  for score, patch in zip(face_blendshapes_scores, bar.patches):
    plt.text(patch.get_x() + patch.get_width(), patch.get_y(), f"{score:.4f}", va="top")

  ax.set_xlabel('Score')
  ax.set_title("Face Blendshapes")
  plt.tight_layout()
  plt.show()

def draw_landmarks_on_image(rgb_image, detection_result):
  face_landmarks_list = detection_result.face_landmarks
  annotated_image = np.copy(rgb_image)

  # Loop through the detected faces to visualize.
  for idx in range(len(face_landmarks_list)):
    face_landmarks = face_landmarks_list[idx]
    # print(face_landmarks)
    # face_landmarks = face_landmarks[1:3]
    # Draw the face landmarks.


    face_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
    face_landmarks_proto.landmark.extend([
      landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in face_landmarks
    ])

    solutions.drawing_utils.draw_landmarks(
        image=annotated_image,
        landmark_list=face_landmarks_proto,
        connections=mp.solutions.face_mesh.FACEMESH_TESSELATION,
        landmark_drawing_spec=None,
        connection_drawing_spec=mp.solutions.drawing_styles
        .get_default_face_mesh_tesselation_style())
    solutions.drawing_utils.draw_landmarks(
        image=annotated_image,
        landmark_list=face_landmarks_proto,
        connections=mp.solutions.face_mesh.FACEMESH_CONTOURS,
        landmark_drawing_spec=None,
        connection_drawing_spec=mp.solutions.drawing_styles
        .get_default_face_mesh_contours_style())
    solutions.drawing_utils.draw_landmarks(
        image=annotated_image,
        landmark_list=face_landmarks_proto,
        connections=mp.solutions.face_mesh.FACEMESH_IRISES,
          landmark_drawing_spec=None,
          connection_drawing_spec=mp.solutions.drawing_styles
          .get_default_face_mesh_iris_connections_style())

  return annotated_image

def detection(raw_frame):
  base_options = python.BaseOptions(model_asset_path='face_landmarker_v2_with_blendshapes.task')
  options = vision.FaceLandmarkerOptions(base_options=base_options,
                                        output_face_blendshapes=True,
                                        output_facial_transformation_matrixes=True,
                                        num_faces=1)
  detector = vision.FaceLandmarker.create_from_options(options) 
  # print('there')
  frame = mp.Image(image_format=mp.ImageFormat.SRGB, data=raw_frame)
  # print(frame)
  detection_result = detector.detect(frame)
  return detection_result

def extract_landmarks(frame):
  detection_result = detection(frame)

  landmarks = []
  left_eye_border_landmarks = {'name': 'left_eye_border', 'landmarks': get_specific_landmarks(frame, detection_result, landmarks_number['left_eye_border'])}
  right_eye_border_landmarks = {'name': 'right_eye_border', 'landmarks': get_specific_landmarks(frame, detection_result, landmarks_number['right_eye_border'])}
  face_grid_landmarks = {'name': 'face_grid', 'landmarks': get_specific_landmarks(frame, detection_result, landmarks_number['face_grid'])}
  right_pupil_landmarks = {'name': 'right_pupil', 'landmarks': get_specific_landmarks(frame, detection_result, landmarks_number['right_pupil'])}
  left_pupil_landmarks = {'name': 'left_pupil', 'landmarks': get_specific_landmarks(frame, detection_result, landmarks_number['left_pupil'])}
  
  #TODO get monitor size and add it too landmarks 
  monitor_size = {}
  landmarks.extend([left_eye_border_landmarks, right_eye_border_landmarks, face_grid_landmarks, right_pupil_landmarks, left_pupil_landmarks])

  return landmarks
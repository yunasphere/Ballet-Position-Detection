"""
Used to process the reference pictures of the ballet positions,
detecting landmarks in them.
"""

import mediapipe as mp
import cv2
import numpy as np
import Compare as comp

from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.vision import drawing_utils
from mediapipe.tasks.python.vision import drawing_styles
from pathlib import Path


#Model for limb ('landmark') detection
#model_path = '/Users/oscar/Documents/Github/Ballet/Ballet-Position-Detection/pose_landmarker_full.task'
model_path = str(Path(__file__).parent)
model_path += '/pose_landmarker_full.task'


#PoseLandmarker (IMAGE)
BaseOptions = mp.tasks.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode


options = PoseLandmarkerOptions(
    base_options = BaseOptions(model_asset_path = model_path),
    running_mode = VisionRunningMode.IMAGE)


def draw_landmarks_on_image(image, detection_result):
  pose_landmarks_list = detection_result.pose_landmarks
  annotated_image = np.copy(image)

  pose_landmark_style = drawing_styles.get_default_pose_landmarks_style()
  pose_connection_style = drawing_utils.DrawingSpec(color=(0, 255, 0), thickness=2)

  for pose_landmarks in pose_landmarks_list:
    drawing_utils.draw_landmarks(
        image=annotated_image,
        landmark_list=pose_landmarks,
        connections=vision.PoseLandmarksConnections.POSE_LANDMARKS,
        landmark_drawing_spec=pose_landmark_style,
        connection_drawing_spec=pose_connection_style)

  return annotated_image


detector = vision.PoseLandmarker.create_from_options(options)

#Image needs to be an mp image in BGR foRmat

#IGNORE: testing thing :)
#bgr_img = cv2.imread("/Users/oscar/Documents/DigiCam/PICT0854.JPG")
#image = mp.Image(image_format=mp.ImageFormat.SRGB, data=bgr_img)
#detection_result = detector.detect(image)
#annotated_image = draw_landmarks_on_image(image.numpy_view(), detection_result)

#Display annotated image
#cv2.imshow('', cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR))
#cv2.waitKey(0)


def landmark_image(input_image):
    image = mp.Image(image_format=mp.ImageFormat.SRGB, data=input_image)
    detection_result = detector.detect(image)
    annotated_image = draw_landmarks_on_image(image.numpy_view(), detection_result)

    return annotated_image


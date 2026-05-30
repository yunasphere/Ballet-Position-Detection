import mediapipe as mp
import cv2
import numpy as np

from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.vision import drawing_utils
from mediapipe.tasks.python.vision import drawing_styles

#Model for limb ('landmark') detection
model_path = '/Users/oscar/Documents/Ballet/pose_landmarker_full.task'

#PoseLandmarker
BaseOptions = mp.tasks.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
PoseLandmarkerResult = mp.tasks.vision.PoseLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode


RESULT = None
#Print pose info 
def print_result(result: PoseLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
    global RESULT
    RESULT = result
    

options = PoseLandmarkerOptions(
    base_options = BaseOptions(model_asset_path = model_path),
    running_mode = VisionRunningMode.LIVE_STREAM,
    result_callback = print_result)



#Draw lines on body 
def drawLandmarksOnScreen(image, detection_result):
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


#Initialise live feed camera
cap = cv2.VideoCapture(0)
start_time = cv2.getTickCount()
with PoseLandmarker.create_from_options(options) as landmarker:
    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            print("Ignoring empty frame")
            break

        frame_timestamp_ms = int((cv2.getTickCount() - start_time) * 1000 / cv2.getTickFrequency())
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        landmarker.detect_async(mp_image, frame_timestamp_ms)

        if type(RESULT) is not type(None):
            annotated_frame = drawLandmarksOnScreen(frame, RESULT)
            cv2.imshow('Ballet Detection', annotated_frame)
        else:
            cv2.imshow('Ballet Detection', frame)

        if cv2.waitKey(1) == ord('q'):
            break


    cap.release()
    cv2.destroyAllWindows()




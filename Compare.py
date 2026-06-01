"""
File for processing video frames, comparing them to library and determining
which (if any) ballet position is being detected.
"""

import mediapipe as mp
import cv2
import numpy as np

from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.vision import drawing_utils
from mediapipe.tasks.python.vision import drawing_styles

def DeterminePose(frame):
    print ("TODO: Compare feed frame to library of poses")


#Calculate rotation difference in 2 landmarks
def RotationDiff():



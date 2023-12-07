import numpy as np
import utils.constant

from utils.constant import LEFT_HIP
from utils.constant import LEFT_KNEE
from utils.constant import LEFT_ANKLE
from utils.constant import RIGHT_HIP
from utils.constant import RIGHT_KNEE
from utils.constant import RIGHT_ANKLE

class Result:
    def __init__(self):
        self.left_angle = 0.0
        self.right_angle = 0.0

def calculate_angle(a, b, c):
    a = np.array(a)  # First
    b = np.array(b)  # Mid
    c = np.array(c)  # End

    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - \
        np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)

    if angle > 180.0:
        angle = 360-angle

    return angle


def count_squat(imlist):
    
    result = Result()
    if len(imlist) != 0:
        left_hip = [imlist[LEFT_HIP][1],
                    imlist[LEFT_HIP][2]]
        left_knee = [imlist[LEFT_KNEE][1],
                        imlist[LEFT_KNEE][2]]
        left_ankle = [imlist[LEFT_ANKLE][1],
                        imlist[LEFT_ANKLE][2]]
        right_hip = [imlist[RIGHT_HIP][1],
                        imlist[RIGHT_HIP][2]]
        right_knee = [imlist[RIGHT_KNEE][1],
                        imlist[RIGHT_KNEE][2]]
        right_ankle = [imlist[RIGHT_ANKLE][1],
                        imlist[LEFT_ANKLE][2]]

        result.left_angle = calculate_angle(left_hip, left_knee, left_ankle)
        result.right_angle = calculate_angle(right_hip, right_knee, right_ankle)

        return result
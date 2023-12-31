import numpy as np
import utils.constant

from utils.constant import LEFT_HIP
from utils.constant import LEFT_KNEE
from utils.constant import LEFT_ANKLE
from utils.constant import RIGHT_HIP
from utils.constant import RIGHT_KNEE
from utils.constant import RIGHT_ANKLE
from utils.constant import RIGHT_SHOULDER
from utils.constant import LEFT_SHOULDER


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

def check_visibility(left, right):
    left_v = True
    right_v = True
    for x in left:
        if x < 0.8:
            left_v = False
    
    for x in right:
        if x < 0.8:
            right_v = False

    return left_v or right_v


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
                       imlist[RIGHT_ANKLE][2]]
        mid_shoulder = [(imlist[RIGHT_SHOULDER][1]+imlist[LEFT_SHOULDER][1])/2,
                        (imlist[RIGHT_SHOULDER][2]+imlist[LEFT_SHOULDER][2])/2]
        vert_shoulder = [(imlist[RIGHT_SHOULDER][1]+imlist[LEFT_SHOULDER][1])/2,
                         0]
        mid_hip = [(imlist[RIGHT_HIP][1]+imlist[LEFT_HIP][1])/2,
                   (imlist[RIGHT_HIP][2]+imlist[LEFT_HIP][2])/2]

        result.left_angle = calculate_angle(left_hip, left_knee, left_ankle)
        result.right_angle = calculate_angle(
            right_hip, right_knee, right_ankle)
        result.back_angle = calculate_angle(
            mid_hip, vert_shoulder, mid_shoulder)
        
        visibility_left = [imlist[LEFT_HIP][3], imlist[LEFT_KNEE][3], imlist[LEFT_ANKLE][3], imlist[LEFT_SHOULDER][3]]
        visibility_right = [imlist[RIGHT_HIP][3], imlist[RIGHT_KNEE][3], imlist[RIGHT_ANKLE][3], imlist[RIGHT_SHOULDER][3]]
        
        
        result.visibility = check_visibility(visibility_left, visibility_right)

        return result

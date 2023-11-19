import cv2
import mediapipe as mp
import numpy as np
import constant
        
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
    if len(imlist) != 0:
        left_hip = [imlist[constant.LEFT_HIP][1],
            imlist[constant.LEFT_HIP][2]]
        left_knee = [imlist[constant.LEFT_KNEE][1],
                        imlist[constant.LEFT_KNEE][2]]
        left_ankle = [imlist[constant.LEFT_ANKLE][1],
                        imlist[constant.LEFT_ANKLE][2]]
        
        left_angle = calculate_angle(left_hip, left_knee, left_ankle)
        
        return left_angle
import cv2
import mediapipe as md
import time
import math
import moviepy.video.fx.all as vfx
import constant
from moviepy.editor import VideoFileClip

from constant import RIGHT_SHOULDER
from constant import RIGHT_ELBOW
from constant import RIGHT_WRIST
from constant import RIGHT_HIP
from constant import RIGHT_KNEE
from constant import RIGHT_ANKLE
from constant import LEFT_SHOULDER
from constant import LEFT_ELBOW
from constant import LEFT_WRIST
from constant import LEFT_HIP
from constant import LEFT_KNEE
from constant import LEFT_ANKLE


def getAngle(a, b, c):
    ang = math.degrees(math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
    return ang + 360 if ang < 0 else ang

def create_imlist(path):
    md_pose = md.solutions.pose 

    count = 0
    position = None 

    cap = cv2.VideoCapture(path)
    imlist = []
    # debug
    num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    start_time = time.time()

    with md_pose.Pose(
        min_detection_confidence = 0.7,
        min_tracking_confidence = 0.7
    ) as pose:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print('Video not found or ended')
                break
            
            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
            result = pose.process(image)
            
            # imlist = []

            if result.pose_landmarks:
                for id, lm in enumerate(result.pose_landmarks.landmark):
                    h, w, _ = image.shape
                    # X, Y = int(lm.x * w), int(lm.y * h)
                    imlist.append([id, lm.x, lm.y])
    return imlist


def count_pushup_angle(path):
    md_pose = md.solutions.pose 

    count = 0
    position = None 

    cap = cv2.VideoCapture(path)
    angle = []
    # debug
    num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    start_time = time.time()

    with md_pose.Pose(
        min_detection_confidence = 0.7,
        min_tracking_confidence = 0.7
    ) as pose:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print('Video not found or ended')
                break
            
            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
            result = pose.process(image)
            
            imlist = []

            if result.pose_landmarks:
                for id, lm in enumerate(result.pose_landmarks.landmark):
                    h, w, _ = image.shape
                    X, Y = int(lm.x * w), int(lm.y * h)
                    imlist.append([id, X, Y])
            if len(imlist) == 0:
                print("em")
            if len(imlist) != 0:
                angle_SEW_left =  getAngle((imlist[LEFT_SHOULDER][1], imlist[LEFT_SHOULDER][2]),
                                        (imlist[LEFT_ELBOW][1],imlist[LEFT_ELBOW][2]),
                                        (imlist[LEFT_WRIST][1],imlist[LEFT_WRIST][2]))
                angle_SEW_right =  getAngle((imlist[RIGHT_SHOULDER][1], imlist[RIGHT_SHOULDER][2]),
                                        (imlist[RIGHT_ELBOW][1],imlist[RIGHT_ELBOW][2]),
                                        (imlist[RIGHT_WRIST][1],imlist[RIGHT_WRIST][2]))
                angle_SHK_left = getAngle((imlist[LEFT_SHOULDER][1], imlist[LEFT_SHOULDER][2]),
                                        (imlist[LEFT_HIP][1],imlist[LEFT_HIP][2]),
                                        (imlist[LEFT_KNEE][1],imlist[LEFT_KNEE][2]))
                angle_SHK_right = getAngle((imlist[RIGHT_SHOULDER][1], imlist[RIGHT_SHOULDER][2]),
                                        (imlist[RIGHT_HIP][1],imlist[RIGHT_HIP][2]),
                                        (imlist[RIGHT_KNEE][1],imlist[RIGHT_KNEE][2]))
                angle_HKA_left = getAngle((imlist[LEFT_HIP][1], imlist[LEFT_HIP][2]),
                                        (imlist[LEFT_KNEE][1],imlist[LEFT_KNEE][2]),
                                        (imlist[LEFT_ANKLE][1],imlist[LEFT_ANKLE][2]))
                angle_HKA_right = getAngle((imlist[RIGHT_HIP][1], imlist[RIGHT_HIP][2]),
                                        (imlist[RIGHT_KNEE][1],imlist[RIGHT_KNEE][2]),
                                        (imlist[RIGHT_ANKLE][1],imlist[RIGHT_ANKLE][2]))
                if (angle_SEW_right >= 180 and angle_SEW_left >= 180) :
                    angle_SEW_left = 360 - getAngle((imlist[LEFT_SHOULDER][1], imlist[LEFT_SHOULDER][2]),
                                        (imlist[LEFT_ELBOW][1],imlist[LEFT_ELBOW][2]),
                                        (imlist[LEFT_WRIST][1],imlist[LEFT_WRIST][2]))
                    angle_SEW_right = 360 -  getAngle((imlist[RIGHT_SHOULDER][1], imlist[RIGHT_SHOULDER][2]),
                                        (imlist[RIGHT_ELBOW][1],imlist[RIGHT_ELBOW][2]),
                                        (imlist[RIGHT_WRIST][1],imlist[RIGHT_WRIST][2]))
                    angle_SHK_left = 360 - getAngle((imlist[LEFT_SHOULDER][1], imlist[LEFT_SHOULDER][2]),
                                        (imlist[LEFT_HIP][1],imlist[LEFT_HIP][2]),
                                        (imlist[LEFT_KNEE][1],imlist[LEFT_KNEE][2]))
                    angle_SHK_right = 360 - getAngle((imlist[RIGHT_SHOULDER][1], imlist[RIGHT_SHOULDER][2]),
                                            (imlist[RIGHT_HIP][1],imlist[RIGHT_HIP][2]),
                                            (imlist[RIGHT_KNEE][1],imlist[RIGHT_KNEE][2]))
                    angle_HKA_left = 360 - getAngle((imlist[LEFT_HIP][1], imlist[LEFT_HIP][2]),
                                            (imlist[LEFT_KNEE][1],imlist[LEFT_KNEE][2]),
                                            (imlist[LEFT_ANKLE][1],imlist[LEFT_ANKLE][2]))
                    angle_HKA_right = 360 - getAngle((imlist[RIGHT_HIP][1], imlist[RIGHT_HIP][2]),
                                            (imlist[RIGHT_KNEE][1],imlist[RIGHT_KNEE][2]),
                                            (imlist[RIGHT_ANKLE][1],imlist[RIGHT_ANKLE][2]))
                # angle_SEW_left =  getAngle((imlist[LEFT_SHOULDER][1], imlist[LEFT_SHOULDER][2]),
                #                         (imlist[LEFT_ELBOW][1],imlist[LEFT_ELBOW][2]),
                #                         (imlist[LEFT_WRIST][1],imlist[LEFT_WRIST][2]))
                # angle_SEW_right =  getAngle((imlist[RIGHT_SHOULDER][1], imlist[RIGHT_SHOULDER][2]),
                #                         (imlist[RIGHT_ELBOW][1],imlist[RIGHT_ELBOW][2]),
                #                         (imlist[RIGHT_WRIST][1],imlist[RIGHT_WRIST][2]))
                # angle_SHK_left = getAngle((imlist[LEFT_SHOULDER][1], imlist[LEFT_SHOULDER][2]),
                #                         (imlist[LEFT_HIP][1],imlist[LEFT_HIP][2]),
                #                         (imlist[LEFT_KNEE][1],imlist[LEFT_KNEE][2]))
                # angle_SHK_right = getAngle((imlist[RIGHT_SHOULDER][1], imlist[RIGHT_SHOULDER][2]),
                #                         (imlist[RIGHT_HIP][1],imlist[RIGHT_HIP][2]),
                #                         (imlist[RIGHT_KNEE][1],imlist[RIGHT_KNEE][2]))
                # angle_HKA_left = getAngle((imlist[LEFT_HIP][1], imlist[LEFT_HIP][2]),
                #                         (imlist[LEFT_KNEE][1],imlist[LEFT_KNEE][2]),
                #                         (imlist[LEFT_ANKLE][1],imlist[LEFT_ANKLE][2]))
                # angle_HKA_right = getAngle((imlist[RIGHT_HIP][1], imlist[RIGHT_HIP][2]),
                #                         (imlist[RIGHT_KNEE][1],imlist[RIGHT_KNEE][2]),
                #                         (imlist[RIGHT_ANKLE][1],imlist[RIGHT_ANKLE][2]))
                # angle.append(angle_left)
                # if ((angle_right) <= constant.ANGLE_RIGHT
                # and (angle_left) <= constant.ANGLE_LEFT):
                #     position = "down"
                print(angle_SEW_left)
                print(angle_SEW_right)
                if  ((angle_SEW_left) <= constant.SEW_THRESHOLD and (angle_SEW_right) <= constant.SEW_THRESHOLD and
                    ((angle_SHK_left) >= constant.SHK_THRESHOLD and (angle_SHK_right) >= constant.SHK_THRESHOLD) and 
                    ((angle_HKA_left) >= constant.HKA_THRESHOLD and (angle_HKA_right) >= constant.HKA_THRESHOLD) ):
                    # print(angle_SEW_left)
                    position = "down"  
                if (((angle_SEW_left) >= constant.SEW_THRESHOLD and (angle_SEW_right) >= constant.SEW_THRESHOLD) and
                    ((angle_SHK_left) >= constant.SHK_THRESHOLD and (angle_SHK_right) >= constant.SHK_THRESHOLD) and
                    ((angle_HKA_left) >= constant.HKA_THRESHOLD and (angle_HKA_right) >= constant.HKA_THRESHOLD) and position == "down"):
                    position = "up"
                    count +=1 
                    print(count) 
    return count
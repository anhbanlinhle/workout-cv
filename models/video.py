import cv2
import mediapipe as md
import utils.constant

from utils.drawing import draw_landmarks
from models.pushup import count_push_up
from models.squat import count_squat
import utils.constant

from utils.constant import SEW_THRESHOLD
from utils.constant import SHK_THRESHOLD
from utils.constant import HKA_THRESHOLD

def process_video(path, algorithm):
    md_pose = md.solutions.pose 

    count = 0
    position = None 

    cap = cv2.VideoCapture(path)

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
                draw_landmarks(
                    md_pose,
                    image,
                    result.pose_landmarks,
                    [11, 12, 13, 14, 15, 16, 23, 24, 25, 26, 27, 28],
                    imlist
                )

            if len(imlist) != 0:
                if algorithm == "pushup":
                    angle = count_push_up(imlist)
                    if  ((angle[0]) <= SEW_THRESHOLD and (angle[1]) <= SEW_THRESHOLD and
                        ((angle[2]) >= SHK_THRESHOLD and (angle[3]) >= SHK_THRESHOLD) and 
                        ((angle[4]) >= HKA_THRESHOLD and (angle[5]) >= HKA_THRESHOLD) ):
                        position = "down"  
                    if (((angle[0]) >= SEW_THRESHOLD and (angle[1]) >= SEW_THRESHOLD) and
                        ((angle[2]) >= SHK_THRESHOLD and (angle[3]) >= SHK_THRESHOLD) and
                        ((angle[4]) >= HKA_THRESHOLD and (angle[5]) >= HKA_THRESHOLD) and position == "down"):
                        count +=1
                        position = "up"
                elif algorithm == "squat":
                    result = count_squat(imlist)
                    if(result.back_angle < 20):
                        if result.left_angle > 160 and result.right_angle > 160:
                            position = 'down'
                        if result.left_angle < 75 and result.right_angle < 75 and position == 'down':
                            count += 1
                            position = 'up'

    cap.release()
    cv2.destroyAllWindows()
    return count
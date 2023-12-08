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

def process_camera(path, algorithm):
    # load pose model from mediapipe
    md_pose = md.solutions.pose 

    count = 0
    position = None 

    # open video capture from camera
    cap = cv2.VideoCapture(path)

    # init pose instance with confidence threshold
    with md_pose.Pose(
        min_detection_confidence = 0.9,
        min_tracking_confidence = 0.9
    ) as pose:
        # process video frame by frame
        while cap.isOpened():
            success, image = cap.read()
            # exit if video not found or ended
            if not success:
                print('Video not found or ended')
                break
            
            # convert color and flip image
            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

            # get pose landmarks as result using mediapipe pose model
            result = pose.process(image)
            
            # init empty list to store landmarks
            imlist = []

            # draw landmarks on image
            if result.pose_landmarks:
                draw_landmarks(
                    md_pose,
                    image,
                    result.pose_landmarks,
                    # draw only necessary landmarks
                    [11, 12, 13, 14, 15, 16, 23, 24, 25, 26, 27, 28],
                    imlist
                )

            # process exercise algorithm if landmarks are detected
            if len(imlist) != 0:
                if algorithm == "pushup":
                    # count push up using push up algorithm
                    angle = count_push_up(imlist)
                    if(angle[7] and 150 < angle[6]):
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
                    # count squat using squat algorithm
                    result = count_squat(imlist)
                    if(result.back_angle < 20 and result.visibility):
                        if result.left_angle > 160 and result.right_angle > 160:
                            position = 'down'
                        if result.left_angle < 75 and result.right_angle < 75 and position == 'down':
                            count += 1
                            position = 'up'

            # display count on screen
            cv2.putText(image, f'Count: {count}', (10, 60), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 255, 255), 2)
            # show processed image on screen
            cv2.imshow('Workout Scanner', cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()
    return count
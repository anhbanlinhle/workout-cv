import cv2
import mediapipe as md
import constant
from drawing import draw_landmarks

def process_data(path):
    md_pose = md.solutions.pose 

    count = 0
    position = None 

    cap = cv2.VideoCapture(0)

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
                print(count)

            cv2.imshow('Workout Scanner', cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()
    return count
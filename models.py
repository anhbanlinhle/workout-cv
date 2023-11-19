import cv2
import mediapipe as md
import time

from moviepy.editor import VideoFileClip
import moviepy.video.fx.all as vfx
import constant

def process_data(path):
    md_pose = md.solutions.pose 

    count = 0
    position = None 

    # cap = cv2.VideoCapture(path)
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
                for id, lm in enumerate(result.pose_landmarks.landmark):
                    h, w, _ = image.shape
                    X, Y = int(lm.x * w), int(lm.y * h)
                    imlist.append([id, X, Y])

                md.solutions.drawing_utils.draw_landmarks(
                    image,
                    result.pose_landmarks,
                    md_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec = md.solutions.drawing_utils.DrawingSpec(
                        color=(0, 0, 0), 
                        thickness=4, 
                        circle_radius=5
                    ),
                    connection_drawing_spec = md.solutions.drawing_utils.DrawingSpec(
                        color=(255, 255, 255),
                        thickness=4
                    ),
                )

            if len(imlist) != 0:
                right = abs(imlist[constant.RIGHT_SHOULDER][2] - imlist[constant.RIGHT_ELBOW][2])
                left = abs(imlist[constant.LEFT_SHOULDER][2] - imlist[constant.LEFT_ELBOW][2])
                if ((left) >= constant.DOWN_HAND_THRESHOLD 
                and (right) >= constant.DOWN_HAND_THRESHOLD):
                    position = "down"
                if ((left) <= constant.UP_HAND_THRESHOLD 
                and (right) <= constant.UP_HAND_THRESHOLD) and position == "down":
                    position = "up"
                    count +=1 
                    print(count)

            cv2.imshow('Pose Landmarks', cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()
    return count


def speedup_video(old, new):
    clip = VideoFileClip(old)
    final = clip.fx(vfx.speedx, constant.SPEED_UP_THRESHOLD)
    final.write_videofile(new)
    return 
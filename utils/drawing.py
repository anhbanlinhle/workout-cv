import cv2
import mediapipe as md

def draw_landmarks(md_pose, image, landmarks, landmark_indices, imlist):
    for id, lm in enumerate(landmarks.landmark):
        h, w, _ = image.shape
        X, Y = int(lm.x * w), int(lm.y * h)
        imlist.append([id, X, Y, lm.visibility])

    for connection in md_pose.POSE_CONNECTIONS:
        start_landmark = connection[0]
        end_landmark = connection[1]

        if start_landmark in landmark_indices and end_landmark in landmark_indices:
            start_point = (int(landmarks.landmark[start_landmark].x * w), int(landmarks.landmark[start_landmark].y * h))
            end_point = (int(landmarks.landmark[end_landmark].x * w), int(landmarks.landmark[end_landmark].y * h))

            cv2.line(image, start_point, end_point, 
                color=(255, 255, 255), 
                thickness=4
            )

    for id in landmark_indices:
        lm = landmarks.landmark[id]
        h, w, _ = image.shape
        X, Y = int(lm.x * w), int(lm.y * h)

        cv2.circle(image, (X, Y), 
            radius = 5, 
            color = (0, 0, 0), 
            thickness = 4
        )
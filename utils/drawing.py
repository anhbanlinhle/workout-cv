import cv2
import mediapipe as md

def draw_landmarks(md_pose, image, landmarks, landmark_indices, imlist):
    # loop through each landmark
    for id, lm in enumerate(landmarks.landmark):
        # get height and width of result screen
        h, w, _ = image.shape
        # normalize landmark position to screen size
        X, Y = int(lm.x * w), int(lm.y * h)

        imlist.append([id, X, Y, lm.visibility])

    # loop through each connection in pose model
    for connection in md_pose.POSE_CONNECTIONS:
        # get start and end landmark
        start_landmark = connection[0]
        end_landmark = connection[1]

        # draw line between start and end landmark if both are detected
        if start_landmark in landmark_indices and end_landmark in landmark_indices:
            # get normalized x and y of start and end landmark
            start_point = (int(landmarks.landmark[start_landmark].x * w), int(landmarks.landmark[start_landmark].y * h))
            end_point = (int(landmarks.landmark[end_landmark].x * w), int(landmarks.landmark[end_landmark].y * h))

            # draw connection line
            cv2.line(image, start_point, end_point, 
                color=(255, 255, 255), 
                thickness=4
            )

    # loop through each landmark that needs to be highlighted
    for id in landmark_indices:
        # normalizing steps similar to above
        lm = landmarks.landmark[id]
        h, w, _ = image.shape
        X, Y = int(lm.x * w), int(lm.y * h)

        # draw circle on landmarks
        cv2.circle(image, (X, Y), 
            radius = 5, 
            color = (0, 0, 0), 
            thickness = 4
        )
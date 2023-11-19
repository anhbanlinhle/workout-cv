import cv2
import mediapipe as md
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
                draw_landmarks(
                    md_pose,
                    image,
                    result.pose_landmarks,
                    [11, 12, 13, 14, 15, 16, 23, 24, 25, 26, 27, 28],
                    imlist
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

def draw_landmarks(md_pose, image, landmarks, landmark_indices, imlist):
    # for id in landmark_indices:
    #     lm = landmarks.landmark[id]
    #     h, w, _ = image.shape
    #     X, Y = int(lm.x * w), int(lm.y * h)
    #     imlist.append([id, X, Y])
    for id, lm in enumerate(landmarks.landmark):
        h, w, _ = image.shape
        X, Y = int(lm.x * w), int(lm.y * h)
        imlist.append([id, X, Y])

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
import cv2
import numpy as np

import os

down_move_path = "./pushup/down_move"
no_move_path = "./pushup/no_move"
up_move_path = "./pushup/up_move"

down_move_files = os.listdir(down_move_path)
no_move_files = os.listdir(no_move_path)
up_move_files = os.listdir(up_move_path)

up_move_index = len(up_move_files)
no_move_index = len(no_move_files)
down_move_index = len(down_move_files)
# Capturing the video file 0 for videocam else you can provide the url
capture = cv2.VideoCapture("pushup.mp4")

# Reading the first frame
_, frame1 = capture.read()
# Convert to gray scale
prvs = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
# Create mask
hsv_mask = np.zeros_like(frame1)
# Make image saturation to a maximum value
hsv_mask[..., 1] = 255

# Till you scan the video
while True:
    # Capture another frame and convert to gray scale
    _, frame2 = capture.read()
    next = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    # Optical flow is now calculated
    flow = cv2.calcOpticalFlowFarneback(
        prvs, next, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    # Compute magnitude and angle of 2D vector
    mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
    # Set image hue value according to the angle of optical flow
    hsv_mask[..., 0] = ang * 180 / np.pi / 2
    # Set value as per the normalized magnitude of optical flow
    hsv_mask[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
    # Convert to rgb
    rgb_representation = cv2.cvtColor(hsv_mask, cv2.COLOR_HSV2BGR)

    cv2.imshow('frame2', rgb_representation)

    # Wait for the user to press a key
    kk = cv2.waitKey(0) & 0xFF

    # Press 'e' to exit the video
    if kk == ord('e'):
        break
    # Press 's' to save the video
    elif kk == ord('z'):
        cv2.imwrite('./pushup/up_move/up_move' + str(up_move_index) +
                    '.png', rgb_representation)
        up_move_index += 1

    elif kk == ord('x'):
        cv2.imwrite('./pushup/no_move/no_move' + str(no_move_index) +
                    '.png', rgb_representation)
        no_move_index += 1

    elif kk == ord('c'):
        cv2.imwrite('./pushup/down_move/down_move' + str(down_move_index) +
                    '.png', rgb_representation)
        down_move_index += 1

    prvs = next

capture.release()
cv2.destroyAllWindows()

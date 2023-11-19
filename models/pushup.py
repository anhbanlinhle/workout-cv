import numpy as np
import utils.constant
# from constant import RIGHT_SHOULDER
# from constant import RIGHT_ELBOW
# from constant import RIGHT_WRIST
# from constant import RIGHT_HIP
# from constant import RIGHT_KNEE
# from constant import RIGHT_ANKLE
# from constant import LEFT_SHOULDER
# from constant import LEFT_ELBOW
# from constant import LEFT_WRIST
# from constant import LEFT_HIP
# from constant import LEFT_KNEE
# from constant import LEFT_ANKLE
def getAngle(a, b, c):
    a = np.array(a)  # First
    b = np.array(b)  # Mid
    c = np.array(c)  # End

    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - \
        np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)

    if angle > 180.0:
        angle = 360-angle

    return angle

# SEW - Shoulder Elbow Wrist
# SHK - Shoulder Hip Knee
# HKA - Hip Knee Ankle
# angle[0] = SEW_left 
# angle[1] = SEW_right
# angle[2] = SHK_left
# angle[3] = SHK_right
# angle[4] = HKA_left
# angle[5] = HKA_right

def count_push_up(imlist):
    angle = []
    if len(imlist) != 0:
        SEW_left =  getAngle((imlist[LEFT_SHOULDER][1], imlist[LEFT_SHOULDER][2]),
                                        (imlist[LEFT_ELBOW][1],imlist[LEFT_ELBOW][2]),
                                        (imlist[LEFT_WRIST][1],imlist[LEFT_WRIST][2]))
        angle.append(SEW_left)
        SEW_right =  getAngle((imlist[RIGHT_SHOULDER][1], imlist[RIGHT_SHOULDER][2]),
                                        (imlist[RIGHT_ELBOW][1],imlist[RIGHT_ELBOW][2]),
                                        (imlist[RIGHT_WRIST][1],imlist[RIGHT_WRIST][2]))
        angle.append(SEW_right)
        SHK_left =  getAngle((imlist[LEFT_SHOULDER][1], imlist[LEFT_SHOULDER][2]),
                                        (imlist[LEFT_HIP][1],imlist[LEFT_HIP][2]),
                                        (imlist[LEFT_KNEE][1],imlist[LEFT_KNEE][2]))
        angle.append(SHK_left)
        SHK_right =  getAngle((imlist[RIGHT_SHOULDER][1], imlist[RIGHT_SHOULDER][2]),
                                        (imlist[RIGHT_HIP][1],imlist[RIGHT_HIP][2]),
                                        (imlist[RIGHT_KNEE][1],imlist[RIGHT_KNEE][2]))
        angle.append(SHK_right)
        HKA_left =  getAngle((imlist[LEFT_HIP][1], imlist[LEFT_HIP][2]),
                                        (imlist[LEFT_KNEE][1],imlist[LEFT_KNEE][2]),
                                        (imlist[LEFT_ANKLE][1],imlist[LEFT_ANKLE][2]))
        angle.append(HKA_left)
        HKA_right =  getAngle((imlist[RIGHT_HIP][1], imlist[RIGHT_HIP][2]),
                                        (imlist[RIGHT_KNEE][1],imlist[RIGHT_KNEE][2]),
                                        (imlist[RIGHT_ANKLE][1],imlist[RIGHT_ANKLE][2]))
        angle.append(HKA_right)
    return angle
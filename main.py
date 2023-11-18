from push_up import count_pushup_angle
from constant import RIGHT_SHOULDER
from constant import RIGHT_ELBOW
from constant import RIGHT_WRIST
from constant import LEFT_SHOULDER
from constant import LEFT_ELBOW
from constant import LEFT_WRIST


path = "data/cd5.mp4"
# imlist = create_imlist(path)
count = count_pushup_angle(path)
print(count)


import os
import datetime
import moviepy.video.fx.all as vfx

from moviepy.editor import VideoFileClip
from utils.constant import OPTIMIZE_THRESHOLD

def speedup_video(path):
    file_name = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    speedup = f"./test/{file_name}.mp4"
    os.makedirs(os.path.dirname(speedup), exist_ok=True)
    clip = VideoFileClip(path)
    final = clip.fx(vfx.speedx, OPTIMIZE_THRESHOLD)
    final.write_videofile(speedup)
    return speedup
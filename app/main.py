import argparse
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.camera import process_data

def main():
    parser = argparse.ArgumentParser(description='Pose Detection and Exercise Recognition')
    parser.add_argument('-I', '--input', choices=['video', 'camera'], required=True, help='Input source (video or camera)')
    parser.add_argument('-A', '--algorithm', choices=['squat', 'pushup'], required=True, help='Exercise recognition algorithm')
    parser.add_argument('-S', '--source', help='Absolute path to the video file (required if input is video)')

    args = parser.parse_args()

    if args.input == 'video':
        if args.source is None:
            parser.error('--source is required when input is video')
        video_path = args.source
    elif args.input == 'camera':
        video_path = 0

    if args.algorithm == 'squat':
        print(process_data(video_path, "squat"))
    elif args.algorithm == 'pushup':
        print(process_data(video_path, "pushup"))
    else:
        print('Invalid algorithm specified. Please choose "squat" or "pushup".')

if __name__ == "__main__":
    main()
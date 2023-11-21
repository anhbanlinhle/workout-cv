import argparse
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.camera import process_camera
from utils.optimizer import speedup_video

def main():
    parser = argparse.ArgumentParser(description='Pose Detection and Exercise Recognition')
    parser.add_argument('-I', '--input', choices=['video', 'camera'], required=True, help='Input source (video or camera)')
    parser.add_argument('-A', '--algorithm', choices=['squat', 'pushup'], required=True, help='Exercise recognition algorithm')
    parser.add_argument('-S', '--source', help='Absolute path to the video file (required if input is video)')
    parser.add_argument('-T', '--test', help='Absolute path to test data file')

    args = parser.parse_args()

    if args.algorithm not in ['squat', 'pushup']:
        print('Invalid algorithm specified. Please choose "squat" or "pushup".')

    if args.input == 'video':
        if args.source is None:
            parser.error('--source is required when input is video')
        print(process_camera(speedup_video(args.source), args.algorithm))
    elif args.input == 'camera':
        if args.test is None:
            print(process_camera(0, args.algorithm))
        else:
            print(process_camera(args.test, args.algorithm))

if __name__ == "__main__":
    main()
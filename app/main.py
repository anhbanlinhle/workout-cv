import argparse
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.camera import process_camera

def main():
    parser = argparse.ArgumentParser(description='Pose Detection and Exercise Recognition')
    parser.add_argument('-I', '--input', choices=['video', 'camera'], required=True, help='Input source (video or camera)')
    parser.add_argument('-A', '--algorithm', choices=['squat', 'pushup'], required=True, help='Exercise recognition algorithm')
    parser.add_argument('-S', '--source', help='Absolute path to the video file (required if input is video)')

    args = parser.parse_args()

    if args.algorithm not in ['squat', 'pushup']:
        print('Invalid algorithm specified. Please choose "squat" or "pushup".')

    if args.input == 'video':
        if args.source is None:
            parser.error('--source is required when input is video')
        print(process_camera(args.source, args.algorithm))
    elif args.input == 'camera':
        print(process_camera(0, args.algorithm))


if __name__ == "__main__":
    main()
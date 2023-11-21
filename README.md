# Pose Detection and Exercise Recognition

# Installation

```sh
git clone https://github.com/anhbanlinhle/workout-cv.git
```

```sh
pip install -r requirements.txt
```

# Usage

## Command

```sh
python3 app/main.py -I {video,camera} -A {squat,pushup} [-S SOURCE] [-T TEST]
```

## Options
```sh
  -I {video,camera}, --input {video,camera}
                        Input source (video or camera)
  -A {squat,pushup}, --algorithm {squat,pushup}
                        Exercise recognition algorithm
  -S SOURCE, --source SOURCE
                        Absolute path to the video file (required if input is video)
  -T TEST, --test TEST  Absolute path to test data file
```

## Example

To live process on camera

```sh
python3 app/main.py --input=camera --algorithm=exercise
```

To quick-process a pre-recorded video

```sh
python3 app/main.py --input=video --algorithm=exercise --source=/path/to/video
```

To live process a pre-recorded video

```sh
python3 app/main.py --input=camera --algorithm=exercise --test=/path/to/video
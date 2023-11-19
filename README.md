# Pose Detection and Exercise Recognition

# Installation

```sh
git clone https://github.com/anhbanlinhle/workout-cv.git
```

```sh
pip install -r requirements.txt
```

# Usage

```sh
python3 app/main.py -I {video,camera} -A {squat,pushup} [-S SOURCE]
```

- Options
```sh
  -I {video,camera}, --input {video,camera}
                        Input source (video or camera)
  -A {squat,pushup}, --algorithm {squat,pushup}
                        Exercise recognition algorithm
  -S SOURCE, --source SOURCE
                        Absolute path to the video file (required if input is video)
```
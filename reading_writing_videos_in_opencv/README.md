# README

## Directory Structure

**All the code files and folders follow the following structure.**

```
│   README.md
│
├───CPP
│   ├───video_read_from_file
│   │   │   CMakeLists.txt
│   │   │   video_read_from_file.cpp
│   │   │
│   │   └───Resources
│   │           Cars.mp4
│   │
│   ├───video_read_from_image_sequence
│   │   │   CMakeLists.txt
│   │   │   video_read_from_image_sequence.cpp
│   │   │
│   │   └───Resources
│   │       └───Image_Sequence
│   │
│   ├───video_read_from_webcam
│   │       CMakeLists.txt
│   │       video_read_from_webcam.cpp
│   │
│   ├───video_write_from_webcam
│   │       CMakeLists.txt
│   │       video_write_from_webcam.cpp
│   │
│   └───video_write_to_file
│       │   CMakeLists.txt
│       │   video_write_to_file.cpp
│       │
│       └───Resources
│               Cars.mp4
│
└───Python
    │   video_read_from_file.py
    │   video_read_from_image_sequence.py
    │   video_read_from_webcam.py
    │   video_write_from_webcam.py
    │   video_write_to_file.py
    │   requirements.txt
    │
    └───Resources
        │   Cars.mp4
        │
        └───Image_sequence
                
```



## Instructions

### Python

To run the code in Python, please go into the `Python` folder and execute the Python scripts in each of the respective sub-folders.

### C++

To run the code in C++, please go into the `CPP` folder, then go into each of the respective sub-folders and follow the steps below:

```
mkdir build
cd build
cmake ..
cmake --build . --config Release
cd ..
./build/video_read
```

```
mkdir build
cd build
cmake ..
cmake --build . --config Release
cd ..
./build/video_read_is
```

```
mkdir build
cd build
cmake ..
cmake --build . --config Release
cd ..
./build/video_read_wc
```

```
mkdir build
cd build
cmake ..
cmake --build . --config Release
cd ..
./build/video_write_wc
```

```
mkdir build
cd build
cmake ..
cmake --build . --config Release
cd ..
./build/video_write_wc
```



# AI Courses by OpenCV

Want to become an expert in AI? [AI Courses by OpenCV](https://opencv.org/courses/) is a great place to start.

![img](https://camo.githubusercontent.com/18c5719ef10afe9607af3e87e990068c942ae4cba8bd4d72d21950d6213ea97e/68747470733a2f2f7777772e6c6561726e6f70656e63762e636f6d2f77702d636f6e74656e742f75706c6f6164732f323032302f30342f41492d436f75727365732d42792d4f70656e43562d4769746875622e706e67)



## Last Run and Tested

Last successful run, March 22 2021.
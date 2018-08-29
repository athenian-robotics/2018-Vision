## 2018-Vision

**Vision system for FRC team 852.**
#### Dependencies
* OpenCV
* ROS
* CMake

**How to bulid and run on OSX/Linux**
1. Install dependencies
1. Create and `cd` to a `build` directory
1. Run `cmake .. && make` from the `build` directory
1. Execute `2018-Vision` in `build/bin` to run the cube detection/video streamer (Note that this assumes that you will be streaming to 10.8.52.8 on port 5802, these can be found near the top of 2018Vision.cpp, requires rebuild if changed)
1. Run `python3 viewer.py <stream-port>` to view the camera feed remotely on device with target IP

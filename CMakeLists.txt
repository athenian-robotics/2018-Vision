cmake_minimum_required(VERSION 3.5)
#if (UNIX)
#    set(CMAKE_CXX_FLAGS "-O3")
#endif ()
set(CMAKE_CXX_STANDARD 11)
project(arc2018vision)

find_package(OpenCV REQUIRED)

find_package(catkin REQUIRED COMPONENTS roscpp geometry_msgs std_msgs)
catkin_package()
include_directories(${OpenCV_INCLUDE_DIRS} ${catkin_INCLUDE_DIRS})

set(LIBS ${OpenCV_LIBS} ${catkin_LIBRARIES} -lavcodec -lavformat -lavutil -lswscale -lavfilter -lavutil -lavdevice)

set(VisionINCLUDE include/Streamer.h include/CubeRecog.h)
set(VisionSRC src/Streamer.cpp src/CubeRecog.cpp)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY bin)

add_executable(2018-Vision 2018Vision.cpp ${VisionSRC} ${VisionINCLUDE})
target_link_libraries(2018-Vision ${LIBS})

add_executable(FUK FUK.cpp)
target_link_libraries(FUK ${LIBS})
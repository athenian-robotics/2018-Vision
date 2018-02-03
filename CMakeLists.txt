cmake_minimum_required(VERSION 3.5)
#if (UNIX)
#    set(CMAKE_CXX_FLAGS "-O3")
#endif ()
set(CMAKE_CXX_STANDARD 11)
project(arc2018vision)

find_package(OpenCV REQUIRED)
include_directories(${OpenCV_INCLUDE_DIRS})

find_package(catkin REQUIRED COMPONENTS roscpp geometry_msgs)
catkin_package()
include_directories(include ${catkin_INCLUDE_DIRS})

set(RECOG src/CubeRecog.cpp src/CubeRecog.h)
set(NETWORK src/ImagePipe.cpp src/ImagePipe.h)
set(SRC main.cpp ${RECOG} ${NETWORK})

add_executable(2018-Vision ${SRC})
target_link_libraries(2018-Vision ${OpenCV_LIBS} ${catkin_LIBRARIES})

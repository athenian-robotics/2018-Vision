cmake_minimum_required(VERSION 3.5)
#if (UNIX)
#    set(CMAKE_CXX_FLAGS "-O3")
#endif ()
set(CMAKE_CXX_STANDARD 11)
project(arc2018vision)

find_package(OpenCV REQUIRED)

include_directories(${OpenCV_INCLUDE_DIRS})

set(Vision include/Streamer.h include/CubeRecog.h src/Streamer.cpp src/CubeRecog.cpp)
set(PracticalSock PracticalSocket.cpp PracticalSocket.h)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY bin)

add_executable(2018-Vision 2018Vision.cpp ${Vision} ${PracticalSock})
target_link_libraries(2018-Vision ${OpenCV_LIBS})
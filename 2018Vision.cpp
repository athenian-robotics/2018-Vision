#include <iostream>
#include <ctime>

#include "include/CubeRecog.h"
#include "include/Streamer.h"

int main(int argc, char *argv[]) {

    cv::VideoCapture cap(0);
    if (!cap.isOpened()) {
        std::cout << "HAVING A CAMERA MIGHT HELP" << std::endl;
        return -1;
    }
    cap.set(CV_CAP_PROP_FRAME_WIDTH, 640);
    cap.set(CV_CAP_PROP_FRAME_HEIGHT, 360);
    std::clock_t start;
    CubeRecog recog(640, 360);
    Streamer streamer("127.0.0.1", 10000);
    std::cout << "ENTERING LOOP" << std::endl;
    cv::Mat frame;
    for (;;) {
        start = std::clock();
        cap >> frame;
        streamer.sendFrame(frame);

        Point3d location = recog.get_cube_loc(frame);

        if (cv::waitKey(1) == 27)
            break;
    }

    cv::destroyAllWindows();
    cap.release();
}
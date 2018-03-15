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
    std::clock_t start;
    cv::Size frame_size = cv::Size(640, 360);
    //CubeRecog recog(640, 360);
    Streamer streamer("dracula.local", 9999);
    std::cout << "ENTERING LOOP" << std::endl;
    cv::Mat frame;
    int consecFail = 0;
    for (;;) {
        start = std::clock();
        cap >> frame;
        cv::resize(frame, frame, frame_size);
        streamer.sendFrame(frame) ? consecFail = 0 : consecFail++;
        if(consecFail == 5) {
            std::cout << "Streamer has failed 5 sends, closing" << std::endl;
            streamer.close();
        }

        //Point3d location = recog.get_cube_loc(frame);
        if (cv::waitKey(1) == 27)
            break;
    }


    cv::destroyAllWindows();
    cap.release();
}
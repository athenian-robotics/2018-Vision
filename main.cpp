#include <iostream>
#include <ctime>
#include "src/CubeRecog.h"





int main() {
    cv::VideoCapture cap(1);
    if (!cap.isOpened()) {
        std::cout << "BORK" << std::endl;
        return -1;
    }
    long frames = 0;
    std::time_t startTime = std::time(0);
    int tick = 0;


    CubeRecog recog(370, 640);
    printf("Ready\n");
    for (;;) {
        cv::Mat frame;
        cap >> frame;
        cv::Mat processed = recog.get_frame(frame);
        cv2::resizeWindow('Processed', 2400, 1200)
        cv::imshow("Image", frame);
        cv::imshow("Processed", processed);
        if (cv::waitKey(1) >= 0) break;
        ++frames;
        std::time_t now = std::time(0) -startTime;
        if(now - tick >=1){
            ++tick;
            std::cout << "FPS: " << frames << std::endl;
            frames = 0;
        }

    }

    cv::destroyAllWindows();
    cap.release();
}
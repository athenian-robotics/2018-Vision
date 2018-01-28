#include <iostream>
#include <ctime>
#include "CubeRecog.h"





int main() {
    cv::VideoCapture cap(0);
    if (!cap.isOpened()) {
        std::cout << "BORK" << std::endl;
        return -1;
    }

    CubeRecog recog(640, 360);
    printf("Ready\n");
    for (;;) {
        cv::Mat frame;
        cap >> frame;
        cv::Mat processed = recog.get_frame(frame);
        cv::imshow("Image", frame);
        cv::imshow("Processed", processed);
        if (cv::waitKey(1) >= 0) break;
    }

    cv::destroyAllWindows();
    cap.release();
}
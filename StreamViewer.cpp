#include <opencv2/core.hpp>
#include <opencv2/highgui.hpp>
#include "include/RemoteCamera.h"

int main() {
    cv::Mat frame;
    RemoteCamera cap(10000);
    for (;;) {
        frame = cap.grabFrame();
        if (frame.size().area() == 0){
            std::cout << "ERROR: empty frame" << std::endl;
            continue;
        }
        cv::imshow("Remote frame", frame);

        if (cv::waitKey(1) == 27)
            break;
    }
    cv::destroyAllWindows();
    cap.release();
}
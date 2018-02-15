#include <opencv2/opencv.hpp>
#include <fcntl.h>
#include <zconf.h>


int main(int argc, char **argv) {
    std::string fifo_file = "/tmp/img";
    std::cout << "Starting" << std::endl;
    int fifo_handle;

    cv::VideoCapture cap(1);
    cv::Mat frame;

    std::vector<uchar> buffer;
    std::vector<int> param(2);
    param[0] = cv::IMWRITE_JPEG_QUALITY;
    param[1] = 95; // default jpeg quality
    std::cout << "Entering loop" << std::endl;
    std::cout << cap.get(CV_CAP_PROP_FRAME_WIDTH) << ":" << cap.get(CV_CAP_PROP_FRAME_HEIGHT) << std::endl;
    for (;;) {

        if ((fifo_handle = open(fifo_file.c_str(), O_WRONLY)) < 0) {
            std::cerr << "FATAL ERROR: Failed to open fifo pipe, exiting" << std::endl;
            return -1;
        }
        cap >> frame;
        cv::imencode(".jpg", frame, buffer, param);
        if (write(fifo_handle, buffer.data(), buffer.size()) < 0) {
            std::cerr << "ERROR: Failed to write to pipe" << std::endl;
        }
        close(fifo_handle);
        cv::waitKey(1);
    }
}
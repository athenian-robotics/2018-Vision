#include <iostream>
#include <fcntl.h>
#include <zconf.h>
#include <vector>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/core/mat.hpp>

class PipeWriter {
public:
    explicit PipeWriter(char *pipe, char *enc_type = (char *)(".jpg"), std::vector<int> params = std::vector<int>(0));

    void writeImg(cv::Mat frame);

private:
    int fifo_handle;
    char *pipeName;
    char *enc_type;
    std::vector<uchar> buffer;
    std::vector<int> params;
};
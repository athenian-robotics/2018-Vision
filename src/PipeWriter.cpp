#include "PipeWriter.h"

PipeWriter::PipeWriter(char *pipe, char *enc_type, std::vector<int> params) {
    // Gonna assume that the pipeName exists, as it should be created by the reader
    this->pipeName = pipe;
    this->enc_type = enc_type;
    if (!params.empty()) {
        this->params = std::vector<int>(2);
        this->params[0] = 1; // This is the jpeg quality
        this->params[1] = 95; // This is the actual value to set the quality to
    } else {
        this->params = params;
    }
}

void PipeWriter::writeImg(cv::Mat frame) {
    if ((fifo_handle = open(this->pipeName, O_WRONLY)) < 0) {
        exit(-1);
    }
    cv::imencode(this->enc_type, frame, this->buffer, this->params);
    if (write(fifo_handle, buffer.data(), buffer.size()) < 0) {
        std::cerr << "ERROR FAILED TO WRITE TO PIPE" << std::endl;
        exit(-1);
    }
    close(fifo_handle);
}

//
// Created by jrmo on 3/12/18.
//

#include "../include/RemoteCamera.h"

RemoteCamera::RemoteCamera(unsigned short port) {
    this->sock = new UDPSocket(port);
}

cv::Mat RemoteCamera::grabFrame() {
    do {
        recvMsgSize = this->sock->recvFrom(buffer, BUF_LEN, srcAddr, srcPort);
    } while (recvMsgSize > sizeof(int));
    int total_pack = ((int *) buffer)[0];

    char *longBuf = new char[PACK_SIZE * total_pack];
    for (int i = 0; i < total_pack; ++i) {
        recvMsgSize = sock->recvFrom(buffer, BUF_LEN, srcAddr, srcPort);
        if (recvMsgSize != PACK_SIZE) {
            std::cerr << "Received unexpected sized packet: " << recvMsgSize << std::endl;
            continue;
        }
        memcpy(&longBuf[i * PACK_SIZE], buffer, PACK_SIZE);
    }
    cv::Mat rawData = cv::Mat(1, PACK_SIZE * total_pack, CV_8UC1, longBuf);
    cv::Mat frame = cv::imdecode(rawData, CV_LOAD_IMAGE_COLOR);
    if (frame.size().width == 0) {
        std::cerr << "Decode failed!" << std::endl;
        return cv::Mat(0,0,0);
    }
    free(longBuf);
    return frame;
}

void RemoteCamera::release() {
    this->sock->cleanUp();
    free(this->buffer);
}
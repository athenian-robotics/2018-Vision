#include "../PracticalSocket.h"
#include <iostream>
#include <cstdlib>
#include <opencv2/highgui.hpp>
#include <opencv2/core.hpp>
#include "config.h"

#define BUF_LEN 65540 // Over the max UDP packet size

class RemoteCamera{
public:
    RemoteCamera(unsigned short port);
    cv::Mat grabFrame();
    void release();
private:
    unsigned short srcPort;
    UDPSocket *sock;
    char buffer[BUF_LEN];
    int recvMsgSize;
    std::string srcAddr;
};

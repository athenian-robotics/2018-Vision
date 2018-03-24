#include "../PracticalSocket.h"
#include <opencv2/core.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>
#include <iostream>

#define PACK_SIZE 4096 //udp pack size; note that OSX limits < 8100 bytes
#define ENCODE_QUALITY 50
#define DEBUG

class Streamer {
public:
    Streamer(std::string addr, unsigned short port);

    bool sendFrame(cv::Mat frame);

    void close();

    bool running;
#ifdef DEBUG
    std::string getStats();
    clock_t last_cycle;
    std::stringstream stats;
#endif
private:
    unsigned short servPort;
    std::string servAddr;
    UDPSocket *sock;

    int jpegqual;
    std::vector<uchar> encoded;
    std::vector<int> compression_params;

};
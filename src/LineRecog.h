#include <opencv2/core/types.hpp>
#include <opencv2/core/mat.hpp>

// REMEMBER THAT OPENCV USES BGR

class LineRecog {
    struct thetaNimg {
        explicit thetaNimg(double theta, cv::Mat) {
            this->theta = theta;
            this->img = img;
        }

        double theta;
        cv::Mat img;
    };

public:
    std::vector<cv::Point> get_angle(cv::Mat frame);
private:
    bool isColor(std::vector<int> in, int primaryIdx, std::vector<float> ratios);
    double distance(cv::Point p1, cv::Point p2);
};
//
// Created by Jackson Moffet on 1/29/18.
//

#ifndef CUBERECOG_LINERECOG_H
#define CUBERECOG_LINERECOG_H

#include <opencv2/opencv.hpp>

class LineRecog {
public:
    LineRecog(int x, int y);

    std::vector<cv::Point> find_largest_contour(cv::Mat frame);

    cv::Mat isolate_color(cv::Mat frame, cv::Scalar color);

    // This one is just for display and debugging
    cv::Mat get_frame(cv::Mat frame);

    double get_angle(cv::Mat frame);

private:
    int x_size, y_size;

    int abs(int x);

    double safeDiv(int num, int denom);

    double safeDiv(double num, double denom);

    int mask_l_bound[3] = {1, 1, 1};
    int mask_u_bound[3] = {255, 255, 255};
};


#endif //CUBERECOG_LINERECOG_H

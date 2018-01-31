//
// Created by Jackson Moffet on 1/25/18.
//

#ifndef CUBERECOG_H
#define CUBERECOG_H

#include <opencv2/opencv.hpp>
#include <iostream>

class CubeRecog {
public:
    CubeRecog(int x, int y);

    std::vector<cv::Point> find_largest_contour(cv::Mat frame);

    cv::Point find_centroid(std::vector<cv::Point> contour);

    cv::Mat isolate_color(cv::Mat frame);

    cv::Mat get_frame(cv::Mat frame);

    cv::Point get_cube_center(cv::Mat frame);


private:
    int x_size, y_size;

    int abs(int x);

    int safeDiv(int num, int denom);

    double safeDiv(double num, double denom);

    int mask_l_bound[3] = {1, 1, 1};
    int mask_u_bound[3] = {255, 255, 255};

};


#endif //CUBERECOG_H

//
// Created by Jackson Moffet on 1/25/18.
//

#ifndef CUBERECOG_H
#define CUBERECOG_H

#include <opencv2/core.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>
#include <iostream>

class CubeRecog {


public:
    struct Point{
        double x;
        double y;
        double z;
    };

    struct imgNpoint {
        cv::Mat img;
        cv::Point point;
    };

    CubeRecog(int x, int y);

    std::vector<cv::Point> find_largest_contour(cv::Mat frame);

    cv::Point find_centroid(std::vector<cv::Point> contour);

    cv::Mat isolate_color(cv::Mat frame);

    cv::Mat get_frame(cv::Mat frame);

    CubeRecog::Point get_cube_center(cv::Mat frame);

    imgNpoint get_both(cv::Mat frame);

private:
    int x_size, y_size;

    int abs(int x);

    int safeDiv(int num, int denom);

    double safeDiv(double num, double denom);

    int mask_l_bound[3] = {1, 1, 1};
    int mask_u_bound[3] = {255, 255, 255};

};


#endif //CUBERECOG_H

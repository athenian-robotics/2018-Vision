#include <opencv2/core.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>
#include <iostream>

class CubeRecog {


public:
    struct Point{
        explicit Point(double x=-1, double y=-1, double z=-1){
            this->x = x;
            this->y = y;
            this->z = z;
        }
        double x;
        double y;
        double z;
    };
    //TODO REMOVE FROM ROBIT CODE
    struct DEBUGSTRUCT{
        cv::Mat a;
        cv::Mat b;
        Point point;
    };

    struct imgNpoint {
        cv::Mat img;
        Point point;
    };

    CubeRecog(int x, int y);

    std::vector<cv::Point> find_largest_contour(cv::Mat frame);

    cv::Point find_centroid(std::vector<cv::Point> contour);

    cv::Mat isolate_color(cv::Mat frame);

    CubeRecog::Point get_cube_center(cv::Mat frame);

    DEBUGSTRUCT debug_func(cv::Mat frame);

private:
    int x_size, y_size;

    int abs(int x);

    double safeDiv(double num, double denom);

    int mask_l_bound[3] = {1, 1, 1};
    int mask_u_bound[3] = {255, 255, 255};

};
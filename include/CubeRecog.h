#include <opencv2/opencv.hpp>
struct Point3d {
    explicit Point3d(double x = -1, double y = -1, double z = -1) {
        this->x = x;
        this->y = y;
        this->z = z;
    }

    double x, y, z;
};

struct DEBUGSTRUCT {
    cv::Mat a, b, c;
    Point3d loc;
};

class CubeRecog {
public:
    CubeRecog(int x, int y);

    cv::Mat isolateSeparated(cv::Mat frame);

    Point3d find_centroid(std::vector<cv::Point> contour);

    std::vector<cv::Point> find_closest_cube(cv::Mat frame);

    Point3d get_cube_loc(cv::Mat frame);

    DEBUGSTRUCT debug_fun(cv::Mat frame);

private:
    int x_size, y_size;

    double abs(double x);

    double safeDiv(double num, double denom);

    // We can just cram color data into a point
    double dist3d(Point3d a, Point3d b);

    bool isCubeLike(cv::Rect bb);

    // Take in RGB values and check if they match a predefined color
    bool isColor(int blue, int green, int red);

    bool isEdge(Point3d a, Point3d b, Point3d c);

};
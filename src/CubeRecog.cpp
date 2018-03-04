#include "../include/CubeRecog.h"
// This will need to change
#define THRESH 5.5
#define THRESH_CO 1.25

CubeRecog::CubeRecog(int x, int y) {
    this->x_size = x;
    this->y_size = y;
}

cv::Mat CubeRecog::isolateSeparated(cv::Mat frame) {
    int nRows = frame.rows, nCols = frame.cols;
    // Remember that OpenCV uses BGR
    // OpenCV contour stuff wants a single channel mat, so lets do it ourselves
    cv::Mat ret(frame.rows, frame.cols, CV_8UC1);
    std::vector<cv::Mat> chanz;
    // Lets us look at each individual channel
    // Split into rgb channels so we don't have to mess with the stride of the original image
    cv::split(frame, chanz);
    cv::Mat blue_chan = chanz[0];
    cv::Mat green_chan = chanz[1];
    cv::Mat red_chan = chanz[2];

    uchar *bluRow, *greenRow, *redRow, *nextBluRow, *nextGreenRow, *nextRedRow;
    uchar *returnRow;
    // Convenient for holding 3 numbers, x,y&z or B,G&R
    Point3d a, b, c;
    for (int y = 0; y < nRows; ++y) {
        // Get the row we're gonna write to
        returnRow = ret.ptr<uchar>(y);
        // Get the  current rows
        bluRow = blue_chan.ptr<uchar>(y);
        greenRow = green_chan.ptr<uchar>(y);
        redRow = red_chan.ptr<uchar>(y);
        // Get the next row (the prev row if we're looking at the last one already)
        nextBluRow = blue_chan.ptr<uchar>(y != nRows - 1 ? y + 1 : y - 1);
        nextGreenRow = green_chan.ptr<uchar>(y != nRows - 1 ? y + 1 : y - 1);
        nextRedRow = red_chan.ptr<uchar>(y != nRows - 1 ? y + 1 : y - 1);
        for (int x = 0; x < nCols; ++x) {
            // The main pixel that we're working on right now
            a.x = bluRow[x];
            a.y = greenRow[x];
            a.z = redRow[x];
            // The pixel to the right (or the one to the left if we're looking at the right most)
            b.x = bluRow[x != nCols - 1 ? x + 1 : x - 1];
            b.y = greenRow[x != nCols - 1 ? x + 1 : x - 1];
            b.z = redRow[x != nCols - 1 ? x + 1 : x - 1];
            // The pixel below us (again, if we're looking at one in bottom row, the the one immediately above us)
            c.x = nextBluRow[x];
            c.y = nextGreenRow[x];
            c.z = nextRedRow[x];
            // 255 == white, 0 == black
            if (!isEdge(a, b, c) && isColor(a.x, a.y, a.z))
                returnRow[x] = 0xFF;
            else
                returnRow[x] = 0x00;
        }
    }

    return ret;
}

Point3d CubeRecog::find_centroid(std::vector<cv::Point> contour) {
    Point3d ret;
    cv::Moments M = cv::moments(contour);
    int cX;
    int cY;
    // Lets not blowup
    try {
        cX = int(safeDiv(M.m10, M.m00));
        cY = int(safeDiv(M.m01, M.m00));
    } catch (std::overflow_error e) {
        // Point3d inits to all -1
        return ret;
    }
    cv::Rect bound_b = cv::boundingRect(contour);
    ret.x = cX;
    ret.y = cY;
    ret.z = bound_b.area();
    return ret;
}

std::vector<cv::Point> CubeRecog::find_closest_cube(cv::Mat frame) {
    std::vector<std::vector<cv::Point>> contours;
    std::vector<cv::Vec4i> hierarchy;

    cv::findContours(frame, contours, hierarchy, cv::RETR_TREE, cv::CHAIN_APPROX_SIMPLE);
    // If there is no contours, then we shouldn't look.
    if (contours.empty()) {
        std::vector<cv::Point> noCube;
        return noCube;
    }
    cv::Moments M;
    cv::Rect bBox;
    double largest_area = 0;
    int largest_idx = -1;
    for (int i = 0; i < contours.size(); ++i) {
        M = cv::moments(contours[i]);
        bBox = cv::boundingRect(contours[i]);
        if (!isCubeLike(bBox))
            continue;
        if (M.m00 > largest_area) {
            largest_area = M.m00;
            largest_idx = i;
        }
    }
    return contours[largest_idx];
}

Point3d CubeRecog::get_cube_loc(cv::Mat frame) {
    cv::Mat iso = isolateSeparated(frame);
    std::vector<cv::Point> cont = find_closest_cube(iso);
    if (cont.empty())
        return Point3d();
    return find_centroid(cont);
}

DEBUGSTRUCT CubeRecog::debug_fun(cv::Mat frame) {
    DEBUGSTRUCT ret;
    cv::Mat iso = isolateSeparated(frame);
    std::vector<cv::Point> cont = find_closest_cube(iso);
    Point3d loc = find_centroid(cont);
    cv::rectangle(frame, cv::boundingRect(cont), cv::Scalar(0, 0, 255));
    cv::circle(frame, cv::Point(loc.x, loc.y), 7, cv::Scalar(0, 0, 255), -1);
    ret.a = frame;
    ret.b = iso;
    ret.loc = loc;
    return ret;
}

/*** PRIVATE FUNCTIONS ***/
double CubeRecog::abs(double x) {
    return x > 0 ? x : -x;
}

double CubeRecog::safeDiv(double num, double denom) {
    if (denom == 0)
        throw std::overflow_error("Divide by zero error");
    return num / denom;
}

double CubeRecog::dist3d(Point3d a, Point3d b) {
    double xD = a.x - b.x, yD = a.y - b.y, zD = a.z - b.z;
    return sqrt((xD * xD) + (yD * yD) + (zD * zD));
}

bool CubeRecog::isCubeLike(cv::Rect bb) {
    bool propSize = bb.area() > 1000;
    if (!propSize)
        return false;
    // Basically the percent change formula (what percent different is the height from the width)
    bool ratiosOK = (abs(bb.height - bb.width) / bb.width) * 100 < 50;
    return propSize && ratiosOK;
}

bool CubeRecog::isColor(int blue, int green, int red) {
    int g_low, g_high, diff, sim;
    bool green_in_bound, is_yellow, is_grey;

    g_low = red - 30;
    g_high = red + 18;
    // Avg of green and red - blue = make sure that there isn't too much blue
    diff = (green + red) / 2 - blue;
    // Used to exclude grey, white and black pixels
    sim = abs(green - red) + abs(red - blue) + abs(green - blue);
    green_in_bound = g_low <= green && green <= g_high;
    is_yellow = diff >= 55;
    is_grey = sim <= 30;
    return is_yellow && !is_grey && green_in_bound;
}

bool CubeRecog::isEdge(Point3d a, Point3d b, Point3d c) {
    return (dist3d(a, b) > THRESH && dist3d(a, c) > THRESH) ||
           (dist3d(a, b) > THRESH * THRESH_CO || dist3d(a, c) > THRESH * THRESH_CO);
}
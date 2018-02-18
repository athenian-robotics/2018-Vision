#include "CubeRecog.h"

CubeRecog::CubeRecog(int x, int y) {
    x_size = x;
    y_size = y;
}

cv::Mat CubeRecog::isolate_color(cv::Mat frame) {
    // Remember that opencv uses BGR
    cv::Mat ret(frame.rows, frame.cols, CV_8UC1);
    std::vector<cv::Mat> chanz;
    cv::split(frame, chanz);
    cv::Mat blue_chan = chanz[0];
    cv::Mat green_chan = chanz[1];
    cv::Mat red_chan = chanz[2];
    int nRows = blue_chan.rows;
    int nCols = blue_chan.cols;

    uchar *og_blue, *og_green, *og_red, *ret_mono;
    int red, green, blue, g_low, g_high, diff, sim;
    bool green_in_bound, is_yellow, is_grey;
    for (int y = 0; y < nRows; ++y) {
        og_blue = blue_chan.ptr<uchar>(y);
        og_green = green_chan.ptr<uchar>(y);
        og_red = red_chan.ptr<uchar>(y);
        ret_mono = ret.ptr<uchar>(y);
        for (int x = 0; x < nCols; ++x) {
            blue = og_blue[x];
            green = og_green[x];
            red = og_red[x];

            // Set the green high and low in relation to the red
            g_low = red - 30;
            g_high = red + 18;
            // Avg of green and red - blue = make sure that there isn't too much blue
            diff = (green + red) / 2 - blue;
            // Used to exclude grey, white and black pixels
            sim = abs(green - red) + abs(red - blue) + abs(green - blue);
            green_in_bound = g_low <= green && green <= g_high;
            is_yellow = diff >= 55;
            is_grey = sim <= 30;

            if (!green_in_bound || !is_yellow || is_grey) {
                ret_mono[x] = 0;
            } else {
                ret_mono[x] = 255;
            }
        }
    }

    return ret;
}

std::vector<cv::Point> CubeRecog::find_largest_contour(cv::Mat frame) {
    std::vector<std::vector<cv::Point>> contours;
    std::vector<cv::Vec4i> hierarchy;

    cv::findContours(frame, contours, hierarchy, cv::RETR_TREE, cv::CHAIN_APPROX_SIMPLE);
    // If there is no contours, then we shouldn't look.
    if (contours.empty()) {
        std::vector<cv::Point> noCube;
        return noCube;
    }
    cv::Moments M;
    double largest_area = 0;
    int largest_idx = 0;
    for (int i = 0; i < contours.size(); ++i) {
        M = cv::moments(contours[i]);
        if (M.m00 > largest_area) {
            largest_area = M.m00;
            largest_idx = i;
        }
    }

    // To increase the likely hood that we are looking at a cube, enforce a minimum size
    if (largest_area < 20) {
        std::vector<cv::Point> tooSmol;
        return tooSmol;
    }
    return contours[largest_idx];
}

cv::Point CubeRecog::find_centroid(std::vector<cv::Point> contour) {
    cv::Moments M = cv::moments(contour);
    int cX;
    int cY;
    try {
        cX = int(safeDiv(M.m10, M.m00));
        cY = int(safeDiv(M.m01, M.m00));
    } catch (std::overflow_error e) {
        return cv::Point(-1, -1);
    }
    return cv::Point(cX, cY);
}

int CubeRecog::abs(int x) {
    return x > 0 ? x : -x;
}

double CubeRecog::safeDiv(double num, double denom) {
    if (denom == 0)
        throw std::overflow_error("Divide by zero error");
    return num / denom;
}

CubeRecog::Point CubeRecog::get_cube_center(cv::Mat frame) {
    if (frame.cols != x_size || frame.rows != y_size) {
        cv::resize(frame, frame, cv::Size(x_size, y_size));
    }

    // Get a black and white image, with the white being yellow and the black being everything else
    cv::Mat iso = isolate_color(frame);
    std::vector<int> lowerB(mask_l_bound, mask_l_bound + sizeof(mask_l_bound) / sizeof(mask_l_bound[0]));
    std::vector<int> upperB(mask_u_bound, mask_u_bound + sizeof(mask_u_bound) / sizeof(mask_u_bound[0]));

    std::vector<cv::Point> contour = find_largest_contour(iso);
    Point centerNsize;
    cv::Point tmp = find_centroid(contour);
    centerNsize.x = tmp.x;
    centerNsize.y = tmp.y;
    centerNsize.z = cv::moments(contour).m00;
    return centerNsize;
}

CubeRecog::DEBUGSTRUCT CubeRecog::debug_func(cv::Mat frame) {
    if (frame.cols != x_size || frame.rows != y_size) {
        cv::resize(frame, frame, cv::Size(x_size, y_size));
    }
    DEBUGSTRUCT ret;

    cv::Mat iso = isolate_color(frame);
//    std::vector<int> lowerB(mask_l_bound, mask_l_bound + sizeof(mask_l_bound) / sizeof(mask_l_bound[0]));
//    std::vector<int> upperB(mask_u_bound, mask_u_bound + sizeof(mask_u_bound) / sizeof(mask_u_bound[0]));
//    cv::Mat mask;
//    cv::inRange(iso, lowerB, upperB, mask);
    std::vector<cv::Point> contour = find_largest_contour(iso);

    if (contour.empty()) {
        ret.a = frame;
        ret.b = iso;
        return ret;
    }

    cv::Point centroid = find_centroid(contour);
    cv::Rect bound_b = cv::boundingRect(contour);
    cv::Mat processed;

    frame.copyTo(processed);

    cv::rectangle(processed, bound_b, cv::Scalar(0, 0, 255));
    cv::circle(processed, centroid, 7, cv::Scalar(0, 0, 255), -1);

    ret.a = processed;
    ret.b = iso;
    ret.point.x = centroid.x;
    ret.point.y = centroid.y;
    ret.point.z = cv::moments(contour).m00;
    return ret;
}
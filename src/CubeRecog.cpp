#include "CubeRecog.h"

CubeRecog::CubeRecog(int x, int y) {
    x_size = x;
    y_size = y;
}

cv::Mat CubeRecog::isolate_color(cv::Mat frame) {
    // Remember that opencv uses BGR
    std::vector<cv::Mat> chanz;
    cv::split(frame, chanz);
    cv::Mat blue_chan = chanz[0];
    cv::Mat green_chan = chanz[1];
    cv::Mat red_chan = chanz[2];
    int nRows = blue_chan.rows;
    int nCols = blue_chan.cols;

    uchar *p_blue;
    uchar *p_green;
    uchar *p_red;
    int red, green, blue, g_low, g_high, diff, sim;
    bool green_in_bound, is_yellow, is_grey;
    for (int y = 0; y < nRows; ++y) {
        p_blue = blue_chan.ptr<uchar>(y);
        p_green = green_chan.ptr<uchar>(y);
        p_red = red_chan.ptr<uchar>(y);
        for (int x = 0; x < nCols; ++x) {
            blue = p_blue[x];
            green = p_green[x];
            red = p_red[x];

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
                p_blue[x] = 0;
                p_green[x] = 0;
                p_red[x] = 0;
            } else {
                p_blue[x] = 255;
                p_green[x] = 255;
                p_red[x] = 255;
            }
        }
    }

    cv::Mat tmp[] = {blue_chan, green_chan, red_chan};
    std::vector<cv::Mat> comb(tmp, tmp + sizeof(tmp) / sizeof(tmp[0]));
    cv::Mat ret;
    cv::merge(comb, ret);
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

cv::Mat CubeRecog::get_frame(cv::Mat frame) {
    if (frame.cols != x_size || frame.rows != y_size) {
        cv::resize(frame, frame, cv::Size(x_size, y_size));
    }

    // Get a black and white image, with the white being yellow and the black being everything else
    cv::Mat iso = isolate_color(frame);
    std::vector<int> lowerB(mask_l_bound, mask_l_bound + sizeof(mask_l_bound) / sizeof(mask_l_bound[0]));
    std::vector<int> upperB(mask_u_bound, mask_u_bound + sizeof(mask_u_bound) / sizeof(mask_u_bound[0]));
    cv::Mat mask;
    cv::inRange(iso, lowerB, upperB, mask);

    std::vector<cv::Point> contour = find_largest_contour(mask);
    if (contour.empty()) {
        return frame;
    }
    cv::Point centroid = find_centroid(contour);
    // Check if we think we've found a a power cube
    cv::Rect bound_b = cv::boundingRect(contour);
    cv::Mat processed;
    frame.copyTo(processed);
    cv::rectangle(processed, bound_b, cv::Scalar(0, 0, 255));
    cv::circle(processed, centroid, 7, cv::Scalar(0, 0, 255), -1);
    return processed;
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
    centerNsize.z = cv::contourArea(contour);
    return centerNsize;
}

CubeRecog::imgNpoint CubeRecog::get_both(cv::Mat frame) {
    if (frame.cols != x_size || frame.rows != y_size) {
        cv::resize(frame, frame, cv::Size(x_size, y_size));
    }
    imgNpoint ret;

    cv::Mat iso = isolate_color(frame);
    std::vector<int> lowerB(mask_l_bound, mask_l_bound + sizeof(mask_l_bound) / sizeof(mask_l_bound[0]));
    std::vector<int> upperB(mask_u_bound, mask_u_bound + sizeof(mask_u_bound) / sizeof(mask_u_bound[0]));
    cv::Mat mask;
    cv::inRange(iso, lowerB, upperB, mask);

    std::vector<cv::Point> contour = find_largest_contour(mask);

    if (contour.empty()) {
        ret.img = frame;
        return ret;
    }

    cv::Point centroid = find_centroid(contour);
    cv::Rect bound_b = cv::boundingRect(contour);
    cv::Mat processed;

    frame.copyTo(processed);

    cv::rectangle(processed, bound_b, cv::Scalar(0, 0, 255));
    cv::circle(processed, centroid, 7, cv::Scalar(0, 0, 255), -1);
    cv::circle(processed, (320, 240), 7, cv::Scalar(0, 255, 255), -1);
    cv::circle(processed, (305, 240), 7, cv::Scalar(0, 255, 255), -1);
    cv::circle(processed, (335, 240), 7, cv::Scalar(0, 255, 255), -1);

    ret.img = processed;
    ret.point.x = centroid.x;
    ret.point.y = centroid.y;
    ret.point.z = centroid.z;
    return ret;
}
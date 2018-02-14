#include <iostream>
#include <ctime>
#include <ros/ros.h>
#include <geometry_msgs/Point.h>
#include "src/CubeRecog.h"

int main(int argc, char *argv[]) {
    cv::VideoCapture cap(1);
    if (!cap.isOpened()) {
        std::cout << "BORK" << std::endl;
        return -1;
    }

    CubeRecog recog(640, 360);
    // Setup to count the frame rate
    std::time_t startTime = std::time(0);
    int tick = 0;
    // Setup ROS stuff
    // Must call ros::init before doing anything else with ROS
    ros::init(argc, argv, "cube_finder");
    ros::NodeHandle handle;
    // Create a publisher with a message queue of 1 -> just blast over the network
    ros::Publisher publisher = handle.advertise<geometry_msgs::Point>("cube", 1);
    // Send data at a max of 15hz so we don't flood the server
    ros::Rate loop_rate(15);

    while (ros::ok()) {
        cv::Mat frame;
        cap >> frame;
        CubeRecog::Point location = recog.get_cube_center(frame);

        geometry_msgs::Point point_msg;
        point_msg.x = location.x;
        point_msg.y = location.y;
        point_msg.z = location.z;
        publisher.publish(point_msg);
        loop_rate.sleep();
        // TODO remove this line before running on robot
        cv::waitKey(1);
    }

    cv::destroyAllWindows();
    cap.release();
}
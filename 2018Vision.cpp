#include <iostream>
#include <ctime>
#include <ros/ros.h>
#include <geometry_msgs/Point.h>
#include <std_msgs/String.h>
#include "src/CubeRecog.h"
#include "src/PipeWriter.h"

int main(int argc, char *argv[]) {
    cv::VideoCapture cap(0);
    if (!cap.isOpened()) {
        std::cout << "BORK" << std::endl;
        return -1;
    }

    std::clock_t start;
    CubeRecog recog(640, 360);
    PipeWriter writer((char *) ("/tmp/img"));
    // Setup ROS stuff
    // Must call ros::init before doing anything else with ROS
    ros::init(argc, argv, "cube_finder");
    ros::NodeHandle handle;
    // Create a publisher with a message queue of 1 -> just blast over the network
    ros::Publisher cube_publisher = handle.advertise<geometry_msgs::Point>("cube", 0);
    ros::Publisher frame_time_pub = handle.advertise<std_msgs::String>("frame_time", 0);
    // Send data at a max of 15hz so we don't flood the server
    ros::Rate loop_rate(20);

    while (ros::ok()) {
        start = std::clock();
        cv::Mat frame;
        cap >> frame;
//        CubeRecog::imgNpoint data = recog.get_both(frame);
        CubeRecog::Point location = recog.get_cube_center(frame);

        // Write the image to be displayed
  //      writer.writeImg(data.img);

        geometry_msgs::Point point_msg;
        point_msg.x = location.x;
        point_msg.y = location.y;
        point_msg.z = location.z;
        std_msgs::String proc_time_msg;
        std::ostringstream time_msg_data;
        time_msg_data << (std::clock() - start) / (double) CLOCKS_PER_SEC << " secs";
        proc_time_msg.data = time_msg_data.str();
        cube_publisher.publish(point_msg);
        loop_rate.sleep();
    }

    cv::destroyAllWindows();
    cap.release();
}
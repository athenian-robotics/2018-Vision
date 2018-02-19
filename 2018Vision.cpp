#include <iostream>
#include <ctime>

#include <ros/ros.h>
#include <geometry_msgs/Point.h>
#include <std_msgs/String.h>

#include "src/CubeRecog.h"
#include "src/PipeWriter.h"

int main(int argc, char *argv[]) {
    // TODO CHANGE BACK TO 0 BEFORE COMMIT
    cv::VideoCapture cap(0);
    if (!cap.isOpened()) {
        std::cout << "HAVING A CAMERA MIGHT HELP" << std::endl;
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
    ros::Rate loop_rate(30);
    std::cout << "ENTERING LOOP" << std::endl;
    while (ros::ok()) {
        start = std::clock();
        cv::Mat frame;
        cap >> frame;

        // CubeRecog::DEBUGSTRUCT data = recog.debug_func(frame);
        CubeRecog::Point location = recog.get_cube_center(frame);
        // This bit is under review
        // Write the image to be displayed
        // writer.writeImg(data.img);

        // Stuff the point into a message
        geometry_msgs::Point point_msg;
        point_msg.x = location.x;
        point_msg.y = location.y;
        point_msg.z = location.z;
        // Publish the frame time, b/c why not
        std_msgs::String proc_time_msg;
        std::stringstream time_msg_data;
        double end = std::clock();
        time_msg_data << (end - start) / (double) CLOCKS_PER_SEC * 1000 << " ms";
        proc_time_msg.data = time_msg_data.str();
        // Actually publish the data that we packed earlier
        cube_publisher.publish(point_msg);
        frame_time_pub.publish(proc_time_msg);
        // Limit to however many Hz was passed to loop_rate so we don't flood the server
        loop_rate.sleep();
    }

    cv::destroyAllWindows();
    cap.release();
}
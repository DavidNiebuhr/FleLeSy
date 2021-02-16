#!/usr/bin/env python
import json
import os
import uuid
import roslaunch
import rospy


def app_main():
    rospy.init_node("axis_control")  # , log_level=rospy.DEBUG)

    rospy.spin()


if __name__ == '__main__':
    app_main()

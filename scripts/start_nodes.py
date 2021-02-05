#!/usr/bin/env python

import uuid
import roslaunch
import rospy
from start_a_node import start_a_node


def app_main():
    rospy.init_node("start_nodes")
    launch = roslaunch.scriptapi.ROSLaunch()
    launch.start()
    start_a_node(launch, "FleLeSy", "module_imitator.py", "Module_22")
    rospy.spin()


if __name__ == '__main__':
    app_main()

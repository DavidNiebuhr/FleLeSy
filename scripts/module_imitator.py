#!/usr/bin/env python
import os
import time
import uuid
import roslaunch
import rospy
from FleLeSy.srv import *

Module_Name = "Module"


# Affiliated_Robots = []

class Robot:
    def __init__(self, package, executable, name):
        self.identification = str(uuid.uuid4())
        self.package = package
        self.executable = executable
        self.name = name

    def start_robot_exe(self, launch):
        namespace = self.identification
        exe = roslaunch.core.Node(self.package, self.executable, self.name, namespace)
        process = launch.launch(exe)


def app_main():
    rospy.init_node(Module_Name)
    uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
    roslaunch.configure_logging(uuid.replace("-","_"))
    launch = roslaunch.parent.ROSLaunchParent(uuid,
                                              ["/home/david/catkin_ws/src/kuka210_moveit_config/launch/demo.launch"])
    launch.start()
    rospy.loginfo("started")


    """launch = roslaunch.scriptapi.ROSLaunch()
    launch.start()
    rospy.sleep(1)
    simrobot1 = Robot("kuka210_moveit_config", "demo.launch", "KUKA_kr210")
    simrobot1.start_robot_exe(launch)"""
    """
    robot1 = Robot("FleLeSy", "robot_imitator.py", "ABBle")
    robot1.start_robot_exe(launch)
    robot2 = Robot("FleLeSy", "robot_imitator.py", "KUKAchen")
    robot2.start_robot_exe(launch)"""
    rospy.spin()

if __name__ == '__main__':
    app_main()

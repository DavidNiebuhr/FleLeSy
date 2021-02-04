#!/usr/bin/env python
import uuid
import roslaunch
import rospy
from FleLeSy.srv import *

Module_Name = "Module_1_a"


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
    launch = roslaunch.scriptapi.ROSLaunch()
    launch.start()
    rospy.sleep(1)

    robot1 = Robot("FleLeSy", "robot_imitator.py", "ABBle")
    robot1.start_robot_exe(launch)
    robot2 = Robot("FleLeSy", "robot_imitator.py", "KUKAchen")
    robot2.start_robot_exe(launch)
    try:
        while True:
            rospy.sleep(2)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    app_main()

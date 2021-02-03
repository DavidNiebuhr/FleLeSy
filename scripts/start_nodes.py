#!/usr/bin/env python

import rospy
import uuid
import roslaunch
import time

def start_robot_imitator():
    package = 'FleLeSy'
    executable = 'robot_imitator.py'
    name = "robot_imitator_1"
    identification = uuid.uuid4()
    namespace = '/%s' % identification
    node = roslaunch.core.Node(package, executable, name, namespace)
    launch = roslaunch.scriptapi.ROSLaunch()
    launch.start()


def start_kukarobot():
    package = 'kuka210_moveit_config'
    executable = 'demo.launch'
    name = "kuka_kr210_1"
    identification = uuid.uuid4()
    namespace = '/%s' % identification
    node = roslaunch.core.Node(package, executable, name, namespace)
    launch = roslaunch.scriptapi.ROSLaunch()
    launch.start()


def start_control_system():
    package = 'FleLeSy'
    executable = 'control_system.py'
    name = "control_system"
    namespace = '/control_system'
    node = roslaunch.core.Node(package, executable, name, namespace)
    launch = roslaunch.scriptapi.ROSLaunch()
    launch.start()


def app_main():
    rospy.init_node('start_nodes')
    time.sleep(0.5)
    start_control_system()
    time.sleep(3)
    start_kukarobot()
    time.sleep(3)
    start_robot_imitator()


if __name__ == '__main__':
    app_main()

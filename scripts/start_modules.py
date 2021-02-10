#!/usr/bin/env python
import uuid
import roslaunch
import rospy
from start_a_node import start_a_node



def start_module(launch, package, executable, name):
    node = roslaunch.core.Node(package, executable, name) #, output="screen")
    launch.launch(node)


def app_main():
    rospy.sleep(0.2)
    rospy.init_node("start_modules")
    launch = roslaunch.scriptapi.ROSLaunch()
    launch.start()
    start_module(launch, "FleLeSy", "module_imitator.py", "m1" + str(uuid.uuid4()).replace("-", "_"))
    start_module(launch, "FleLeSy", "module_imitator.py", "m2" + str(uuid.uuid4()).replace("-", "_"))
    rospy.spin()


if __name__ == '__main__':
    app_main()

#!/usr/bin/env python
import rospy
from FleLeSy.srv import *

Module_Name = "TIM_platform_1"
Affiliated_Robots = []


#Muss Robotern beim starten eine ID zuweisen und anschließend meldet es sich beim System an und schickt dabei eine Liste mit Robotern mit.


def app_main():
    rospy.init_node(Module_Name)


if __name__ == '__main__':
    app_main()

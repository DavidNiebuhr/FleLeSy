#!/usr/bin/env python

import rospy
from FleLeSy.srv import *
from std_msgs.msg import std_msgs

spindle_on_status = False


def open_gripper(SRV):
    global spindle_on_status
    gripper_open_status = True
    return set_bool_statusResponse(True)


def close_gripper(SRV):
    global spindle_on_status
    gripper_open_status = False
    return set_bool_statusResponse(True)


def offer_services():
    rospy.Service('%s/open_gripper' % rospy.get_name(), set_bool_status, open_gripper)
    rospy.Service('%s/close_gripper' % rospy.get_name(), set_bool_status, close_gripper)


def publish_state():
    while not rospy.is_shutdown():
        r = rospy.Rate(1)  # 10hz
        so = rospy.Publisher('%s/gripper_open' % rospy.get_name(), std_msgs.msg.Bool, queue_size=10)  # on = True
        so.publish(spindle_on_status)
        r.sleep()


def app_main():
    rospy.init_node("grippers")  # , log_level=rospy.DEBUG)

    offer_services()
    publish_state()
    rospy.spin()


if __name__ == '__main__':
    app_main()

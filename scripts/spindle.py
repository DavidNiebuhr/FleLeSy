#!/usr/bin/env python

import rospy
from FleLeSy.srv import *
from std_msgs.msg import std_msgs

nail_gun_ready = False


def start_spindle(SRV):
    global nail_gun_ready
    spindle_on_status = True
    return set_bool_statusResponse(True)


def stop_spindle(SRV):
    global nail_gun_ready
    spindle_on_status = False
    return set_bool_statusResponse(True)


def offer_services():
    rospy.Service('%s/start_spindle' % rospy.get_name(), set_bool_status, start_spindle)
    rospy.Service('%s/stop_spindle' % rospy.get_name(), set_bool_status, start_spindle)


def publish_state():
    while not rospy.is_shutdown():
        r = rospy.Rate(1)  # 10hz
        so = rospy.Publisher('%s/spindle_on' % rospy.get_name(), std_msgs.msg.Bool, queue_size=10)  # on = True
        so.publish(nail_gun_ready)
        r.sleep()


def app_main():
    rospy.init_node("spindle", log_level=rospy.DEBUG)

    offer_services()
    publish_state()
    rospy.spin()


if __name__ == '__main__':
    app_main()

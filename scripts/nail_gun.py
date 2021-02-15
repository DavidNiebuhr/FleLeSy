#!/usr/bin/env python

import rospy
from FleLeSy.srv import *
from std_msgs.msg import std_msgs

nail_gun_ready = True  # Nachladevorgang setzt den Status kurzzeitig auf False


def shoot_nail(SRV):
    global nail_gun_ready
    nail_gun_ready = False
    rospy.sleep(5)  # Nachladevorgang
    nail_gun_ready = True
    return set_bool_statusResponse(True)


def offer_services():
    rospy.Service('%s/shoot_nail' % rospy.get_name(), set_bool_status, shoot_nail)


def publish_state():
    while not rospy.is_shutdown():
        r = rospy.Rate(1)  # 10hz
        so = rospy.Publisher('%s/nail_gun_ready' % rospy.get_name(), std_msgs.msg.Bool, queue_size=10)
        so.publish(nail_gun_ready)
        r.sleep()


def app_main():
    rospy.init_node("spindle", log_level=rospy.DEBUG)

    offer_services()
    publish_state()
    rospy.spin()


if __name__ == '__main__':
    app_main()

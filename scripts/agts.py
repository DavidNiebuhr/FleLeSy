#!/usr/bin/env python

import rospy
from FleLeSy.srv import *
from std_msgs.msg import std_msgs, Float64


class Movement:
    movement_status = False


def register_node_func():
    response = None
    rospy.wait_for_service('/control_system/register_robot', 20)
    rospy.logdebug("R: Found it, continuing registration.")
    try:
        register_service = rospy.ServiceProxy('/control_system/register_robot', register_robot)
        response = register_service(rospy.get_name(), rospy.get_namespace()[:-1])
    except rospy.ServiceException as e:
        rospy.logerr("R: Registration has failed: %s" % e)
        response.success = False
    if response.success:
        rospy.logdebug("R: Robot %s is registered." % rospy.get_name())
    else:
        rospy.logwarn(
            "R: Controlsystem returned that it didn't work")
    return None

def set_movement_status(set_to):
    Movement.movement_status = set_to


def get_movement_status():
    return Movement.movement_status


def callback(affiliated_fm_position, move_x_target):
    while ((affiliated_fm_position.x + 0.05) < move_x_target) or ((affiliated_fm_position.x - 0.05) > move_x_target):
        if (affiliated_fm_position.x + 0.05) < move_x_target:
            move = 0.1
        else:
            move = -0.1
        r = rospy.Rate(10)
        m_fm = rospy.Publisher('%s/move_platform' % rospy.get_name().split("/", 2)[0], Float64,
                               queue_size=10)  # on = True
        m_fm.publish(move)
        r.sleep()


def move_agts(SRV):
    set_movement_status(True)
    rospy.Subscriber('%s/platform_pose' % rospy.get_name().split("/", 2)[0], geometry_msgs.msg.Pose2D,
                     callback(SRV.move_x_target))
    set_movement_status(False)
    return set_bool_statusResponse(True)


def offer_services():
    rospy.Service('%s/move_agts' % rospy.get_name(), agts_new_target, move_agts)


def publish_state():
    while not rospy.is_shutdown():
        r = rospy.Rate(1)  # 10hz
        so = rospy.Publisher('%s/moving' % rospy.get_name(), std_msgs.msg.Bool, queue_size=10)  # on = True
        so.publish()
        r.sleep()


def app_main():
    rospy.init_node("agts")#, log_level=rospy.DEBUG)

    offer_services()
    publish_state()
    register_node_func()
    rospy.spin()


if __name__ == '__main__':
    app_main()

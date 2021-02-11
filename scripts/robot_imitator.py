#!/usr/bin/env python
import rospy
from FleLeSy.srv import *
from std_msgs.msg import std_msgs

RobotName = "ThisRobot"
currently_working = False  # working = True
gripper_open = False
spindle_on = False
x = -4.2
y = +19.3
z = +132.4
position = [x, y, z]


def move_x_to(x_target):
    while x_target != position[0]:
        if position[0] < x_target:
            position[0] += 0.1
        else:
            position[0] -= 0.1
        rospy.sleep(0.01)
    return True


def move_y_to(y_target):
    while y_target != position[1]:
        if position[1] < y_target:
            position[1] += 0.1
        else:
            position[1] -= 0.1
        rospy.sleep(0.01)
    return True


def move_z_to(z_target):
    while z_target != position[2]:
        if position[2] < z_target:
            position[2] += 0.1
        else:
            position[2] -= 0.1
        rospy.sleep(0.01)
    return True


def move_to(x_target, y_target, z_target):
    x_done = move_x_to(x_target)
    y_done = move_y_to(y_target)
    z_done = move_z_to(z_target)
    while not x_done or not y_done or not z_done:
        rospy.sleep(1)
    return True


def interpolate(SRV):  # SRV=ServiceResponseValues
    global currently_working
    rospy.loginfo("R: Moving to point\nX: %s\nY: %s\nZ: %s\n with interpolation" % (
        SRV.target.X, SRV.target.Y, SRV.target.Z))
    arrived = move_to(SRV.target.X, SRV.target.Y, SRV.target.Z)
    while not arrived:
        currently_working = True
        rospy.sleep(1)
    currently_working = False
    return AuftragResponse(True)


def publish_robot_state():
    while not rospy.is_shutdown():
        r = rospy.Rate(1)  # 10hz
        wor = rospy.Publisher('%s/working' % rospy.get_name(), std_msgs.msg.Bool,
                              queue_size=10)  # working = True
        wor.publish(currently_working)

        eep = rospy.Publisher('%s/end_effector_position' % rospy.get_name(), geometry_msgs.msg.Point, queue_size=10)
        eep.publish(position[0], position[1], position[2])

        go = rospy.Publisher('%s/gripper_open' % rospy.get_name(), std_msgs.msg.Bool, queue_size=10)  # open = True
        go.publish(gripper_open)

        so = rospy.Publisher('%s/spindle_on' % rospy.get_name(), std_msgs.msg.Bool, queue_size=10)  # on = True
        so.publish(spindle_on)
        r.sleep()


def offer_services():
    rospy.Service('%s/interpolate' % rospy.get_name(), Auftrag, interpolate)
    rospy.loginfo("R: Interpolation is available")

    rospy.Service('%s/point2point' % rospy.get_name(), Auftrag, interpolate)
    rospy.loginfo("R: Milling is available")

    rospy.Service('%s/pic_and_place' % rospy.get_name(), Auftrag, interpolate)
    rospy.loginfo("R: Pick and place is available")


def register_robot_func():
    response = None
    rospy.wait_for_service('/control_system/register_robot', 20)
    rospy.loginfo("R: Found it, continuing registration.")
    try:
        register_service = rospy.ServiceProxy('/control_system/register_robot', register_robot)
        response = register_service(rospy.get_name(), rospy.get_namespace()[:-1])
    except rospy.ServiceException as e:
        rospy.logerr("R: Registration has failed: %s" % e)
        response.success = False
    if response.success:
        rospy.loginfo("R: Robot %s is registered." % rospy.get_name())
    else:
        rospy.logwarn(
            "R: Controlsystem returned that it didn't work")
    return None


def app_main():
    rospy.init_node(RobotName, log_level=rospy.DEBUG)
    rospy.loginfo("R: Roboternode %s is Running. I'll look out for the registration Service." % rospy.get_name())
    register_robot_func()
    offer_services()
    publish_robot_state()
    rospy.spin()


if __name__ == '__main__':
    app_main()  # Den Grund warum das extra als Funktion aufgerufen wird, habe ich noch nicht verstanden.

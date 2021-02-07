#!/usr/bin/env python
import rospy
from FleLeSy.srv import *

RobotName = "ThisRobot"


def Interpolate(SRV):  # SRV=ServiceResponseValues
    rospy.loginfo("R: Moving to point\nX: %s\nY: %s\nZ: %s\n with interpolation" % (
        SRV.target.X, SRV.target.Y, SRV.target.Z))
    return True


def offer_services():
    rospy.Service('%s/interpolate' % rospy.get_name(), Auftrag, Interpolate)
    rospy.loginfo("R: Interpolation is available")


def register_robot_func():
    global response
    rospy.wait_for_service('/control_system/register_robot', 20)
    rospy.loginfo("R: Found it, continuing registration.")
    try:
        register_service = rospy.ServiceProxy('/control_system/register_robot', register_robot)
        response = register_service(rospy.get_name(), rospy.get_namespace())
    except rospy.ServiceException as e:
        rospy.logerr("R: Registration has failed: %s" % e)
        response.success = False
    if response.success:
        rospy.loginfo("R: Robot %s is registered." % rospy.get_name())
    else:
        rospy.logwarn(
            "R: Controlsystem returned that it didn't work")
    offer_services()
    return None


def app_main():
    rospy.init_node(RobotName)#, log_level=rospy.DEBUG
    rospy.loginfo("R: Roboternode %s is Running. I'll look out for the registration Service." % rospy.get_name())
    register_robot_func()
    rospy.spin()


if __name__ == '__main__':
    app_main()  # Den Grund warum das extra als Funktion aufgerufen wird, habe ich noch nicht verstanden.

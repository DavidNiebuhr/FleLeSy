#!/usr/bin/env python
import rospy
from FleLeSy.srv import *

RobotName = "ThisRobot"


def Interpolate(SRV):  # SRV=ServiceResponseValues
    rospy.loginfo("Ich fahre per Interpolation zu Punkt \nX: %s\nY: %s\nZ: %s" % (
        SRV.target.X, SRV.target.Y, SRV.target.Z))
    return True


def offer_services():
    rospy.Service('%s/interpolate' % rospy.get_name(), Auftrag, Interpolate)
    rospy.loginfo("Interpolation ist verfuegbar")


def register_robot_func():
    rospy.wait_for_service('/control_system/register_robot', 20)
    rospy.loginfo("Found it, continuing registration.")
    try:
        register_service = rospy.ServiceProxy('/control_system/register_robot', register_robot)
        response = register_service(rospy.get_name(), rospy.get_namespace())
    except rospy.ServiceException as e:
        rospy.logerr("Registration has failed: %s" % e)
    if response.Erfolg:
        rospy.loginfo("Robot %s is registered." % rospy.get_name())
    else:
        rospy.logwarn(
            "Das Leitsystem hat einen Fehler zurueckgemeldet. Wahrscheinlich ist das Modul bereits angemeldet.")
    offer_services()
    return None


def app_main():
    rospy.init_node(RobotName)#, log_level=rospy.DEBUG
    rospy.loginfo("Roboternode %s is Running. I'll look out for the registration Service." % rospy.get_name())
    register_robot_func()
    rospy.spin()


if __name__ == '__main__':
    app_main()  # Den Grund warum das extra als Funktion aufgerufen wird, habe ich noch nicht verstanden.

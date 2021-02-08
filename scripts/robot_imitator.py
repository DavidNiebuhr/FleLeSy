#!/usr/bin/env python
import rospy
from FleLeSy.srv import *
from std_msgs.msg import String

RobotName = "ThisRobot"
currently_working = False  # working = True


def Interpolate(SRV):  # SRV=ServiceResponseValues
    global currently_working
    currently_working = True
    rospy.loginfo("R: Moving to point\nX: %s\nY: %s\nZ: %s\n with interpolation" % (
        SRV.target.X, SRV.target.Y, SRV.target.Z))
    rospy.sleep(10)
    currently_working = False
    return AuftragResponse(True)


def publish_robot_state():
    # Publish endeffektor position
    # Publish if working or resting
    pub = rospy.Publisher('%s/working_or_resting' % rospy.get_name(), String, queue_size=10)  # working = True
    r = rospy.Rate(1)  # 10hz
    while not rospy.is_shutdown():
        pub.publish(str(currently_working))
        r.sleep()
    pass


def offer_services():
    rospy.Service('%s/interpolate' % rospy.get_name(), Auftrag, Interpolate)
    rospy.loginfo("R: Interpolation is available")
    rospy.Service('%s/milling' % rospy.get_name(), Auftrag, Interpolate)
    rospy.loginfo("R: Milling is available")
    rospy.Service('%s/pic_and_place' % rospy.get_name(), Auftrag, Interpolate)
    rospy.loginfo("R: Pick and place is available")


def register_robot_func():
    global response
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
    rospy.init_node(RobotName)  # , log_level=rospy.DEBUG
    rospy.loginfo("R: Roboternode %s is Running. I'll look out for the registration Service." % rospy.get_name())
    register_robot_func()
    offer_services()
    publish_robot_state()
    rospy.spin()


if __name__ == '__main__':
    app_main()  # Den Grund warum das extra als Funktion aufgerufen wird, habe ich noch nicht verstanden.

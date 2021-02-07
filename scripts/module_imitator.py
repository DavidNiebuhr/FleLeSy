#!/usr/bin/env python

import uuid
import roslaunch
import rospy
from FleLeSy.srv import *
from start_a_node import start_a_node

Affiliated_Robots = []  # list of identification numbers of robots on platform


class Robot:
    def __init__(self, package, executable, name):
        self.identification = "r%s" % str(uuid.uuid4()).replace("-", "_")
        self.package = package
        self.executable = executable
        self.name = name
        Affiliated_Robots.append(self.identification)

    def start_robot_exe(self, launch):
        start_a_node(launch, self.package, self.executable, self.name)

        """ namespace = self.identification
        exe = roslaunch.core.Node(self.package, self.executable, self.name, namespace)
        process = launch.launch(exe)"""


def regist_module():
    global response
    rospy.wait_for_service('/control_system/register_module')
    try:
        register = rospy.ServiceProxy('/control_system/register_module', register_module)
        response = register(rospy.get_name(), Affiliated_Robots)
    except rospy.ServiceException as e:
        rospy.logerr("M: Error during registration:\n%s" % e)
        response.success = False
    if response.success:
        rospy.loginfo("M: The control system confirmed the registration.")
    else:
        rospy.logwarn(
            "M: Something seem to be wrong here.")


def app_main():
    rospy.init_node("Where will this appear?")
    """uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
    roslaunch.configure_logging(uuid.replace("-","_"))
    launch = roslaunch.parent.ROSLaunchParent(uuid,
                                           ["/home/david/catkin_ws/src/kuka210_moveit_config/launch/demo.launch"])
    launch.start()"""

    launch = roslaunch.scriptapi.ROSLaunch()
    launch.start()
    rospy.sleep(0.1)
    """simrobot1 = Robot("kuka210_moveit_config", "demo.launch", "KUKA_kr210")
    simrobot1.start_robot_exe(launch)"""
    robot1 = Robot("FleLeSy", "robot_imitator.py", rospy.get_name())
    robot1.start_robot_exe(launch)
    rospy.sleep(0.2)
    robot2 = Robot("FleLeSy", "robot_imitator.py", rospy.get_name())
    robot2.start_robot_exe(launch)
    rospy.loginfo("M: All Robots of %s should be running." % rospy.get_name())
    rospy.sleep(0.7)
    rospy.loginfo("M: I'll register myself and will tell which robots are on this plattform.")
    # Anmeldevorgang
    regist_module()
    rospy.loginfo("M: Registration complete")
    rospy.spin()


if __name__ == '__main__':
    app_main()

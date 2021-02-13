#!/usr/bin/env python
import json
import os
import uuid
import roslaunch
import rospy
import std_msgs
from FleLeSy.srv import *
from start_a_node import start_a_node

Affiliated_Robots = []  # list of identification numbers of robots on platform
module_position = [0, 0]


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


"""def publish_robot_state():
    while not rospy.is_shutdown():
        r = rospy.Rate(1)  # 10hz
        wor = rospy.Publisher('%s/working' % rospy.get_name(), std_msgs.msg.Bool,
                              queue_size=10)  # working = True
        wor.publish(module_position)
        r.sleep()"""


def start_particular_oe(launch, name, namespace):
    node = roslaunch.core.Node("FleLeSy", "robot_imitator.py", name, namespace, output="screen")
    launch.launch(node)


def start_all_oe(launch, config_data):
    types_and_positions = config_data[0]
    type_description = config_data[1]
    place_in_config_list = int(rospy.get_name()[3])
    type_of_this_module = types_and_positions[place_in_config_list].get("Type")
    rospy.logdebug("This Module has number %s and is a %s platform" % (rospy.get_name()[3], type_of_this_module))
    type_description_of_this_module = type_description.get(type_of_this_module)
    oe_of_this_module = type_description_of_this_module.get("operating_elements")
    rospy.logdebug(oe_of_this_module)
    for oe in range(0, len(oe_of_this_module)):
        start_particular_oe(launch,
                            "oe%s_" % oe + str(uuid.uuid4()).replace("-", "_"), rospy.get_name())


def app_main():
    rospy.init_node("Where will this appear?", log_level=rospy.DEBUG)
    launch = roslaunch.scriptapi.ROSLaunch()
    launch.start()
    rospy.sleep(0.1)

    # Open configuration file:
    this_folder = os.path.dirname(os.path.abspath(__file__))
    my_file = os.path.join(this_folder, 'configuration_file.json')
    file = open(my_file, "r")
    json_string = file.read()
    config_data = json.loads(json_string)

    # start operation entities
    start_all_oe(launch, config_data)

    """robot1 = Robot("FleLeSy", "robot_imitator.py", rospy.get_name())
    robot1.start_robot_exe(launch)
    rospy.sleep(0.2)
    robot2 = Robot("FleLeSy", "robot_imitator.py", rospy.get_name())
    robot2.start_robot_exe(launch)"""
    rospy.loginfo("M: All Robots of %s should be running." % rospy.get_name())
    rospy.sleep(0.5)
    # Anmeldevorgang
    regist_module()
    rospy.loginfo("M: Registration complete")
    rospy.spin()


if __name__ == '__main__':
    app_main()

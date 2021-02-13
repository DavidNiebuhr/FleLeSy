#!/usr/bin/env python
import json
import os
import uuid
import roslaunch
import rospy
from FleLeSy.srv import *

"""
Abbreviations:
CS = control system
fm = fabrication module
OE = operating element
"""

affiliated_oe_id_list = []
position_of_this_fm = []


def publish_fm_pose():
    while not rospy.is_shutdown():
        r = rospy.Rate(0.5)
        fm_pos = rospy.Publisher('%s/platform_pose' % rospy.get_name(), geometry_msgs.msg.Pose2D, queue_size=10)
        fm_pos.publish(position_of_this_fm[0], position_of_this_fm[1], position_of_this_fm[2])
        r.sleep()


def publish_fm_state(config_data):
    type_of_fm = config_data[0][int(rospy.get_name()[3])].get("Type")
    topics = config_data[1].get(type_of_fm).get("Topics")
    if "pose" in topics:
        publish_fm_pose()
    # other states may follow


def register_fm_at_cs():
    global response
    rospy.wait_for_service('/control_system/register_module')
    try:
        register = rospy.ServiceProxy('/control_system/register_module', register_module)
        response = register(rospy.get_name(), affiliated_oe_id_list)
    except rospy.ServiceException as e:
        rospy.logerr("M: Error during registration:\n%s" % e)
        response.success = False
    if response.success:
        rospy.loginfo("M: The control system confirmed the registration.")
    else:
        rospy.logwarn(
            "M: Something seem to be wrong here.")


def start_particular_oe(launch, name, namespace):
    node = roslaunch.core.Node("FleLeSy", "robot_imitator.py", name, namespace)  # , output="screen")
    launch.launch(node)
    affiliated_oe_id_list.append(str(namespace) + "/" + str(name))


def start_all_oe(launch, config_data):
    # Divide configuration_file into two parts:
    types_and_positions = config_data[0]
    type_description = config_data[1]

    # Whats the type of this FM
    place_in_config_list = int(rospy.get_name()[3])
    type_of_this_module = types_and_positions[place_in_config_list].get("Type")

    # call start every OE that is on such type of FM
    type_description_of_this_module = type_description.get(type_of_this_module)
    oe_of_this_module = type_description_of_this_module.get("operating_elements")
    rospy.logdebug(oe_of_this_module)
    for oe in range(0, len(oe_of_this_module)):
        start_particular_oe(launch,
                            "oe%s_" % oe + str(uuid.uuid4()).replace("-", "_"), rospy.get_name())


def app_main():
    # Initialize Node, prepare launch
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

    # initial getting position from config file
    global position_of_this_fm
    types_and_positions = config_data[0]
    place_in_config_list = int(rospy.get_name()[3])
    position_of_this_fm = types_and_positions[place_in_config_list].get("Position")

    # start operation entities
    start_all_oe(launch, config_data)
    rospy.sleep(0.5)

    # register at the control system
    register_fm_at_cs()

    # publish information about this modules status
    publish_fm_state(config_data)

    # that's all for now
    rospy.spin()


if __name__ == '__main__':
    app_main()

#!/usr/bin/env python
import json
import os

import roslaunch
import rospy
from FleLeSy.srv import *
from std_msgs.msg import std_msgs

"""
Abbreviations:
CS = control system
fm = fabrication module
OE = operating element
"""

RobotName = "ThisRobot"
currently_working = False  # working = True
gripper_open = False
nail_gun_ready = False
x = 0.0
y = 0.0
z = 0.0
oe_position = [x, y, z]


def move_x_to(x_target):
    while x_target > (oe_position[0] + 0.05):
        oe_position[0] += 0.1
        rospy.sleep(0.01)
    while (oe_position[0] - 0.05) > x_target:
        oe_position[0] -= 0.1
        rospy.sleep(0.01)
    return True


def move_y_to(y_target):
    while y_target > (oe_position[1] + 0.05):
        oe_position[1] += 0.1
        rospy.sleep(0.01)
    while (oe_position[1] - 0.05) > y_target:
        oe_position[1] -= 0.1
        rospy.sleep(0.01)
    return True


def move_z_to(z_target):
    while z_target > (oe_position[2] + 0.05):
        oe_position[2] += 0.1
        rospy.sleep(0.01)
    while (oe_position[2] - 0.05) > z_target:
        oe_position[2] -= 0.1
        rospy.sleep(0.01)
    return True


def move_to(x_target, y_target, z_target):
    x_done = move_x_to(x_target)
    y_done = move_y_to(y_target)
    z_done = move_z_to(z_target)
    while not x_done or not y_done or not z_done:
        rospy.sleep(1)
    return True


def interpolate(SRV, this_service):  # SRV=ServiceResponseValues
    global currently_working
    rospy.loginfo("R: Moving to point\nX: %s\nY: %s\nZ: %s\n with interpolation" % (
        SRV.target.X, SRV.target.Y, SRV.target.Z))
    arrived = move_to(SRV.target.X, SRV.target.Y, SRV.target.Z)
    while not arrived:
        currently_working = True
        rospy.sleep(1)
    currently_working = False
    return eval(this_service.get("srv_file") + str("Response"))(True)


def point2point(SRV, this_service):
    global currently_working
    rospy.loginfo("R: Moving to point\nX: %s\nY: %s\nZ: %s\n with interpolation" % (
        SRV.target.X, SRV.target.Y, SRV.target.Z))
    arrived = move_to(SRV.target.X, SRV.target.Y, SRV.target.Z)
    while not arrived:
        currently_working = True
        rospy.sleep(1)
    currently_working = False
    return eval(this_service.get("srv_file") + str("Response"))(True)


def start_spindle(SRV, this_service):
    global nail_gun_ready
    spindle_on_status = True
    global currently_working
    currently_working = True
    return eval(this_service.get("srv_file") + str("Response"))(True)


def stop_spindle(SRV, this_service):
    global nail_gun_ready
    spindle_on_status = False
    global currently_working
    currently_working = False
    return eval(this_service.get("srv_file") + str("Response"))(True)


def open_gripper(SRV, this_service):
    global currently_working
    currently_working = True
    global gripper_open
    gripper_open = True
    rospy.sleep(2)
    currently_working = False
    return eval(this_service.get("srv_file") + str("Response"))(True)


def close_gripper(SRV, this_service):
    global currently_working
    currently_working = True
    global gripper_open
    gripper_open = False
    rospy.sleep(2)
    currently_working = False
    return eval(this_service.get("srv_file") + str("Response"))(True)


def offer_services(this_oe_data):
    this_oe_services = this_oe_data.get("Services")
    for service in range(0, len(this_oe_services)):
        this_service = this_oe_services[service]
        rospy.logdebug(this_service)
        rospy.Service('%s/%s' % (rospy.get_name(), this_service.get("Name")),
                      eval(this_service.get("srv_file")), eval(this_service.get("callback")), this_service)

    """rospy.Service('%s/point2point' % rospy.get_name(), Auftrag, interpolate)
    rospy.logdebug("R: Milling is available")"""


def publish_robot_state(this_oe_data):
    this_oe_topics = this_oe_data.get("Topics")
    while not rospy.is_shutdown():
        r = rospy.Rate(1)  # 10hz
        if "working" in this_oe_topics:
            wor = rospy.Publisher('%s/working' % rospy.get_name(), std_msgs.msg.Bool,
                                  queue_size=10)  # working = True
            wor.publish(currently_working)
        if "end_effector_position" in this_oe_topics:
            ee_pos = rospy.Publisher('%s/end_effector_position' % rospy.get_name(), geometry_msgs.msg.Point,
                                     queue_size=10)
            ee_pos.publish(oe_position[0], oe_position[1], oe_position[2])
        if "gripper_open" in this_oe_topics:
            go = rospy.Publisher('%s/gripper_open' % rospy.get_name(), std_msgs.msg.Bool, queue_size=10)  # open = True
            go.publish(gripper_open)
        if "spindle_on" in this_oe_topics:
            so = rospy.Publisher('%s/spindle_on' % rospy.get_name(), std_msgs.msg.Bool, queue_size=10)  # on = True
            so.publish(nail_gun_ready)
        r.sleep()


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


def start_child_nodes(this_oe_data):
    child_nodes = this_oe_data.get("Nodes")
    launch = roslaunch.scriptapi.ROSLaunch()
    launch.start()
    for i in range(0, len(child_nodes)):
        split = child_nodes[i].split(".", 1)
        node = roslaunch.core.Node("FleLeSy", child_nodes[i], split[0], namespace=rospy.get_name())  # , output="screen")
        launch.launch(node)


def app_main():
    rospy.init_node(RobotName, log_level=rospy.DEBUG)

    # Open configuration file:
    this_folder = os.path.dirname(os.path.abspath(__file__))
    my_file = os.path.join(this_folder, 'configuration_file.json')
    file = open(my_file, "r")
    json_string = file.read()
    config_data = json.loads(json_string)

    # Get the data of this OE:
    place_in_config_list = int(rospy.get_name()[3])
    type_of_affiliated_fm = config_data[0][place_in_config_list].get("Type")
    oe_list_of_affiliated_fm = config_data[1].get(type_of_affiliated_fm).get("operating_elements")
    this_oe_data = oe_list_of_affiliated_fm[int(rospy.get_name()[44])]
    # rospy.logdebug(this_oe_data)

    start_child_nodes(this_oe_data)

    # register_robot_func()
    # offer_services(this_oe_data)
    # publish_robot_state(this_oe_data)
    rospy.spin()


if __name__ == '__main__':
    app_main()

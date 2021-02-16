#!/usr/bin/env python
import json
import os
import uuid
import roslaunch
import rospy


def start_node(launch, python_program, identification, namespace=None):
    node = roslaunch.core.Node("FleLeSy", python_program, identification, namespace, output="screen")
    launch.launch(node)


def start_oe_child_nodes(launch, this_oe, oe_id):
    oe_child_nodes = this_oe.get("OE_Nodes")
    for node in range(0, len(oe_child_nodes)):
        node_name = oe_child_nodes[node].split(".", 1)[0]
        start_node(launch, oe_child_nodes[node], node_name, oe_id)


def start_operating_elements(launch, this_fm_type, fm_id):
    oe_list = this_fm_type.get("operating_elements")
    for oe in range(0, len(oe_list)):
        oe_id = "oe%s_" % oe + str(uuid.uuid4()).replace("-", "_")
        #start_node(launch, "robot_imitator.py", oe_id, fm_id)
        start_oe_child_nodes(launch, oe_list[oe], fm_id + "/" + oe_id, )


"""
def start_fm_child_nodes(launch, this_fm_type, fm_id):
    child_nodes = this_fm_type.get("FM_Nodes")
    for node in range(0, len(child_nodes)):
        node_name = child_nodes[node].split(".", 1)[0]
        start_node(launch, child_nodes[node], node_name, fm_id)
"""


def start_validation_sim(launch, types_and_positions, type_description):
    for fm in range(0, len(types_and_positions)):
        fm_id = "fm%s_" % fm + str(uuid.uuid4()).replace("-", "_")
        start_node(launch, "module_imitator.py", fm_id)
        this_fm_type = type_description.get(types_and_positions[fm].get("Type"))
        # start_fm_child_nodes(launch, this_fm_type, fm_id)
        start_operating_elements(launch, this_fm_type, fm_id)


def get_configuration_data():
    # Find config file (independent of which computer this was pulled on):
    this_folder = os.path.dirname(os.path.abspath(__file__))
    my_file = os.path.join(this_folder, 'configuration_file.json')

    # Read File
    file = open(my_file, "r")
    json_string = file.read()
    config_data = json.loads(json_string)
    return config_data


def app_main():
    rospy.sleep(0.1)  # Let control system start first
    rospy.init_node("start_modules")  # , log_level=rospy.DEBUG)
    # Preparation:
    launch = roslaunch.scriptapi.ROSLaunch()
    launch.start()

    # Read config file and split into the two main parts
    config_data = get_configuration_data()
    types_and_positions = config_data[0]
    type_description = config_data[1]

    # Main task:
    start_validation_sim(launch, types_and_positions, type_description)

    # Enter spin to keep subnodes alive
    rospy.spin()


if __name__ == '__main__':
    app_main()

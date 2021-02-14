#!/usr/bin/env python
import json
import os
import uuid
import roslaunch
import rospy


def start_particular_fm(launch, name):
    node = roslaunch.core.Node("FleLeSy", "module_imitator.py", name, output="screen")
    launch.launch(node)


def start_all_fm(launch):
    # Find config file (independent of which computer this was pulled on):
    this_folder = os.path.dirname(os.path.abspath(__file__))
    my_file = os.path.join(this_folder, 'configuration_file.json')

    # Read and split File
    file = open(my_file, "r")
    json_string = file.read()
    config_data = json.loads(json_string)
    # splitting into the two main subdivisions:
    types_and_positions = config_data[0]
    type_description = config_data[1]

    # Start every fm
    for fm in range(0, len(types_and_positions)):
        start_particular_fm(launch,
                            "fm%s_" % fm + str(uuid.uuid4()).replace("-", "_"))


def app_main():
    rospy.sleep(0.1)  # Let control system start first
    rospy.init_node("start_modules", log_level=rospy.DEBUG)
    # Preparation:
    launch = roslaunch.scriptapi.ROSLaunch()
    launch.start()

    # Main task:
    start_all_fm(launch)

    # Enter spin to keep subnodes alive
    rospy.spin()


if __name__ == '__main__':
    app_main()

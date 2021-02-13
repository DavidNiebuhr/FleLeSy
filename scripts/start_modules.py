#!/usr/bin/env python
import json
import os
import uuid
import roslaunch
import rospy


def start_particular_module(launch, package, executable, name):
    node = roslaunch.core.Node(package, executable, name, output="screen")
    launch.launch(node)


def start_all_modules(launch):
    this_folder = os.path.dirname(os.path.abspath(__file__))
    my_file = os.path.join(this_folder, 'configuration_file.json')

    file = open(my_file, "r")
    json_string = file.read()
    config_data = json.loads(json_string)
    # splitting into the two main subdivisions:
    types_and_positions = config_data[0]
    type_description = config_data[1]
    for fm in range(0, len(types_and_positions)):
        start_particular_module(launch, "FleLeSy", "module_imitator.py",
                                "fm%s_" % fm + str(uuid.uuid4()).replace("-", "_"))


def app_main():
    rospy.sleep(0.2)
    rospy.init_node("start_modules", log_level=rospy.DEBUG)
    launch = roslaunch.scriptapi.ROSLaunch()
    launch.start()
    start_all_modules(launch)
    rospy.spin()


if __name__ == '__main__':
    app_main()

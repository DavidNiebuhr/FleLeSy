#!/usr/bin/env python
import sys
import uuid
import roslaunch
import rospy
from query_kill import query_kill


def start_exe(launch, package, executable, name, identification):
    namespace = identification
    node = roslaunch.core.Node(package, executable, name, namespace)
    process = launch.launch(node)

    while rospy.is_shutdown():
        process.stop()


def app_main():
    launch = roslaunch.scriptapi.ROSLaunch()
    launch.start()
    sys.stdout.write("\nroscore up and running")
    rospy.sleep(0.1)
    identification = str(uuid.uuid4())
    start_exe(launch, "FleLeSy", "test.py", "testnode", identification)

    sys.stdout.write("\nAll modules are running")
    while not query_kill("\nKill /roscore and all processes?"):
        rospy.sleep(1)


if __name__ == '__main__':
    app_main()

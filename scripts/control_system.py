#!/usr/bin/env python
import json
from xml.etree import ElementTree
from FleLeSy.srv import *
from geometry_msgs.msg import Point
from rosservice import *
# from FleLeSy.docs import Milling.xml
from queries import *
import os

"""
Abbreviations:
CS = control system
fm = fabrication module
OE = operating element
"""


AllModules = []  # change to set?
AllRobots = []  # change to set?
x = 3.3
y = -1.9
z = 112.3

# Milling_step_tuple = (call_point2point(), spindle_start, call_interpolate, spindle_stop, resting_postition)
# Nailing_step_tuple = (call_point2point, shoot_nail, resting_position)


"""class Task:
    def __init__(self, starting_point, task_list, target_point):
        self.starting_point = starting_point
        self.task_list = task_list
        self.target_point = target_point
        task0 = task_list(0)
        task0(starting_point)"""


class Robot:
    def __init__(self, RobotID, AffiliatedModuleID):
        self.RobotID = RobotID
        self.robot_name = "NoNameGiven"
        self.AffiliatedModuleID = AffiliatedModuleID
        AllRobots.append(self)

    """def call_interpolate(self, ix, iy, iz):
        rospy.wait_for_service('%s/interpolate' % self.RobotID)
        rospy.loginfo("calling interpolate now")
        try:
            interp = rospy.ServiceProxy('%s/interpolate' % self.RobotID, Interpolate)
            resp1 = interp(Point(ix, iy, iz))
            return resp1.success
        except rospy.ServiceException as e:
            print("Service call failed: %s" % e)

    def call_point2point(self, x, y, z):
        rospy.wait_for_service('%s/point2point' % self.RobotID)
        rospy.loginfo("calling point2point now")
        try:
            p2p = rospy.ServiceProxy('%s/point2point' % self.RobotID, Interpolate)
            resp1 = p2p(x, y, z)
            return resp1.success
        except rospy.ServiceException as e:
            print("Service call failed: %s" % e)

    def resting_position(self):
        return self.call_point2point(x=0, y=20, z=500)"""


def milling(robot_id, start_point, target_point):
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    my_file = os.path.join(THIS_FOLDER, 'milling.json')

    file = open(my_file, "r")
    json_string = file.read()
    json_data = json.loads(json_string)
    rospy.logdebug(json_data)

    for i in range(0, len(json_data)):
        try:
            rospy.loginfo('%s%s' % (json_data[i].get("Service"), i))
            interp = rospy.ServiceProxy('%s%s' % (robot_id, json_data[i].get("Service")), Interpolate)
            rospy.logdebug(start_point)
            resp1 = interp(Point(start_point))
            while not resp1:
                rospy.sleep(1)
        except rospy.ServiceException as e:
            print("Service call failed: %s" % e)


def search_for_robot(ID):
    for i in range(0, len(AllRobots)):
        if AllRobots[i].ID == ID:  # ID ausstehend
            return AllRobots[i]
    # gives back Object of class Robot, that has the ID that was asked for


class Module:

    def __init__(self, ModuleID, AffiliatedRobots):  # Erstelle ein Objekt der Klasse Module
        self.ModuleName = "NoNameGiven"
        self.ModuleID = ModuleID
        self.Robots = AffiliatedRobots
        rospy.loginfo("CS: A new Module is registered: %s" % self.ModuleID)
        # self.ModuleAlias = queries.query_alias("Please give %s a nickname" % ModuleName)
        AllModules.append(self)
        """for x in range(len(AllModules)):
            rospy.loginfo("CS: All Modules that are currently registered:\n" + AllModules[x].ModuleID)
"""


class Registry:
    def __init__(self):
        pass

    def new_module(self, SRV):  # Function to register a new module #SRV=ServiceResponseValues
        rospy.logdebug("CS: I'll now create an object for the new Module")
        Module(SRV.ModuleID, SRV.AffiliatedRobots)
        rospy.logdebug("CS: Done.")
        return register_moduleResponse(True)

    def new_robot(self, SRV):  # Function to register a new robot #SRV=ServiceResponseValues
        rospy.logdebug("CS: I'll now create an object for the new Robot")
        Robot(SRV.RobotID, SRV.AffiliatedModuleID)
        rospy.logdebug("CS: Done.")
        return register_robotResponse(True)


"""def search_for_module(Identification):
    for i in range(0, len(AllModules)):
        if AllModules[i].ID == Identification:  # ID ausstehend
            return AllModules[i]
    # gives back Object of class Module, that has the ID that was asked for
"""


def service_selection(chosen_robot):
    sys.stdout.write("The chosen Robots offers the following services:\n\n")
    service_list = get_service_list(include_nodes=False)
    this_robot_service_list = []
    for i in range(0, len(service_list)):
        if service_list[i].startswith(AllRobots[chosen_robot].RobotID):
            this_robot_service_list.append(service_list[i])
    for j in range(0, len(this_robot_service_list)):
        sys.stdout.write("[%s] " % j + this_robot_service_list[j] + "\n")
    chosen_service_nr = query_number("\nChoose a service.", 0, len(this_robot_service_list))
    chosen_service = this_robot_service_list[chosen_service_nr]
    rospy.logdebug("User chose:\n" + str(chosen_service))
    if "interpolate" in str(chosen_service):
        milling()


def robot_selection(chosen_module):
    sys.stdout.write("The following robots are on the chosen module and available:\n")
    this_module_robot_list = []
    for i in range(0, len(AllRobots)):
        # An Alternative solution would be to just use the AffiliatedRobot List
        # If this won't be used I can leave it out of the regisitration srv/msg.
        rospy.logdebug("Vergleiche %s mit %s." % (AllRobots[i].AffiliatedModuleID, AllModules[chosen_module].ModuleID))
        if AllRobots[i].AffiliatedModuleID == AllModules[chosen_module].ModuleID:
            this_module_robot_list.append(AllRobots[i].RobotID)
    for j in range(0, len(this_module_robot_list)):
        sys.stdout.write("[%s] " % j + this_module_robot_list[j] + "\n")
    chosen_robot = query_number("\nChoose the robot.", 0, len(AllRobots))
    rospy.logdebug("User chose: " + str(chosen_robot))
    sys.stdout.write("CS: You chose\n" + str(AllRobots[chosen_robot].RobotID) + "\n\n")
    service_selection(chosen_robot)


def module_selection():
    sys.stdout.write("The following modules are available:\n")
    for i in range(0, len(AllModules)):
        sys.stdout.write("[%s] " % i + AllModules[i].ModuleID + "\n")
    chosen_module = query_number("\nChoose the module.", 0, len(AllModules))
    rospy.logdebug("User chose: " + str(chosen_module))
    sys.stdout.write("CS: You chose\n" + str(AllModules[chosen_module].ModuleID) + "\n\n")
    robot_selection(chosen_module)


def json_stuff():  # /home/david/catkin_ws/src/FleLeSy/docs/
    this_folder = os.path.dirname(os.path.abspath(__file__))
    my_file = os.path.join(this_folder, 'milling.json')

    handle = open(my_file, "r")
    content = handle.read()
    content_handle = json.loads(content)
    rospy.logdebug(content_handle)
    rospy.loginfo(content_handle[0])
    first_service = content_handle[0].get("Service")
    rospy.loginfo(first_service)


def app_main():
    rospy.init_node('control_system')  # , log_level=rospy.DEBUG)
    registry = Registry()
    rospy.Service('control_system/register_module', register_module, registry.new_module)
    rospy.Service('control_system/register_robot', register_robot, registry.new_robot)
    rospy.loginfo("Control System is online and ready for registration requests!")
    rospy.sleep(5)
    # rospy.loginfo(AllRobots[0].RobotID)
    # milling(AllRobots[0].RobotID, ([1, 1, 1]), [2, 2, 2])
    # json_stuff()
    # module_selection()
    # rospy.loginfo("These are all Robots: %s \n" % AllRobots[0].RobotID)
    rospy.spin()


if __name__ == '__main__':
    app_main()

#!/usr/bin/env python

import rospy
import sys
from FleLeSy.srv import *
from queries import *
from rosservice import *

AllModules = []
AllRobots = []


class Robot:
    def __init__(self, RobotID, AffiliatedModuleID):
        self.RobotID = RobotID
        self.robotname = "NoNameGiven"
        self.AffiliatedModuleID = AffiliatedModuleID
        AllRobots.append(self)


def search_for_robot(ID):
    for i in range(0, len(AllRobots)):
        if AllRobots.ID == ID:  # ID ausstehend
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
        for x in range(len(AllModules)):
            rospy.loginfo("CS: All Modules that are currently registered:\n" + AllModules[x].ModuleID)


def search_for_module(Identification):
    for i in range(0, len(AllModules)):
        if AllModules.ID == Identification:  # ID ausstehend
            return AllModules[i]
    # gives back Object of class Module, that has the ID that was asked for


def service_selection(chosen_robot):
    sys.stdout.write("The chosen Robots offers the following services:\n\n")
    service_list = map(str, get_service_list(include_nodes=False))
    this_robot_service_list = []
    for i in range(0, len(service_list)):
        if service_list[i].startswith(AllRobots[chosen_robot].RobotID):
            this_robot_service_list.append(service_list[i])
    for j in range(0, len(this_robot_service_list)):
        sys.stdout.write("[%s] " % j + this_robot_service_list[j] + "\n")
    chosen_service_nr = query_number("\nChoose a service.", 0, len(this_robot_service_list))
    chosen_service = this_robot_service_list[chosen_service_nr]
    rospy.loginfo("User chose:\n" + str(chosen_service))
    sys.stdout.write("The following arguments are needed:\n")
    rospy.loginfo(get_service_args(chosen_service))
    rospy.loginfo(type(chosen_service))
    rospy.loginfo(get_service_type(chosen_service))
    rospy.loginfo(get_service_uri(chosen_service))

def robot_selection(chosen_module):
    sys.stdout.write("The following robots are on the chosen module and available:\n")
    for i in range(0, len(AllRobots)):
        # An Alternative solution would be to just use the AffiliatedRobot List
        # would be better because the numbers would start by 0...
        # If this won't be used I can leave it out of the regisitration srv/msg.
        if AllRobots[i].AffiliatedModuleID == AllModules[chosen_module].ModuleID:
            sys.stdout.write("[%s] " % i + AllRobots[i].RobotID + "\n")
    chosen_robot = query_number("\nChoose the robot.", 0, len(AllRobots))
    rospy.loginfo("User chose: " + str(chosen_robot))
    sys.stdout.write("CS: You chose\n" + str(AllRobots[chosen_robot].RobotID) + "\n\n")
    service_selection(chosen_robot)


def module_selection():
    sys.stdout.write("The following modules are available:\n")
    for i in range(0, len(AllModules)):
        sys.stdout.write("[%s] " % i + AllModules[i].ModuleID + "\n")
    chosen_module = query_number("\nChoose the module.", 0, len(AllModules))
    rospy.loginfo("User chose: " + str(chosen_module))
    sys.stdout.write("CS: You chose\n" + str(AllModules[chosen_module].ModuleID) + "\n\n")
    robot_selection(chosen_module)


def NewModule(SRV):  # Function to register a new module #SRV=ServiceResponseValues
    rospy.loginfo("CS: I'll now create an object for the new Module")
    Module(SRV.ModuleID, SRV.AffiliatedRobots)
    rospy.loginfo("CS: Done.")
    return register_moduleResponse(True)


def NewRobot(SRV):  # Function to register a new robot #SRV=ServiceResponseValues
    rospy.loginfo("CS: I'll now create an object for the new Robot")
    Robot(SRV.RobotID, SRV.AffiliatedModuleID)
    rospy.loginfo("CS: Done.")
    return register_robotResponse(True)


def app_main():
    rospy.init_node('control_system')  # , log_level=rospy.DEBUG
    rospy.Service('control_system/register_module', register_module, NewModule)
    rospy.Service('control_system/register_robot', register_robot, NewRobot)
    rospy.loginfo("Control System is online and ready for registration requests!")
    rospy.sleep(5)
    # service_list = map(str, get_service_list(node=None, namespace=None, include_nodes=False))
    """rospy.loginfo("Those are all services available on the system: \n\n%s\n" % ",\n".join(
        service_list))"""
    module_selection()
    # rospy.loginfo("These are all Robots: %s \n" % AllRobots[0].RobotID)
    rospy.spin()


if __name__ == '__main__':
    app_main()

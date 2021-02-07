#!/usr/bin/env python

import rospy
import sys
from FleLeSy.srv import *
from queries import *
from rosservice import get_service_list

AllModules = []
AllRobots = []


class Robot:
    # Attribute der Klasse Robot

    # Muss zu genau einem Modul gehoeren
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


def step_by_step_service_selection():
    sys.stdout.write("The following modules are available:\n")
    for i in range(0, len(AllModules)):
        sys.stdout.write("[%s] " % i + AllModules[i].ModuleID + "\n")
    chosen_module = query_number("Choose the module.", 0, len(AllModules))
    rospy.loginfo("User chose: " + str(chosen_module))
    sys.stdout.write("You chose\n" + str(AllModules[chosen_module].ModuleID) + "\n")


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
    rospy.init_node('control_system')
    # , log_level=rospy.DEBUG)  # Sorgt dafuer dass der Code als Node existiert und gibt ihm den Namen Leitsystem
    rospy.Service('control_system/register_module', register_module, NewModule)
    rospy.Service('control_system/register_robot', register_robot, NewRobot)
    rospy.loginfo("Control System is online and ready for registration requests!")
    rospy.sleep(5)
    # service_list = map(str, get_service_list(node=None, namespace=None, include_nodes=False))
    """rospy.loginfo("Those are all services available on the system: \n\n%s\n" % ",\n".join(
        service_list))"""
    step_by_step_service_selection()
    rospy.spin()


if __name__ == '__main__':
    app_main()

"""
class Module:
    #Attribute der Klasse Robo:
    #topic = None
    #pub = None
    #Funktionen der Klasse Robo:
    def __init__(self, name): #Erstelle ein Objekt der Klasse Robo
        self.topic = "/" + name + "/action" #Schreibe gleich das fuer ihn vorgesehenene Topic in seine Attribute, damit er darauf zurueckgreifen kann.
        self.pub = rospy.Publisher(self.topic, String, queue_size=10)  #Vermerke in seinen Attributen die Funktion mir der er auf dem fuer ihn vorgesehenen Topic publishen kann.
        #rospy.Publisher creates a "handle" to publish messages to a topic using the rospy.Publisher Class

    def do_action(self, payload):
        self.pub.publish(payload) #Auf dem Topic des Objekts, auf das diese Funktionen angewandt wird, soll die mitgegebene Payload gepublished werden.
"""

"""
class Step:
    # Attribute der Klasse Step:
    robot = None
    payload = None

    # Funktionen der Klasse Step:
    def __init__(self, param_robot, param_parameters):  # Erstelle ein Objekt der Klasse Step
        self.robot = param_robot  # Der Step wird mit dem uebergebenen Roboter...
        self.payload = param_parameters  # ...und dem uebegebenem Parameter (also was machen) ausgefuehrt.
"""

"""
#Pseudocode fuer punkt 7:
def punkt_7(service):
    msg_list = service.getAllMessageTypes()
    print("Available Functions for service1", msg_list)
    #klassischerweise loopt man durch die msg_list und gibt davor eine index nummer aus. Der User muss dann nur eine nummer eintippen
    #bsp output des loops:
    
    [0]: MyFunction1
    [1]: MyFunction2
    ...
    
    msg_type = waitForVALIDIntegerInput() #Um aus der Lite auszuwaehlen
    print("Enter Message:")
    msg = []
    for i in range(0, len(msg_type.parameters)):
        msg[i] = waitForInput()


#speudocode fuer punkt 8:
#sei wfi() = waitForInput()
steps_count = wfi()
all_steps = []
for j in range(0, steps_count):
    #auch hier ist eine liste nicht schlecht....
    service = wfi()
    all_steps[j] = punkt_7(service)

"""

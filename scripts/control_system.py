#!/usr/bin/env python
import uuid

import rospy
from rosservice import get_service_list
from std_msgs.msg import String
from FleLeSy.srv import register_module, register_moduleResponse

MaxNumberOfModules = 100  # Die Maximale Anzahl an Modulen die ueberhaupt verwendet werden koennen. Z.B. Anzahl Montagemoeglichkeiten, lieber zu viel als zu wenig.
AllModules = []
AllRobots = []


class Robot:
    # Attribute der Klasse Robot

    # Muss zu genau einem Modul gehoeren
    def __init__(self, robotname, ID, AffiliatedModule):
        self.ID = ID
        self.robotname = robotname
        self.AffiliatedModule = AffiliatedModule
        AllRobots.append(self)

    def search_for_robot(self):
        for i in range(0, len(AllRobots)):
            if AllRobots.ID == self.ID:  # ID ausstehend
                break
        return AllRobots[i]


class Module:
    def __init__(self, Robots):  # Erstelle ein Objekt der Klasse Module
        rospy.loginfo("Ich erstelle jetzt ein Modul mit dem Namen %s." % self)
        self.Robots = Robot
        AllModules.append(self)

    def search_for_module(self):
        for i in range(0, len(AllModules)):
            if AllModules.ID == self.ID:  # ID ausstehend
                break
        return AllModules[i]


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


def NewModule(SRV):  # Service zur Modulanmeldung #SRV=ServiceResponseValues
    if SRV.ModulName in AllModules:
        rospy.loginfo("Dieses Modul ist bereits angemeldet.")
        rospy.loginfo(
            "Das Modul nimmt Befehle entgegen auf /%s_befehle. Diese Bestehen aus zwei Strings: Zielposition und Wegverhalten" %
            SRV.ModulName)
        return register_moduleResponse(False, SRV.ModulName, AllModules.index(SRV.ModulName))
    else:
        i = 0
        while isinstance(AllModules[i], String):
            i += 1
        AllModules[i] = SRV.ModulName
        # rospy.loginfo("Das Modul %s ist als Objekt verfuegbar. Es hat die Nummer %s in der Liste der Roboter bekommen." % (Modules[i], str(i)))
        rospy.loginfo(
            "Das Modul nimmt Befehle entgegen auf /%s_befehle. Diese Bestehen aus zwei Strings: Zielposition und Wegverhalten" %
            AllModules[i])
        return register_moduleResponse(True, AllModules[i], i)


def app_main():
    rospy.init_node('control_system')  # Sorgt dafuer dass der Code als Node existiert und gibt ihm den Namen Leitsystem
    rospy.Service('%s/register_module' % rospy.get_name(), register_module, NewModule)
    rospy.loginfo("Das Leitsystem ist online und nimmt Modulanmeldungen entgegen!")
    rospy.spin()


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

if __name__ == '__main__':
    app_main()  # Den Grund warum das extra als Funktion aufgerufen wird habe ich noch nicht verstanden.

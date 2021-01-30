#!/usr/bin/env python
import rospy
from std_msgs.msg import String
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

class Step:
    #Attribute der Klasse Step:
    robot = None
    payload = None
    #Funktionen der Klasse Step:
    def __init__(self, param_robot, param_parameters): #Erstelle ein Objekt der Klasse Step
        self.robot = param_robot            #Der Step wird mit dem uebergebenen Roboter...
        self.payload = param_parameters     #...und dem uebegebenem Parameter (also was machen) ausgefuehrt.

Roboter1 = Robo("MyRobot1") #Roboter1 wird hiermit zu einem Objekt der Klasse Robo mit Topic /MyRobot1/action
Roboter2 = Robo("MyRobot2")

step1 = Step(Roboter1, "X:42, Y:42, Type:Kleben") #Fuer einfaches Aufrufen, schreiben wir es in eine Variable
step2 = Step(Roboter2, "length: 5cm")
step3 = Step(Roboter2, "X:43, Y:33, Type: milling")

p = 0
all_steps = [step1, step2, step3]



subber = None
def callback(data):
    global p, all_steps, subber

    if p<len(all_steps): #len() gibt die Laenge des Arrays, das wir als Parameter mitgegeben haben zurueck
        rospy.loginfo("Got Message!")
        all_steps[p].robot.do_action(all_steps[p].payload)
        #An dem akktuellem Objekt der Klasse Step wird die Funktion do_action ausgefuehrt
        #Payload ist ein Atribut der Klasse step --> in diesem Fall ist es der String den wir bei der Instanziierung hineingeben.
        p += 1
    else:
        rospy.loginfo("Wir sind fertig")
        subber.unregister()
    return None
"""

def NewModule(name):
    pub = rospy.Publisher("AddModule", String, queue_size=10)
    rate = rospy.Rate(1)  # 1hz
    while not rospy.is_shutdown():
        AddModule = name
        pub.publish(AddModule)
        rate.sleep()

def app_main():
    global subber
    rospy.init_node('leitsystem') #Sorgt dafuer dass der Code als Node existiert und gibt ihm den Namen Leitsystem
    rospy.loginfo("Das Leitsystem ist online")
    NewModuleName = "KUKAchen"
    NewModule(NewModuleName)


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
    app_main() #Den Grund warum das extra als Funktion aufgerufen wird habe ich noch nicht verstanden.
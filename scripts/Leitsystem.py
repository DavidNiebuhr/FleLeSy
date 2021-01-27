#!/usr/bin/env python
import rospy
from std_msgs.msg import String

class Robo:
    topic = None #rospy.sub(
    pub = None
    def __init__(self, name):
        self.topic = "/" + name + "/action"
        self.pub = rospy.Publisher(self.topic, String, queue_size=10)

    def do_action(self, payload):
        self.pub.publish(payload)

class Step:
    robot = None
    payload = None

    def __init__(self, param_robot, param_parameters):
        self.robot = param_robot
        self.payload = param_parameters



Roboter1 = Robo("MyRobot1")
Roboter2 = Robo("MyRobot2")

step1 = Step(Roboter1, "X:42, Y:42, Type:Kleben")
step2 = Step(Roboter2, "length: 5cm")
step3 = Step(Roboter2, "X:43, Y:33, Type: milling")

p = 0
all_steps = [step1, step2, step3]

subber = None
def callback(data):
    global p, all_steps, subber

    if p<len(all_steps):
        rospy.loginfo("Got Message!")
        all_steps[p].robot.do_action(all_steps[p].payload)
        p += 1
    else:
        rospy.loginfo("Wir sind fertig")
        subber.unregister()
    return None


def app_main():
    global subber
    rospy.init_node('leitsystem', anonymous=True)
    subber = rospy.Subscriber("/StatusOK", String, callback)
    rospy.loginfo("Starting first step.")
    all_steps[0].robot.do_action(all_steps[0].payload)
    global p
    p += 1

    rospy.spin() #wartet auf Nachricht, ruft dann Callback auf


#speudocode für punkt 7:
def punkt_7(service):
    msg_list = service.getAllMessageTypes()
    print("Available Functions for service1", msg_list)
    #klassischerweise loopt man durch die msg_list und gibt davor eine index nummer aus. Der User muss dann nur eine nummer eintippen
    #bsp output des loops:
    """
    [0]: MyFunction1
    [1]: MyFunction2
    ...
    """
    msg_type = waitForVALIDIntegerInput() #Um aus der Lite auszuwählen
    print("Enter Message:")
    msg = []
    for i in range(0, len(msg_type.parameters)):
        msg[i] = waitForInput()


#speudocode für punkt 8:
#sei wfi() = waitForInput()
steps_count = wfi()
all_steps = []
for j in range(0, steps_count):
    #auch hier ist eine liste nicht schlecht....
    service = wfi()
    all_steps[j] = punkt_7(service)



if __name__ == '__main__':
    app_main()
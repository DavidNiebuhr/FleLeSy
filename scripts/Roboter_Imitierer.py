#!/usr/bin/env python
import rospy
from std_msgs.msg import String


class Module:
    # Attribute der Klasse Module:
    #topic = None
    #sub = None
    def __init__(self, name): #Erstelle ein Objekt der Klasse Module
        rospy.loginfo("Ich erstelle jetzt ein Modul mit dem Namen " + str(name) + ".")
        #self.topic = "/" + name + "/action" #Schreibe gleich das fuer ihn vorgesehenene Topic in seine Attribute, damit er darauf zurueckgreifen kann.
        #self.sub = rospy.Subscriber(str(name), String, queue_size=10)  #Vermerke in seinen Attributen die Funktion mir der er auf dem fuer ihn vorgesehenen Topic publishen kann.
        #rospy.Publisher creates a "handle" to publish messages to a topic using the rospy.Publisher Class

def AuftragAusfuehren():
    return None

def callbackAuftragAnRoboter1(data):
    rospy.loginfo("Roboter_1 hat folgenden Auftrag erhalten:" + str(data))
    AuftragAusfuehren()
    rospy.loginfo("Auftrag ist ausgefuehrt. Ich melde das jetzt gleich an das Leitsystem.")
    feedback = rospy.Publisher('/Feedback', String, queue_size=10)
    feedback.publish("Auftrag " + str(data) + "wurde ausgefuehrt")
    rospy.loginfo("Das muesste jetzt angekommen sein. Damit muesste alles abgeschlossen sein.")
    return None

def callbackNeuerRoboter(data):
    Roboter_1 = Module(data)
    rospy.loginfo("Das Modul nimmt Befehle entgegen auf /Roboter1_befehle . Diese Bestehen aus zwei Strings: Zielposition und Wegverhalten")
    rospy.Subscriber("/Roboter1_befehle", String, callbackAuftragAnRoboter1)
    rospy.spin()
    return None



def app_main():
    rospy.Subscriber("/InitModule", String, callbackNeuerRoboter)
    rospy.spin()


if __name__ == '__main__':
    rospy.init_node('roboter_imitierer')
    app_main()  # Den Grund warum das extra als Funktion aufgerufen wird habe ich noch nicht verstanden.
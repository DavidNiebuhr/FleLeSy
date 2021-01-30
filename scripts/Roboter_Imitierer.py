#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from functools import partial

MaxNumberOfModules = 100 #Die Maximale Anzahl an Modulen die überhaupt verwendet werden können. Z.B. Anzahl Montagemöglichkeiten, lieber zu viel als zu wenig.
Modules = [] * MaxNumberOfModules
#AlreadyInitialzedModules = 0
class Module:
    # Attribute der Klasse Module:
    #topic = None
    #sub = None
    def __init__(self, name): #Erstelle ein Objekt der Klasse Module
        rospy.loginfo("Ich erstelle jetzt ein Modul mit dem Namen " + str(name) + ".")
        #self.topic = "/" + name + "/action" #Schreibe gleich das fuer ihn vorgesehenene Topic in seine Attribute, damit er darauf zurueckgreifen kann.
        #self.sub = rospy.Subscriber(str(name), String, queue_size=10)  #Vermerke in seinen Attributen die Funktion mir der er auf dem fuer ihn vorgesehenen Topic publishen kann.
        #rospy.Publisher creates a "handle" to publish messages to a topic using the rospy.Publisher Class
"""
def AuftragAusfuehren():
    return None

def callbackAuftragAnRoboter(data, AlreadyInitialzedModules):
    rospy.loginfo("%s hat folgenden Auftrag erhalten:" % Modules[AlreadyInitialzedModules] + str(data.data))
    AuftragAusfuehren()
    rospy.loginfo("Auftrag ist ausgefuehrt. Ich melde das jetzt gleich an das Leitsystem.")
    feedback = rospy.Publisher('/Feedback', String, queue_size=10)
    feedback.publish("Auftrag " + str(data) + "wurde ausgefuehrt")
    rospy.loginfo("Das muesste jetzt angekommen sein. Damit muesste alles abgeschlossen sein.")
    return None
"""
def callbackNeuerRoboter(data):
    AlreadyInitialzedModules = 0
    Modules[AlreadyInitialzedModules] = Module(data.data)
    rospy.loginfo("Das %s. Modul ist als Objekt verfügbar. Es heißt %s." % AlreadyInitialzedModules, Modules[AlreadyInitialzedModules])
    rospy.loginfo("Das Modul nimmt Befehle entgegen auf /%s_befehle_befehle . Diese Bestehen aus zwei Strings: Zielposition und Wegverhalten" % Modules[AlreadyInitialzedModules])
    #rospy.Subscriber("/%s_befehle" % Modules[AlreadyInitialzedModules], String, partial(callbackAuftragAnRoboter, AlreadyInitialzedModules))
    rospy.spin()
    AlreadyInitialzedModules += 1
    return None

def app_main():
    AlreadyInitialzedModules = 0
    rospy.loginfo("Bereit einen Roboter nachzubilden.")
    rospy.Subscriber("/AddModule", String, callbackNeuerRoboter)
    rospy.spin()


if __name__ == '__main__':
    rospy.init_node('roboter_imitierer')
    app_main()  # Den Grund warum das extra als Funktion aufgerufen wird habe ich noch nicht verstanden.
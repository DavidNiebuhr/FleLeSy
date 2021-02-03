#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from query_yes_no import query_yes_no
from FleLeSy.srv import *


Module_Name = "KUKAchen"
#AmLeitsystemAngemeldet = False


def Interpolate(SRV):  # SRV=ServiceResponseValues
    rospy.loginfo("Ich fahre per Interpolation zu Punkt \nX: %s\nY: %s\nZ: %s" % (
    SRV.Auftrag, SRV.target.X, SRV.target.Y, SRV.target.Z))
    return True


def offer_services():
    rospy.Service('%s/interpolate' % Module_Name, Auftrag, Interpolate)
    rospy.loginfo("Interpolation ist verfuegbar")
    rospy.spin()


def app_main():
    rospy.init_node(Module_Name)
    if query_yes_no("Moechtest du dass ich mich beim Leitsystem unter meinem Namen %s anmelden?" % Module_Name):
        rospy.loginfo("Alles klar, ich melde ihn jetzt an.")
        rospy.wait_for_service('leitsystem/anmeldeservice')
        try:
            Anmeldeservice = rospy.ServiceProxy('leitsystem/anmeldeservice', register_module)
            response = Anmeldeservice(Module_Name)
        except rospy.ServiceException as e:
            rospy.logerr("Anmeldung konnte nicht beantragt werden: %s" % e)
        if response.Erfolg:
            rospy.loginfo("Das Modul ist beim System unter %s bekannt und traegt die Nummer %s" % (
                response.SystemweiterModulName, response.ModuleNumber))
        else:
            rospy.logwarn("Das Leitsystem hat einen Fehler zurueckgemeldet. Wahrscheinlich ist das Modul bereits angemeldet.")
        offer_services()
    else:  # Falls bei der Nachfrage doch Nein gesagt wurde
        rospy.loginfo("Okay, dann nicht.")
    return None


if __name__ == '__main__':
    app_main()  # Den Grund warum das extra als Funktion aufgerufen wird, habe ich noch nicht verstanden.

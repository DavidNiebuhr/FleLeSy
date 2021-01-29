#!/usr/bin/env python

from __future__ import print_function

import sys
import rospy
from FleLeSy.srv import AddTwoInts

def add_two_ints_client(x, y):
    rospy.wait_for_service('add_two_ints') #Wartet bis Service verfuegbar ist. In diesem Fall braucht man das, falls man den Server zuerst startet, damit man nicht schon im Code weiter laeuft.
    try:
        add_two_ints = rospy.ServiceProxy('add_two_ints', AddTwoInts)
        resp1 = add_two_ints(x, y)
        return resp1.sum #Das .sum scheint keinen Nutzen zu haben aber auch keinen Schaden
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)

def usage():
    return "%s [x y]"%sys.argv[0]

if __name__ == "__main__":
    if len(sys.argv) == 3:
        x = int(sys.argv[1])
        y = int(sys.argv[2])
    else:
        print(usage())
        sys.exit(1)
    print("Requesting %s+%s"%(x, y)) # %s fuegt die nachfolgenden Variablen an dieser Stelle, in dieser Reihenfolge ein.
    print("%s + %s = %s"%(x, y, add_two_ints_client(x, y)))
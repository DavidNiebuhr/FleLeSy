#!/usr/bin/env python

from __future__ import print_function
from FleLeSy.srv import *
import rospy

def handle_add_two_ints(req):
    print("Returning [%s + %s = %s]"%(req.a, req.b, (req.a + req.b)))
    return AddTwoIntsResponse(req.a + req.b)

def add_two_ints_server():
    s = rospy.Service('add_two_ints', AddTwoInts, handle_add_two_ints) #Was hat s = für eine Bedeutung? kann man das nicht einfach weglassen. Es wir nirgendwo mehr verwendet.
    #handle_add_two_ints ist eine callback funktion
    print("Ready to add two ints.") #gibt an, dass der Service jetzt zuhoert, ob er aufgerufen wird.
    rospy.spin()

if __name__ == "__main__":
    rospy.init_node('add_two_ints_server')
    add_two_ints_server()

# FleLeSy
Flexible controlsystem for IntCDC



























ROS Namespace:
http://wiki.ros.org/Names
https://www.youtube.com/watch?v=qpwxnzxvbhU Min. 4:30

Rviz:
http://wiki.ros.org/rviz/Tutorials/Interactive%20Markers%3A%20Basic%20Controls 
http://wiki.ros.org/rviz


Wenn Rviz keinen Roboter zeigt:
Schließen, dann in Terminal folgende Zeile eingeben und erneut starten.

export LC_NUMERIC="en_US.UTF-8"

Kuka in RViz starten, dabei Namespace zuweiesen:
roslaunch kuka210_moveit_config demo.launch rviz_tutorial:=true __ns:=kuka_kr210_1

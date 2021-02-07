import roslaunch
import uuid


def start_a_node(launch, package, executable, ModuleID):
    namespace = ModuleID
    name = "r" + str(uuid.uuid4()).replace("-", "_")
    node = roslaunch.core.Node(package, executable, name, namespace) #, output="screen")
    launch.launch(node)

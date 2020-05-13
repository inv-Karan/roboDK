from robolink import *              # import the robolink library (bridge with RoboDK)
RDK = Robolink()                    # establish a link with the simulator
robot = RDK.Item('ABB IRB120')      # retrieve the robot by name
robot.setJoints([0,0,0,0,0,0])      # set all robot axes to zero

target = RDK.Item('Target')         # retrieve the Target item
robot.MoveJ(target)                 # move the robot to the target

# calculate a new approach position 100 mm along the Z axis of the tool with respect to the target
from robodk import *                # import the robodk library (robotics toolbox)
approach = target.Pose()*transl(0,0,-100)
robot.MoveL(approach)               # linear move to the approach position
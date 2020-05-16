# Start the RoboDK API
from robolink import *
from robodk import *
RDK = Robolink()

# Define your new robot or mechanism
# Example to create a Fanuc LR Mate 200iD robot
robot_name = 'Fanuc LR Mate 200iD'
DOFs       = 6

# Define the joints of the robot/mechanism
joints_build = [0, 0, 0, 0, 0, 0]

# Define the home position of the robot/mechanism (default position when you build the mechanism)
# This is also the position the robot goes to if you select "Home"
joints_home   = [0, 0, 0, 0, 0, 0]

# Define the robot parameters. The parameters must be provided in the same order they appear 
#     in the menu Utilities-Model Mechanism or robot
# Some basic mechanisms such as 1 or 2 axis translation/rotation axes don't need any parameters 
#     (translation/rotation will happen around the Z axis)
#parameters = []
parameters = [330, 50, 0, 330, 35, 335, 80, 0, -90, 0, 0, 0, 0]

# Define the joint sense (set to +1 or -1 for each axis (+1 is used as a reference for the ABB IRB120 robot)
joints_senses   = [+1, +1, -1,  -1, -1, -1] # add -1 as 7th index to account for axis 2 and axis 3 coupling

# Joint limits (lower limits for each axis)
lower_limits  = [-170, -100, -67, -190, -125, -360]

# Joint limits (upper limits for each axis)
upper_limits  = [ 170,  145, 213,  190,  125,  360]

# Base frame pose (offset the model by applying a base frame transformation)
#base_pose   = xyzrpw_2_pose([0, 0, 0, 0, 0, 0])
# Fanuc and Motoman robots have the base frame at the intersection of axes 1 and 2
base_pose   = xyzrpw_2_pose([0, 0, -330, 0, 0, 0])

# Tool frame pose (offset the tool flange by applying a tool frame transformation)
tool_pose   = xyzrpw_2_pose([0, 0, 0, 0, 0, 0])

# Retrieve all your items from RoboDK (they should be previously loaded manually or using the API's command RDK.AddFile())
list_objects   = []
for i in range(DOFs + 1):
   if i == 0:
       itm = RDK.Item(robot_name + ' Base', ITEM_TYPE_OBJECT)
   else:
       itm = RDK.Item(robot_name + ' ' + str(i), ITEM_TYPE_OBJECT)

   list_objects.append(itm)

# Create the robot/mechanism
new_robot = RDK.BuildMechanism(MAKE_ROBOT_6DOF, list_objects, parameters, joints_build, joints_home, joints_senses, lower_limits, upper_limits, base_pose, tool_pose, robot_name)
if not new_robot.Valid():
    print("Failed to create the robot. Check input values.")
else:
    print("Robot/mechanism created: " + new_robot.Name())
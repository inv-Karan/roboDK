RDK = Robolink()
object = RDK.Item('My Object')
object.Copy()               # same as RDK.Copy(object) also works
object_copy1 = RDK.Paste()
object_copy1.setName('My Object (copy 1)')
object_copy2 = RDK.Paste()
object_copy2.setName('My Object (copy 2)')

#Example to retrieve the 3D point under the mouse cursor
RDK = Robolink()
while True:
    xyz, item = RDK.CursorXYZ()
    print(str(item) + " " + str(xyz))

from robolink import *                  # import the robolink library        
RDK = Robolink()                        # connect to the RoboDK API (RoboDK starts if it has not started
tool  = RDK.Item('Tool')                # Retrieve an item named tool
robot = RDK.Item('', ITEM_TYPE_ROBOT)   # the first available robot

RDK.ItemUserPick("Pick a robot", ITEM_TYPE_ROBOT)

Example to load a plugin
RDK = Robolink()
RDK.PluginLoad("C:/RoboDK/bin/plugin/yourplugin.dll")

from robolink import *                  # import the robolink library        
RDK = Robolink()                        # connect to the RoboDK API (RoboDK starts if it has not started
robot = RDK.Item('', ITEM_TYPE_ROBOT)   # use the first available robot
RDK.ProgramStart('Prog1','C:/MyProgramFolder/', "ABB_RAPID_IRC5", robot)  # specify the program name for program generation
# RDK.setRunMode(RUNMODE_MAKE_ROBOTPROG) # redundant
robot.MoveJ(target)                     # make a simulation
...
RDK.Finish()                            # Provokes the program generation (disconnects the API)

tool = 0    # auto detect active tool
obj = 0     # auto detect object in active reference frame

options_command = "ELLYPSE PROJECT PARTICLE=SPHERE(4,8,1,1,0.5) STEP=8x8 RAND=2"            

# define the ellypse volume as p0, pA, pB, colorRGBA (close and far), in mm
# coordinates must be provided with respect to the TCP
close_p0 = [   0,   0, -200] # xyz in mm: Center of the conical ellypse (side 1)
close_pA = [   5,   0, -200] # xyz in mm: First vertex of the conical ellypse (side 1)
close_pB = [   0,  10, -200] # xyz in mm: Second vertex of the conical ellypse (side 1)
close_color = [ 1, 0, 0, 1]  # RGBA (0-1)

far_p0   = [   0,   0,  50] # xyz in mm: Center of the conical ellypse (side 2)
far_pA   = [  60,   0,  50] # xyz in mm: First vertex of the conical ellypse (side 2)
far_pB   = [   0, 120,  50] # xyz in mm: Second vertex of the conical ellypse (side 2)
far_color   = [ 0, 0, 1, 0.2]  # RGBA (0-1)

close_param = close_p0 + close_pA + close_pB + close_color
far_param = far_p0 + far_pA + far_pB + far_color    
volume = Mat([close_param, far_param]).tr()
RDK.Spray_Add(tool, obj, options_command, volume)
RDK.Spray_SetState(SPRAY_ON)

from robolink import *                  # import the robolink library        
RDK = Robolink()                        # connect to the RoboDK API (RoboDK starts if it has not started
tool  = RDK.Item('Tool')                # Get an item named Tool (name in the RoboDK station tree)
robot = RDK.Item('', ITEM_TYPE_ROBOT)   # Get the first available robot
target = RDK.Item('Target 1', ITEM_TYPE_TARGET)   # Get a target called "Target 1"            
frame = RDK.ItemUserPick('Select a reference frame', ITEM_TYPE_FRAME)   # Promt the user to select a reference frame

robot.setPoseFrame(frame)
robot.setPoseTool(tool)            
robot.MoveJ(target)             # Move the robot to the target using the selected reference frame

from robolink import *      # import the robolink library            
RDK = Robolink()            # Connect to the RoboDK API
prog = RDK.Item('MainProgram', ITEM_TYPE_PROGRAM)
prog.RunProgram()
while prog.Busy():
    pause(0.1)

print("Program done")

from robolink import *                  # import the robolink library
robot = RDK.Item('', ITEM_TYPE_ROBOT)   # Get the first robot available
state = robot.Connect()
print(state)

# Check the connection status and message
state, msg = robot.ConnectedState()
print(state)
print(msg)
if state != ROBOTCOM_READY:
    print('Problems connecting: ' + robot.Name() + ': ' + msg)
    quit()

# Move the robot (real robot if we are connected)
robot.MoveJ(jnts, False)

# Example to display the XYZ position of a selected object
from robolink import *    # Import the RoboDK API
RDK = Robolink()          # Start RoboDK API

# Ask the user to select an object
OBJECT = RDK.ItemUserPick("Select an object", ITEM_TYPE_OBJECT)

while True:
    is_selected, feature_type, feature_id = OBJECT.SelectedFeature()
    
    if is_selected and feature_type == FEATURE_SURFACE:
        point_mouse, name_feature = OBJECT.GetPoints(FEATURE_SURFACE)
        print("Selected %i (%i): %s  %s" % (feature_id, feature_type, str(point_mouse), name_feature))
        
    else:
        print("Object Not Selected. Select a point in the object surface...")
        
    pause(0.1)

from robolink import *                  # import the robolink library        
RDK = Robolink()                        # connect to the RoboDK API (RoboDK starts if it has not started)
tool  = RDK.Item('', ITEM_TYPE_ROBOT)   # Retrieve the robot
joints = robot.Joints().list()          # retrieve the current robot joints as a list
joints[5] = 0                           # set joint 6 to 0 deg
robot.MoveJ(joints)                     # move the robot to the new joint position

program.RunInstruction('Setting the spindle speed', INSTRUCTION_COMMENT)
program.RunInstruction('SetRPM(25000)', INSTRUCTION_INSERT_CODE)
program.RunInstruction('Done setting the spindle speed. Ready to start!', INSTRUCTION_SHOW_MESSAGE)
program.RunInstruction('Program1', INSTRUCTION_CALL_PROGRAM)

# Show the point selected
object = RDK.Item('Object', ITEM_TYPE_OBJECT)
is_selected, feature_type, feature_id = OBJECT.SelectedFeature()

points, name_selected = object.GetPoints(feature_type, feature_id)
point = None
if len(points) > 1:
    point = points[feature_id]
else:
    point = points[0]
    
RDK.ShowMessage("Selected Point: %s = [%.3f, %.3f, %.3f]" % (name_selected, point[0], point[1], point[2]))

from robolink import *                  # import the robolink library        
RDK = Robolink()                        # connect to the RoboDK API (RoboDK starts if it has not started
robot  = RDK.Item('', ITEM_TYPE_ROBOT)  # Retrieve the robot

# get the current robot joints
robot_joints = robot.Joints()

# get the robot position from the joints (calculate forward kinematics)
robot_position = robot.SolveFK(robot_joints)

# get the robot configuration (robot joint state)
robot_config = robot.JointsConfig(robot_joints)

# calculate the new robot position
new_robot_position = transl([x_move,y_move,z_move])*robot_position

# calculate the new robot joints
new_robot_joints = robot.SolveIK(new_robot_position)
if len(new_robot_joints.tolist()) < 6:
    print("No robot solution!! The new position is too far, out of reach or close to a singularity")
    continue

# calculate the robot configuration for the new joints
new_robot_config = robot.JointsConfig(new_robot_joints)

if robot_config[0] != new_robot_config[0] or robot_config[1] != new_robot_config[1] or robot_config[2] != new_robot_config[2]:
    print("Warning! Robot configuration changed: this may lead to unextected movements!")
    print(robot_config)
    print(new_robot_config)

# move the robot to the new position
robot.MoveJ(new_robot_joints)
#robot.MoveL(new_robot_joints)

from robolink import *                  # import the robolink library        
RDK = Robolink()                        # connect to the RoboDK API (RoboDK starts if it has not started
tool  = RDK.Item('Tool')                # Retrieve an item named tool
if not tool.Valid():
    print("The tool item does not exist!")
    quit()

object_curve = RDK.AddCurve(POINTS)
object_curve.setName('AutoPoints n%i' % NUM_POINTS)
path_settings = RDK.AddMillingProject("AutoCurveFollow settings")
prog, status = path_settings.setMillingParameters(part=object_curve)

#Example to expand or collapse an item in the tree
from robolink import *
RDK = Robolink()      # Start the RoboDK API

# How to change the number of threads using by the RoboDK application:
item = RDK.ItemUserPick("Select an item")

item.setParam("Tree", "Expand")
pause(2)
item.setParam("Tree", "Collapse")

#Example to change the post processor
robot = RDK.ItemUserPick("Select a robot", ITEM_TYPE_ROBOT)

# Set the robot post processor (name of the py file in the posts folder)
robot.setParam("PostProcessor", "Fanuc_RJ3")

#Example to change display style
# How to change the display style of an object (color as AARRGGBB):
obj = RDK.ItemUserPick('Select an object to change the style', ITEM_TYPE_OBJECT)

# Display points as simple dots given a certain size (suitable for fast rendering or large point clouds)
# Color is defined as AARRGGBB
obj.setValue('Display', 'POINTSIZE=4 COLOR=#FF771111')

# Display each point as a cube of a given size in mm
obj.setValue('Display','PARTICLE=CUBE(0.2,0.2,0.2) COLOR=#FF771111')

# Another way to change display style of points to display as a sphere (size,rings):
obj.setValue('Display','PARTICLE=SPHERE(4,8) COLOR=red')

# Example to change the size of displayed curves:
obj.setValue('Display','LINEW=4')   

# More examples to change the appearance of points and curves available here:
https://github.com/RoboDK/Plug-In-Interface/tree/master/PluginAppLoader/Apps/SetStyle

#Change robot visibility
# Retrieve the robot (first robot available)
robot = RDK.Item('', ITEM_TYPE_ROBOT)

# Show the robot with default settings:
robot.setVisible(True, VISIBLE_ROBOT_DEFAULT)

# Show the robot and hide all references:
robot.setVisible(1, VISIBLE_ROBOT_DEFAULT and not VISIBLE_ROBOT_ALL_REFS)

# Show only references (hide the robot):
robot.setVisible(1, VISIBLE_ROBOT_ALL_REFS)

from robolink import *              # import the robolink library (bridge with RoboDK)
from robodk import *                # import the robodk library (robotics toolbox)

RDK = Robolink()                    # establish a link with the simulator
robot = RDK.Item('KUKA KR210')      # retrieve the robot by name
robot.setJoints([0,90,-90,0,0,0])   # set the robot to the home position

target = robot.Pose()               # retrieve the current target as a pose (position of the active tool with respect to the active reference frame)
xyzabc = Pose_2_KUKA(target)        # Convert the 4x4 pose matrix to XYZABC position and orientation angles (mm and deg)

x,y,z,a,b,c = xyzabc                # Calculate a new pose based on the previous pose
xyzabc2 = [x,y,z+50,a,b,c+45]
target2 = KUKA_2_Pose(xyzabc2)      # Convert the XYZABC array to a pose (4x4 matrix)

robot.MoveJ(target2)                # Make a linear move to the calculated position

csvdata = LoadList(strfile, ',')
values = []
for i in range(len(csvdata)):
    print(csvdata[i])
    values.append(csvdata[i])
  
# We can also save the list back to a CSV file
# SaveList(csvdata, strfile, ',')

from robolink import *                  # import the robolink library
from robodk import *                    # import the robodk library

RDK = Robolink()                        # connect to the RoboDK API
robot  = RDK.Item('', ITEM_TYPE_ROBOT)  # Retrieve a robot available in RoboDK
#target  = RDK.Item('Target 1')         # Retrieve a target (example)


pose = robot.Pose()                     # retrieve the current robot position as a pose (position of the active tool with respect to the active reference frame)
# target = target.Pose()                # the same can be applied to targets (taught position)

# Read the 4x4 pose matrix as [X,Y,Z , A,B,C] Euler representation (mm and deg): same representation as KUKA robots
XYZABC = Pose_2_KUKA(pose)
print(XYZABC)

# Read the 4x4 pose matrix as [X,Y,Z, q1,q2,q3,q4] quaternion representation (position in mm and orientation in quaternion): same representation as ABB robots (RAPID programming)
xyzq1234 = Pose_2_ABB(pose)
print(xyzq1234)

# Read the 4x4 pose matrix as [X,Y,Z, u,v,w] representation (position in mm and orientation vector in radians): same representation as Universal Robots
xyzuvw = Pose_2_UR(pose)
print(xyzuvw)

x,y,z,a,b,c = XYZABC                    # Use the KUKA representation (for example) and calculate a new pose based on the previous pose
XYZABC2 = [x,y,z+50,a,b,c+45]
pose2 = KUKA_2_Pose(XYZABC2)            # Convert the XYZABC array to a pose (4x4 matrix)

robot.MoveJ(pose2)                      # Make a joint move to the new position
# target.setPose(pose2)                  # We can also update the pose to targets, tools, reference frames, objects, ...

name = mbox('Enter your name', entry=True)
name = mbox('Enter your name', entry='default')
if name:
    print("Value: " + name)

value = mbox('Male or female?', ('male', 'm'), ('female', 'f'))
mbox('Process done')

name = mbox('Enter your name', entry=True)
name = mbox('Enter your name', entry='default')
if name:
    print("Value: " + name)

value = mbox('Male or female?', ('male', 'm'), ('female', 'f'))
mbox('Process done')
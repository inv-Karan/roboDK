from robodk import *
from robolink import *

# Set the name of the reference frame to place the targets:
REFERENCE_NAME = 'Reference CSV'

# Set the name of the reference target
# (orientation will be maintained constant with respect to this target)
TARGET_NAME = 'Home' 

#---------------------------
# Start the RoboDK API
RDK = Robolink()

# Ask the user to pick a file:
rdk_file_path = RDK.getParam("PATH_OPENSTATION")
path_file = getOpenFile(rdk_file_path + "/")
if not path_file:
    print("Nothing selected")
    quit()

# Get the program name from the file path
program_name = getFileName(path_file)

# Load the CSV file as a list of list [[x,y,z,speed],[x,y,z,speed],...]
data = LoadList(path_file)

# Delete previously generated programs that follow a specific naming
# Automatically delete previously generated items (Auto tag)
#list_items = RDK.ItemList() # list all names
#for item in list_items:
#    if item.Name().startswith('Frame'):
#        item.Delete()

# Select the robot (the popup is diplayed only if there are 2 or more robots)
robot = RDK.ItemUserPick('Select a robot',ITEM_TYPE_ROBOT)
if not robot.Valid():
    raise Exception("Robot not selected or not valid")
    quit()

# Get the reference frame to generate the path
frame = RDK.Item(REFERENCE_NAME,ITEM_TYPE_FRAME)
if not frame.Valid():
    raise Exception("Reference frame not found. Use name: %s" % REFERENCE_NAME)

# Use the home target as a reference
target = RDK.Item(TARGET_NAME, ITEM_TYPE_TARGET)
if not target.Valid():
    raise Exception("Home target is not valid. Set a home target named: %s" % TARGET_NAME)

# Set the robot to the home position
robot.setJoints(target.Joints())

# Get the pose reference from the home target
pose_ref = robot.Pose()

# Add a new program
program = RDK.AddProgram(program_name, robot)

# Turn off rendering (faster)
RDK.Render(False)

# Speed up by not showing the instruction:
program.ShowInstructions(False)

# Remember the speed so that we don't set it with every instruction
current_speed = None
target = None

# Very important: Make sure we set the reference frame and tool frame so that the robot is aware of it
program.setPoseFrame(frame)
program.setPoseTool(robot.PoseTool())

# Iterate through all the points
for i in range(len(data)):
    pi = pose_ref
    pi.setPos(data[i])

    # Update speed if there is a 4th column
    if len(data[i]) >= 3:
        speed = data[i][3]
        # Update the program if the speed is different than the previously set speed
        if type(speed) != str and speed != current_speed:
            program.setSpeed(speed)
            current_speed = speed

    target = RDK.AddTarget('T%i'% i, frame)
    target.setPose(pi)
    pi = target

    # Add a linear movement (with the exception of the first point which will be a joint movement)
    if i == 0:
        program.MoveJ(pi)
    else:
        program.MoveL(pi)

    # Update from time to time to notify the user about progress
    if i % 100 == 0:
        program.ShowTargets(False)
        RDK.ShowMessage("Loading %s: %.1f %%" % (program_name, 100*i/len(data)),False)
        RDK.Render()
        
program.ShowTargets(False)

RDK.ShowMessage("Done",False)
print("Done")
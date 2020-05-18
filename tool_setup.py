import sys # allows getting the passed argument parameters
from robodk import *
from robolink import *

RDK = Robolink()

TOOL_ID = 0
if len(sys.argv) >= 2:
    TOOL_ID = int(sys.argv[1])
else:
    tool_str = mbox("Enter the tool number:\n(for example, for Tool 1 set 1)", entry='1')
    if not tool_str:
        # No input
        quit()
    TOOL_ID = int(tool_str)

# Select a robot
robot = RDK.Item('', ITEM_TYPE_ROBOT)
if not robot.Valid():
    raise Exception("Robot not available")

# Create the tool name
tool_name = 'Tool ' + str(TOOL_ID)
print("Using robot: " + robot.Name())
print("Setting tool: " + tool_name)

# Select the tool
tool = RDK.Item(tool_name, ITEM_TYPE_TOOL)
if not tool.Valid():
    raise Exception("Tool %s does not exist!" % tool_name)

# Update the robot to use the tool
robot.setTool(tool)

print("Done!")
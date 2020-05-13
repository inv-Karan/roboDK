from robolink import *

# Connect to the RoboDK API
RDK = Robolink(args=["-NEWINSTANCE", "-NOUI", "-SKIPINI", "-EXIT_LAST_COM"])

# Add a reference frame
RDK.AddFrame("My reference frame")
RDK.setPose(transl(100,200,300) * rotz(pi/2))

# Retrieve all items and print their names (just a reference frame)
list_items = RDK.ItemList()
for item in list_items:
    print(item.Name())   
    
# Close RoboDK
RDK.CloseRoboDK()

# Example command line arguments:
# -NEWINSTANCE: Forces using a new instance
# -NOUI: Run RoboDK behind the scenes (without OpenGL context)
# -SKIPINI: Skip using RoboDK's INI settings (global settings), this provides a faster startup
# -EXIT_LAST_COM: Exit RoboDK when the last API client connected closes
# -DEBUG: Run in debug mode (outputs information in the console)
#
# Follow these steps to see an extended list of command line arguments:
# 1- Select Tools-Run Script
# 2- Select ShowCommands
# 
# More information here:
#    https://robodk.com/doc/en/RoboDK-API.html#CommandLine
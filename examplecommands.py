from robolink import *
RDK = Robolink()      # Start the RoboDK API

# How to change the number of threads using by the RoboDK application:
RDK.Command("Threads", "4")

# How to change the default behavior of 3D view using the mouse:
RDK.Command("MouseClick_Left", "Select")   # Set the left mouse click to select
RDK.Command("MouseClick_Mid", "Pan")       # Set the mid mouse click to Pan the 3D view
RDK.Command("MouseClick_Right", "Rotate")  # Set the right mouse click to Rotate the 3D view

RDK.Command("MouseClick", "Default")       # Set the default mouse 3D navigation settings

# Provoke a resize event
RDK.Command("Window", "Resize")

# Reset the trace
RDK.Command("Trace", "Reset")
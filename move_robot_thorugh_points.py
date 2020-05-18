# Move a robot along a line given a start and end point by steps
# This macro shows different ways of programming a robot using a Python script and the RoboDK API

# Default parameters:
P_START = [1755, -500, 2155]    # Start point with respect to the robot base frame
P_END   = [1755,  600, 2155]    # End point with respect to the robot base frame
NUM_POINTS  = 10                # Number of points to interpolate

# Function definition to create a list of points (line)
def MakePoints(xStart, xEnd, numPoints):
    """Generates a list of points"""
    if len(xStart) != 3 or len(xEnd) != 3:
        raise Exception("Start and end point must be 3-dimensional vectors")
    if numPoints < 2:
        raise Exception("At least two points are required")
    
    # Starting Points
    pt_list = []
    x = xStart[0]
    y = xStart[1]
    z = xStart[2]

    # How much we add/subtract between each interpolated point
    x_steps = (xEnd[0] - xStart[0])/(numPoints-1)
    y_steps = (xEnd[1] - xStart[1])/(numPoints-1)
    z_steps = (xEnd[2] - xStart[2])/(numPoints-1)

    # Incrementally add to each point until the end point is reached
    for i in range(numPoints):
        point_i = [x,y,z] # create a point
        #append the point to the list
        pt_list.append(point_i)
        x = x + x_steps
        y = y + y_steps
        z = z + z_steps
    return pt_list

#---------------------------------------------------
#--------------- PROGRAM START ---------------------
from robolink import *    # API to communicate with RoboDK for simulation and offline/online programming
from robodk import *      # Robotics toolbox for industrial robots

# Generate the points curve path
POINTS = MakePoints(P_START, P_END, NUM_POINTS)

# Initialize the RoboDK API
RDK = Robolink()

# turn off auto rendering (faster)
RDK.Render(False) 

# Automatically delete previously generated items (Auto tag)
list_items = RDK.ItemList() # list all names
for item in list_items:
    if item.Name().startswith('Auto'):
        item.Delete()

# Promt the user to select a robot (if only one robot is available it will select that robot automatically)
robot = RDK.ItemUserPick('Select a robot', ITEM_TYPE_ROBOT)

# Turn rendering ON before starting the simulation
RDK.Render(True) 

# Abort if the user hits Cancel
if not robot.Valid():
    quit()

# Retrieve the robot reference frame
reference = robot.Parent()

# Use the robot base frame as the active reference
robot.setPoseFrame(reference)

# get the current orientation of the robot (with respect to the active reference frame and tool frame)
pose_ref = robot.Pose()
print(Pose_2_TxyzRxyz(pose_ref))
# a pose can also be defined as xyzwpr / xyzABC
#pose_ref = TxyzRxyz_2_Pose([100,200,300,0,0,pi])



#-------------------------------------------------------------
# Option 1: Move the robot using the Python script

# We can automatically force the "Create robot program" action using a RUNMODE state
# RDK.setRunMode(RUNMODE_MAKE_ROBOTPROG)

# Iterate through all the points
for i in range(NUM_POINTS):
    # update the reference target with the desired XYZ coordinates
    pose_i = pose_ref
    pose_i.setPos(POINTS[i])
    
    # Move the robot to that target:
    robot.MoveJ(pose_i)
    
# Done, stop program execution
quit()


#-------------------------------------------------------------
# Option 2: Create the program on the graphical user interface
# Turn off rendering
RDK.Render(False)
prog = RDK.AddProgram('AutoProgram')

# Iterate through all the points
for i in range(NUM_POINTS):
    # add a new target and keep the reference to it
    ti = RDK.AddTarget('Auto Target %i' % (i+1))
    # use the reference pose and update the XYZ position
    pose_i = pose_ref
    pose_i.setPos(POINTS[i])
    ti.setPose(pose_i)
    # force to use the target as a Cartesian target
    ti.setAsCartesianTarget()

    # Optionally, add the target as a Linear/Joint move in the new program
    prog.MoveL(ti)

# Turn rendering ON before starting the simulation
RDK.Render(True) 

# Run the program on the simulator (simulate the program):
prog.RunProgram()
# prog.WaitFinished() # wait for the program to finish

# We can create the program automatically
# prog.MakeProgram()

# Also, if we have the robot driver we could use the following call to provoke a "Run on robot" action (simulation and the robot move simultaneously)
# prog.setRunType(PROGRAM_RUN_ON_ROBOT)

# Done, stop program execution
quit()


#-------------------------------------------------------------
# Option 3: Move the robot using the Python script and detect if movements can be linear
# This is an improved version of option 1
#
# We can automatically force the "Create robot program" action using a RUNMODE state
# RDK.setRunMode(RUNMODE_MAKE_ROBOTPROG)

# Iterate through all the points
ROBOT_JOINTS = None
for i in range(NUM_POINTS):
    # update the reference target with the desired XYZ coordinates
    pose_i = pose_ref
    pose_i.setPos(POINTS[i])
    
    # Move the robot to that target:
    if i == 0:
        # important: make the first movement a joint move!
        robot.MoveJ(pose_i)
        ROBOT_JOINTS = robot.Joints()
    else:
        # test if we can do a linear movement from the current position to the next point
        if robot.MoveL_Test(ROBOT_JOINTS, pose_i) == 0:
            robot.MoveL(pose_i)
        else:
            robot.MoveJ(pose_i)
            
        ROBOT_JOINTS = robot.Joints()
    
# Done, stop program execution
quit()


# This macro shows how you can create a program that moves the robot through a set of points
# The points are automatically created as a cube grid around a reference target
# If a linear movement can't be done from one point to the next one the robot will follow a joint movement
from robolink import *    # API to communicate with RoboDK
from robodk import *      # basic matrix operations
from random import uniform # to randomly calculate rz (rotation around the Z axis)

# Name of the reference target
REFERENCE_TARGET = 'RefTarget'

# Check for collisions
CHECK_COLLISIONS = False

#Start the RoboDK API
RDK = Robolink()

# Set collision checking ON or OFF
RDK.setCollisionActive(COLLISION_ON if CHECK_COLLISIONS else COLLISION_OFF)

# Run on robot: Force the program to run on the connected robot (same behavior as right clicking the program, then, selecting "Run on Robot")
# RDK.setRunMode(RUNMODE_RUN_ROBOT)

# Get the main/only robot in the station
robot = RDK.Item('', ITEM_TYPE_ROBOT)
if not robot.Valid():
    raise Exception("Robot not valid or not available")

# Get the active reference frame
frame = robot.getLink(ITEM_TYPE_FRAME)
if not frame.Valid():
    frame = robot.Parent()
    robot.setPoseFrame(frame)

# Get the reference pose with respect to the robot
frame_pose = robot.PoseFrame()

# Get the active tool
tool = robot.getLink(ITEM_TYPE_TOOL)
if not tool.Valid():
    tool = robot.AddTool(transl(0,0,75), "Tool Grid")
    robot.setPoseTool(tool)

# Get the target reference RefTarget
target_ref = RDK.Item(REFERENCE_TARGET, ITEM_TYPE_TARGET)
if not target_ref.Valid():
    target_ref = RDK.AddTarget(REFERENCE_TARGET, frame, robot)

# Get the reference position (pose=4x4 matrix of the target with respect to the reference frame)
pose_ref = target_ref.Pose()
startpoint = target_ref.Joints()
config_ref = robot.JointsConfig(startpoint)

# Retrieve the tool pose
tool_pose = tool.PoseTool()

# Retrieve the degrees of freedom or axes (num_dofs = 6 for a 6 axis robot)
num_dofs = len(robot.JointsHome().list())

# Get the reference frame of the target reference
ref_frame = target_ref.Parent()

# Function definition to check if 2 robot configurations are the same
# Configurations are set as [Rear/Front,LowerArm/UpperArm,Flip/NonFlip] bits (int values)
def config_equal(config1, config2):
    if config1[0] != config2[0] or config1[1] != config2[1] or config1[2] != config2[2]:
        return False
    return True


# Create a new program
prog = RDK.AddProgram('AutoCreated')

# This should make program generation slightly faster
#prog.ShowInstructions(False)

# Start creating the program or moving the robot:
program_or_robot = prog
program_or_robot.setPoseTool(tool_pose)

program_or_robot.MoveJ(target_ref)
lastjoints = startpoint
rz = 0
ntargets = 0
for tz in range(-100, 101, 100):
    for ty in range(0, 401, 200):
        for tx in range(100, -5001, -250):
            ntargets = ntargets + 1
            # calculate a random rotation around the Z axis of the tool
            #rz = uniform(-20*pi/180, 20*pi/180)
                        
            # Calculate the position of the new target: translate with respect to the robot base and rotate around the tool
            newtarget_pose = transl(tx,ty,tz)*pose_ref*rotz(rz)
            
            # First, make sure the target is reachable:
            newtarget_joints = robot.SolveIK(newtarget_pose, lastjoints, tool_pose, frame_pose)
            if len(newtarget_joints.list()) < num_dofs:
                print('...target not reachable!! Skipping target')
                continue

            # Create a new target:
            newtarget_name = 'Auto T%.0f,%.0f,%.0f Rz=%.1f' % (tx,ty,tz,rz)
            print('Creating target %i: %s' % (ntargets, newtarget_name))
            newtarget = RDK.AddTarget(newtarget_name, ref_frame, robot)

            # At this point, the target is reachable.
            # We have to check if we can do a linear move or not. We have 2 methods:
            can_move_linear = True
            
            # ------------------------------
            # Validation method 1: check the joints at the destination target
            # and make sure we have the same configuration
            # A quick way to validate (it may not be perfect if robot joints can move more than 1 turn)
            # To improve this method we would have to check configurations on all possible solutions
            # from the inverse kinematics, using SolveIK_All()
            if False:
                target_joints_config = robot.JointsConfig(newtarget_joints)
                if not config_equal(config_ref, target_joints_config):
                    # We can't do a linear movement
                    can_move_linear = False
                    print("Warning! configuration is not the same as the reference target! Linear move will not be possible")
                    
                    # update the reference configuration to the new one
                    config_ref = target_joints_config
            # -------------------------------



            # -------------------------------
            # Validation method 2: use the robot.MoveL_Test option to check if the robot can make a linear movement
            # This method is more robust and should provide a 100% accurate result but it may take more time
            # robot.MoveL_Test can also take collisions into account if collision checking is activated
            issues = robot.MoveL_Test(lastjoints, newtarget_pose)
            can_move_linear = (issues == 0)
            # We can retrieve the final joint position by retrieving the robot joints
            if can_move_linear:
                newtarget_joints = robot.Joints()
            
            # ---------------------------------

            if can_move_linear:
                # All good, we don't need to modify the target.
                # However, we could set the joints in the target as this may allow us to retrieve the robot configuration if we ever need it
                newtarget.setAsCartesianTarget() # default behavior
                newtarget.setJoints(newtarget_joints)
                # It is important to have setPose after setJoints as it may recalculate the joints to match the target
                newtarget.setPose(newtarget_pose) 

                # Add the linear movement
                program_or_robot.MoveL(newtarget)
                
            else:
                #print(newtarget_joints)
                # Check if we can do a joint movement (check for collisions)
                issues = robot.MoveJ_Test(lastjoints, newtarget_joints)
                can_move_joints = (issues == 0)
                if not can_move_joints:
                    # Skip this point
                    print("Skipping movement to: " + str(newtarget_joints))
                    continue

                # Make sure we have a joint target and a joint movement
                newtarget.setAsJointTarget() # default behavior
                
                # Setting the pose for a joint target is not important unless we want to retrieve the pose later
                # or we want to use the Cartesian coordinates for post processing
                newtarget.setPose(newtarget_pose)

                # Make sure we set the joints after the pose for a joint taget as it may recalculate the pose
                newtarget.setJoints(newtarget_joints)

                # Add the joint movement
                program_or_robot.MoveJ(newtarget)


            # Remember the joint poisition of the last movement
            lastjoints = newtarget_joints

# Showing the instructions at the end is faster:
prog.ShowInstructions(True)

# Hiding the targets is cleaner and more difficult to accidentaly move a target
#prog.ShowTargets(False)

print('Program done with %i targets' % ntargets)
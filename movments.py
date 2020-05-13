# Turn off rendering (faster)
RDK.Render(False)
prog = RDK.AddProgram('AutoProgram')

# Hide program instructions (optional, but faster)
prog.ShowInstructions(False)

# Retrieve the current robot position:
pose_ref = robot.Pose()

# Iterate through a number of points
for i in range(len(POINTS)):
    # add a new target
    ti = RDK.AddTarget('Auto Target %i' % (i+1))
    
    # use the reference pose and update the XYZ position
    pose_ref.setPos(POINTS[i])
    ti.setPose(pose_ref)
    
    # force to use the target as a Cartesian target (default)
    ti.setAsCartesianTarget()

    # Add the target as a Linear/Joint move in the new program
    prog.MoveL(ti)
    
# Hide the target items from the tree: it each movement still keeps its own target. 
# Right click the movement instruction and select "Select Target" to see the target in the tree
program.ShowTargets(False) 

# Turn rendering ON before starting the simulation (automatic if we are done)
RDK.Render(True)

#--------------------------------------
# Update the program path to display the yellow path in RoboDK. 
# Set collision checking ON or OFF
check_collisions = COLLISION_OFF
# Update the path (can take some time if collision checking is active)
update_result = program.Update(check_collisions)
# Retrieve the result
n_insok = update_result[0]
time = update_result[1]
distance = update_result[2]
percent_ok = update_result[3]*100
str_problems = update_result[4]
if percent_ok < 100.0:
    msg_str = "WARNING! Problems with <strong>%s</strong> (%.1f):<br>%s" % (program_name, percent_ok, str_problems)                
else:
    msg_str = "No problems found for program %s" % program_name

# Notify the user:
print(msg_str)
RDK.ShowMessage(msg_str)
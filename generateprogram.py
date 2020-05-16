from robolink import *                  # import the robolink library        
RDK = Robolink()                        # connect to the RoboDK API (RoboDK starts if it has not started
robot = RDK.Item('', ITEM_TYPE_ROBOT)   # use the first available robot
RDK.ProgramStart('Prog1','C:/MyProgramFolder/', "ABB_RAPID_IRC5", robot)  # specify the program name for program generation
# RDK.setRunMode(RUNMODE_MAKE_ROBOTPROG) # redundant
robot.MoveJ(target)                     # make a simulation
...
RDK.Finish()                            # Provokes the program generation (disconnects the API)
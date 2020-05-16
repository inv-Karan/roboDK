from robolink import *                  # import the robolink library        
RDK = Robolink()                        # connect to the RoboDK API (RoboDK starts if it has not started
RDK.RunCode("Prog1", True)              # Run a program named Prog1 available in the RoboDK station
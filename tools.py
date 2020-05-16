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
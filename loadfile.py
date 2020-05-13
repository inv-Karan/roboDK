RDK = Robolink()
item = RDK.AddFile(r'C:\Users\Name\Desktop\object.step')
item.setPose(transl(100,50,500))

# Add a tool to an existing robot:
tool = RDK.AddFile(r'C:\Users\Name\Desktop\robot-tool.stl', robot)
tool.setPoseTool(transl(100,50,500))

# Add a reference frame, move it and add an object to that reference frame (locally):
frame = AddFrame('Reference A')
frame.setPose(transl(100,200,300))
new_object = RDK.Addfile('path-to-object.stl', frame)
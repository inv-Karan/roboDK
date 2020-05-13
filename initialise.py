from robolink import *

# Connect to the RoboDK API
RDK = Robolink()

# Retrieve all items and print their names
list_items = RDK.ItemList()
for item in list_items:
    print(item.Name())
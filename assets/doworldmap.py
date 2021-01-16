from modules.rpgsrc import world, typeloader, worldToImage
from libs import modutil

typeloader.loadAll()
world.loadAll()

worldmap = ""
print("Transforming world to string...")
for iy in range(world.worldSize):
	for ix in range(world.worldSize):
		if world.getPos(ix,iy).getType() == None:
			worldmap+="X"
		else:
			worldmap += world.getPos(ix,iy).getType().emoji
	worldmap += "\n"
		
worldmap.rstrip("\n")
	
print("Transforming string to image...")
worldToImage.represent(worldmap, modutil.absolutePath + "/map.png", cellSize=1)

print("Finished!")
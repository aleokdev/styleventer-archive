from modules.rpgsrc import worldgen, world

world.loadAll()

def recursiveUpdateLoc(loc):
	if hasattr(loc, "type"):
		loc.stype = loc.type.systemName
		delattr(loc, "type")

	for i in loc.loot:
		if hasattr(i, "type"):
			i.stype = i.type.systemName
			delattr(i, "type")

	for c in loc.connections:
		recursiveUpdateLoc(c)

print("-------- UPDATING START --------")
i = 0
for c in world.world:
	for bx in c.biomes:
		for b in bx:
			if hasattr(b, "type"):
				b.stype = b.type.systemName
				delattr(b, "type")
			if b.locationConnected != None:
				recursiveUpdateLoc(b.locationConnected)
	print("Progress: {}/{}".format(i, len(world.world)))
	i+=1

world.save()
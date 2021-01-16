from modules.rpgsrc import namegen, world, worldToImage, datatypes, namegen
from libs import modutil

import sys


def calculateTerritories():
	print("Initializing territory values...")
	for ix in range(world.worldSize):
		for iy in range(world.worldSize):
			world.getPos(ix,iy).territory = None

	def startFillingTerritory(biome, replacement : int):
		if biome.territory != None:
			return False

		if biome.stype == "OCEAN":
			return False

		biome.territory = replacement
	
		queue = [biome]

		while len(queue) > 0:
			n = queue.pop(0)
			for ix in [n.x - 1, n.x, n.x + 1]:
				for iy in [n.y - 1, n.y, n.y + 1]:
					if ix == n.x and iy == n.y:
						continue

					if world.isPositionValid(ix, iy):
						p = world.getPos(ix, iy)
						if p.territory != None:
							continue
						if p.stype != "OCEAN":
							p.territory = replacement
							queue.append(p)
		return True

	print("Defining territories...")
	t = 1
	for ix in range(world.worldSize):
		for iy in range(world.worldSize):
			if startFillingTerritory(world.getPos(ix, iy), t):
				t+=1

		if ix % 5 == 0:
			print("{}% complete, territories: {}".format(int(ix / world.worldSize * 100), t-1))

	print("Converting world to list...")
	worldmap = []
	for iy in range(world.worldSize):
		worldmap.append([])
		for ix in range(world.worldSize):
				worldmap[iy].append(0 if world.getPos(ix,iy).territory == None else world.getPos(ix,iy).territory)


	print("Defining palette...")
	palette = [(0,0,0)]
	for i in range(1, 100):
		palette.append(((i*21) % 0xff, (i * 7) % 0xff, (i * 29) % 0xff))

	print("Converting to image...")
	worldToImage.representCustom(worldmap, modutil.absolutePath + "/mapland.png", palette)

	print("Saving world...")
	world.save()

	print("Finished!")

def listTerritories():
	print("Extracting territories...")
	territories = {}
	def addTerritory(value):
		if value in territories.keys():
			territories[value] += 1
		else:
			territories[value] = 1

	for ix in range(world.worldSize):
		for iy in range(world.worldSize):
			if (world.getPos(ix,iy).territory == None):
				addTerritory(-1)
			else:
				addTerritory(world.getPos(ix,iy).territory)

	chosenNames = []
	for key, val in territories.items():
		if key == -1:
			print("Ocean;{}".format(val))
		else:
			name = namegen.getRandomName()
			while(name in chosenNames):
				name = namegen.getRandomName()
			l = datatypes.LandMass(key, val, name)
			chosenNames.append(name)
			print("{};{}".format(name, val))
			world.addLandmass(l)
	
	print("Total territories -- {}".format(len(territories) - 1))
	print("Saving world...")
	world.save()


if len(sys.argv) == 1:
	print("Usage: python3 landnamer.py [-g] [-l]")
	print("-g will calculate the terrain of each territory and set it in the current world.")
	print("-l will list all the territories existant and add new landmasses to world.landmasses.")
else:
	world.loadAll()

	if "-g" in sys.argv:
		print("Calculating territories.")
		calculateTerritories()
		
	if "-l" in sys.argv:
		listTerritories()

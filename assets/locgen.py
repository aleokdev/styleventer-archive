#############
## IMPORTS ##
#############
from tqdm import tqdm, trange
from modules.rpgsrc import world, worldToImage, typeloader
from modules.rpgsrc.datatypes import Location
from libs import modutil
import sys, random
import argparse

#################
## DEFINITIONS ##
#################
def placeLocation(x : int, y : int):
	global positionsOkay

	biome = world.getPos(x, y)
	biome.locationConnected = Location(random.choice(biome.getType().possibleLocations).systemName, biome, None)

	for ix in range(x + 1, world.worldSize):
		if world.getPos(ix, y).getType().systemName == "OCEAN":
			break
		setOkay(True, ix, y)

	for ix in range(x - 1, 0, -1):
		if world.getPos(ix, y).getType().systemName == "OCEAN":
			break
		setOkay(True, ix, y)

	for iy in range(y + 1, world.worldSize):
		if world.getPos(x, iy).getType().systemName == "OCEAN":
			break
		setOkay(True, x, iy)

	for iy in range(y - 1, 0, -1):
		if world.getPos(x, iy).getType().systemName == "OCEAN":
			break
		setOkay(True, x, iy)

def isOkay(x, y):
	return positionsOkay[y][x]

def setOkay(val, x, y):
	global positionsOkay
	if world.isPositionValid(x, y):
		positionsOkay[y][x] = val

def selectRandomPosThatCanHaveLocations():
	b = world.getRandomPos()
	while len(b.getType().possibleLocations) == 0:
		b = world.getRandomPos()

	return (x, y)

def getRandomPosFromPositionsOkay():
	x,y = (random.randint(0, world.worldSize-1), random.randint(0, world.worldSize-1))
	tries = 0
	while not isOkay(x, y):
		x,y = (random.randint(0, world.worldSize-1), random.randint(0, world.worldSize-1))
		tries += 1
		if tries > maxRandomTries:
			return (None, None)

	isVertical = isOkay(x, y+1)

	if isVertical:
		x += random.randint(-locationRange, locationRange)
		# Constrain to world limits
		x = min(world.worldSize-1, max(0, x))
	else:
		y += random.randint(-locationRange, locationRange)
		# Constrain to world limits
		y = min(world.worldSize-1, max(0, y))
	return (x,y)

#############
## PROGRAM ##
#############
parser = argparse.ArgumentParser(description="Program used for generating locations in the current world saved.")

parser.add_argument("-l", "--location_density", type=float,
                help="Locations per biome. Must be a number between 0 (No locations) and 1 (Nº biomes = Nº locations). Default is 0.01.")

parser.add_argument("-r", "--location_range", type=int,
                help="Maximum distance there can be from a location to a walkable path the player can be in. Default is 2.")

parser.add_argument("-t", "--random_tries", type=int,
                help="How many times the algorithm will try to put a location before it gives up. Default is 10000 tries.")

parser.add_argument("-m", "--max_recursion", type=int,
					help="How much recursion is allowed in a location. Defaults to 50.")

parser.add_argument("-s", "--recursion_slices", type=int,
					help="In how many 'slices' the recursion levels are divided into. Think of it like 'levels' of recursion (small, medium, big) would be 3 slices. Smaller numbers produce indifference between big and small islands, while bigger numbers produce an exaggerate difference. Defaults to 10.")

parser.add_argument("-c", "--max_children", type=int,
					help="How many children are allowed in a family of locations. This is NOT seen as a rule, but as a hint to the algorithm. Defaults to 1000.")

parser.add_argument("-b", "--max_bifurcations", type=int,
					help="How many children are allowed PER LOCATION. Defaults to 3.")

parser.add_argument("-gsl", "--generate_surface_locations", action="store_true", help="Will generate locations that are in biomes.")

parser.add_argument("-grl", "--generate_recursive_locations", action="store_true", help="Will recurse locations that are in biomes.")

parser.add_argument("-ra", "--reset_all", action="store_true", help="Will destroy ALL locations.")

parser.add_argument("-rr", "--reset_recursive", action="store_true", help="Will destroy all recursive locations (Locations that are children of other locations).")

parser.add_argument("-mm", "--max_multitude_for_recursion", type=int,
					help="The maximum multitude allowed for having the maximum recursion possible. Higher means that big islands will have a higher chance of having big locations, while a low number means the opposite. Default is 1000.")

prgArgs = parser.parse_args(sys.argv[1:])

locationDensity = 0.01 if prgArgs.location_density == None else prgArgs.location_density
locationRange = 2 if prgArgs.location_range == None else prgArgs.location_range
maxRandomTries = 10000 if prgArgs.random_tries == None else prgArgs.random_tries
maxRecursion = 50 if prgArgs.max_recursion == None else prgArgs.max_recursion
maxChildren = 1000 if prgArgs.max_recursion == None else prgArgs.max_recursion
maxBifurcations = 3 if prgArgs.max_bifurcations == None else prgArgs.max_bifurcations
maxMultitudeForMaxRecursion = 1000 if prgArgs.max_multitude_for_recursion == None else prgArgs.max_multitude_for_recursion
recursionSlices = 10 if prgArgs.recursion_slices == None else prgArgs.recursion_slices

if(prgArgs.reset_all):
	world.loadAll()
	for iy in tqdm(range(world.worldSize), desc="Resetting all locations"):
		for ix in range(world.worldSize):
			world.getPos(ix,iy).locationConnected = None

	for l in tqdm(world.landmasses, desc="Resetting landmasses' location count"):
		l.nOfLocations = 0

	world.save()

if(prgArgs.reset_recursive):
	world.loadAll()
	for iy in tqdm(range(world.worldSize), desc="Resetting recursive locations"):
		for ix in range(world.worldSize):
			if world.getPos(ix,iy).locationConnected != None:
				world.getPos(ix,iy).locationConnected.connections = []
	
	world.save()

if(prgArgs.generate_surface_locations):
	allPositionsOkay = []
	positionsOkay = []

	for iy in tqdm(range(world.worldSize), desc = "Creating positionsOkay"):
		positionsOkay.append([])
		for ix in range(world.worldSize):
			positionsOkay[iy].append(False)

	for iy in tqdm(range(world.worldSize), desc = "Creating allPositionsOkay"):
		allPositionsOkay.append([])
		for ix in range(world.worldSize):
			allPositionsOkay[iy].append(False)

	typeloader.loadAll()
	world.loadAll()


	for iy in tqdm(range(world.worldSize), desc="Adding territory starting positions"):
		for ix in range(world.worldSize):
			b = world.getPos(ix,iy)
			if b.territory == None:
				continue
			if len(b.getType().possibleLocations) > 0:
				world.getLandmassByID(b.territory).startingPos = (ix, iy)

	for landmass in tqdm(world.landmasses, desc="Adding locations"):
		if not hasattr(landmass, "startingPos"):
			continue
		for iy in range(world.worldSize):
			for ix in range(world.worldSize):
				setOkay(False, ix, iy)

		placeLocation(*landmass.startingPos)
		landmass.nOfLocations = 1

		def f(lm): # Neccesary because we want to break out from a nested loop
			for i in tqdm(range(int(lm.size * locationDensity)), desc="Landmass #{}".format(lm.id)):
				x,y = getRandomPosFromPositionsOkay()
				if x == None:
					continue
				while len(world.getPos(x, y).getType().possibleLocations) == 0 or world.getPos(x, y).locationConnected != None:
					x,y = getRandomPosFromPositionsOkay()
					if x == None:
						break
				if x == None:
					continue
				placeLocation(x, y)
				lm.nOfLocations+=1
		f(landmass)

		for iy in range(world.worldSize):
			for ix in range(world.worldSize):
				if isOkay(ix,iy):
					allPositionsOkay[iy][ix] = True

	worldmap = []
	for iy in tqdm(range(world.worldSize), desc = "Converting world to list"):
		worldmap.append([])
		for ix in range(world.worldSize):
			worldmap[iy].append((1 if allPositionsOkay[iy][ix] else 0) if world.getPos(ix,iy).locationConnected == None else 2)

	palette = [(0,0,0), (0x99,0xd9,0xea), (0xff,0,0)]

	print("Converting to image...")
	worldToImage.representCustom(worldmap, modutil.absolutePath + "/maploc.png", palette)

	print("Finished placing locations in surface!")

	world.save()


def calculateLocationMultitude(loc : Location):
	loc.multitude = world.getLandmassByID(loc.biome.territory).nOfLocations

def calculateRecursion(loc : Location):
	calculateLocationMultitude(loc)

	return random.randint(0, maxRecursion)


def calculateChildren(loc : Location, locMaxRecursion = None):
	if locMaxRecursion == None:
		locMaxRecursion = calculateRecursion(loc)

	totalSize = 1

	for i in range(random.randint(1, maxBifurcations + 1)):
		if loc.recursion >= locMaxRecursion or len(loc.getType().possibleLocationsConnected) == 0 or totalSize > maxChildren:
			return totalSize
		child = Location(random.choice(loc.getType().possibleLocationsConnected).systemName, loc.biome, loc)
		loc.connections.append(child)
		totalSize += calculateChildren(child, locMaxRecursion)

	return totalSize

if prgArgs.generate_recursive_locations:
	typeloader.loadAll()
	world.loadAll()
	sizes = {}
	def addSize(s):
		if s not in sizes.keys():
			sizes[s] = 1
		else:
			sizes[s] += 1
	for iy in tqdm(range(world.worldSize), desc="Recursing locations"):
		for ix in range(world.worldSize):
			b = world.getPos(ix, iy)
			if b.locationConnected != None:
				addSize(calculateChildren(b.locationConnected))

	for k, v in sizes.items():
		print("Nº of locations with size {}: {}".format(k, v))

	world.save()
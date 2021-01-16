import random
from . import world
from .datatypes import Biome, Location, BiomeType, WeaponType, Weapon, Chunk
from .world import getPos, isPositionValid

def spawnLoot(loc):
	for wType in WeaponType.all:
		# Get common loot types between the location and each and every weapon type.
		# Since wType.lootLocations is a tuple containing also the rarity of each loot type, get only the loot type (item 0).
		common = set(map(lambda l: l[0], wType.lootConnections)).intersection(loc.getType().lootTypes)
		
		# If there are common loot types...
		if len(common) > 0:
			# Iterate over all of them
			for clt in common:
				# And if by random chance specified in the weaponType, add weapon.
				if random.randint(0,100) < list(filter(lambda l: clt == l[0],wType.lootConnections))[0][1]:
					loc.loot.append(Weapon(wType))
					
def recursivelySpawnLoot(loc):
	spawnLoot(loc)
	for l in loc.connections:
		recursivelySpawnLoot(l)
		
def resetLoot(loc):
	loc.loot = []
	
def recursivelyResetLoot(loc):
	resetLoot(loc)
	for l in loc.connections:
		recursivelyResetLoot(l)

# Adds connecting locations to an existing one. Also adds loot.
def recurseLocation(loc):
	spawnLoot(loc)
	if loc.recursion > 5:
		return
	
	for possibleConnectionType in loc.getType().possibleLocationsConnected:
		if random.randint(0,100) < 60:
			loc.connections.append(Location(possibleConnectionType, loc.biome, loc))
			loc.connections[-1].recursion = loc.recursion + 1
			recurseLocation(loc.connections[-1])
			

# Function that generates an "edgy" world start with a biometype specified.
# "edgy" starts generate biomes in the border of the world.
# Can be used, for example, to make oceans that expand to the center of the world.
def generateStart_edgy(b : BiomeType):
	for ix in [0,world.worldSize-1]:			# Go through each border...
		for iy in range(0,world.worldSize-1):
			getPos(ix,iy).stype = b.systemName	# And change it to be the biomeType specified.

	for iy in [0,world.worldSize-1]:
		for ix in range(0,world.worldSize-1):
			getPos(ix,iy).stype = b.systemName

# World starters, also known as properties linked to functions that generate the base for a world.
worldStarters = {"EDGY" : generateStart_edgy}

def generateBaseForWorld():
	pr = BiomeType.getPrioritized()									# First, get the prioritized BiomeType. This type should have a property that indicates
	if pr == None:													# the world generator which "world starter" to use.
		print("WARNING: There is no prioritized biome type.")		# If there is no prioritized BiomeType, throw an informative message and return.
		return

	if not any(p in worldStarters.keys() for p in pr.properties):	# Check if the prioritized BiomeType has any worldStarters as a property.
		raise Exception("There are no starting properties in prioritized biome type!")	# If not, raise an exception.
	else:
		for property in worldStarters.keys():						# If it has a worldStarter as a property, get the function linked to it declared in
			if property in pr.properties:							# the 'worldStarters' variable, and call it with the prioritized biome type.
				worldStarters[property](pr)

def getWeightedFromNeighbours(x, y):
	possibilities = {}
	only = {}
	for ix in (-1, 0, 1):
		for iy in (-1, 0, 1):	
			if ix == 0 and iy == 0:
				continue
			if not isPositionValid(x+ix, y+iy):
				continue
			neighbour = getPos(x+ix,y+iy).getType()

			if neighbour == None:
				continue
			
			if "CANCELONLYTHIS" in neighbour.properties:
				only = None

			if "ONLYTHIS" in neighbour.properties and only != None:
				only = neighbour.possibleBiomesNear
			else:
				for bio in neighbour.possibleBiomesNear.keys():
					if bio not in possibilities:
						possibilities[bio] = neighbour.possibleBiomesNear[bio]
					else:
						possibilities[bio] = min(possibilities[bio], neighbour.possibleBiomesNear[bio])
	
	if only == None or only == {}:
		return possibilities
	else:
		return only

# Generates a biome depending on its neighbours.
def chooseBiome(x, y):
	biome = getPos(x,y)													# First, store the biome as a variable so we don't have to use getPos constantly.
	if biome.stype != None:												# Return if the biome is already typed.
		return

	possibilities = getWeightedFromNeighbours(x, y)
	
	biome.stype = random.choices(										# If no errors occur, then get a random, weighted value from possibilities.
								list(possibilities.keys()),
								weights=list(possibilities.values())
								)[0].systemName							# And that's it!
			
# Initializes and generates the world variable, with the size specified.
# Also saves all chunks at world/chunks/.
def generateWorld():
	for iy in range(5):
		for ix in range(5):
			world.addChunk(Chunk(ix, iy, None))
	
	print("Generating world. This may take a few minutes.")
	generateBaseForWorld()

	for i, c in enumerate(world.world):
		for ix in range(Chunk.size):
			for iy in range(Chunk.size):
				chooseBiome(ix+c.x*Chunk.size, iy+c.y*Chunk.size)

		print("Generated: {}/{}".format(i,len(world.world)))

def clearWorld():
	world.world = []
	for iy in range(5):
		for ix in range(5):
			world.addChunk(Chunk(ix, iy, None))
		
def generateLoot():
	for iy in range(5):
		for ix in range(5):
			world.world.append(Chunk.load(ix, iy))

	for i, c in enumerate(world.world):
		for ix in range(Chunk.size):
			for iy in range(Chunk.size):
				l = getPos(ix+c.x*Chunk.size, iy+c.y*Chunk.size).locationConnected
				if l != None:
					recursivelyResetLoot(l)
					recursivelySpawnLoot(l)
		print("Generated: {}/{}".format(i,len(world.world)))
import random, world,pickle,os
from libs import modutil
from . import rpglang

# RPGuser class. Stores information about an user, like its discord id and position.
class RPGUser:
	# all	-> (str:RPGUser) RPGUsers that have played are stored here. Keyed by id.
	all = {}

	def saveAll():
		for i, user in enumerate(RPGUser.all.values()):
			user.save()
			print("Saved users: {}/{}".format(i, len(RPGUser.all)))

	def get(id):
		try:
			return RPGUser.all[int(id)]
		except KeyError:
			return None

	def isLoaded(id):
		return (int(id) in RPGUser.all.keys())
	
	# id			-> (str) Discord ID of the user.
	# x, y			-> (int) Position of the user in the world.
	# locPos		-> (Location) None if the user is not inside any location, otherwise represents
	#							  a location the player is in.
	# fighters		-> (Fighter[]) List of fighters the user has.
	# tutorialDone	-> (bool) Tutorial state of the user:
	#				-------> True: Done tutorial
	#				-------> False: Hasn't done tutorial
	# inventory		-> (Loot[]) Contains loot that the user has collected and currently posseses.

	# setPos(self, _x, _y)	-> (None) Sets the user's position.
	# move(self, _x, _y)	-> (None) Moves the player by an amount in the x and y axis.
	# getName(self)			-> (str) Returns the user's name.
	# name	-> (str) Name of the fighter. The first fighter in an user will always have the user's name and
	#				 will represent the entirety of the team.
	# level	-> (int) Level of the fighter. New fighters start with level 1.
	# xp	-> (int) Experience of the fighter. New fighters start with 0 experience.
	# hp	-> (int) Current health points out of <maxhp>.
	# maxhp	-> (int) The maximum health points that this fighter can have.
	
	# getXpForNextLevel(self)	-> (int) Returns the neccesary experience points to reach the next level.
	
	def __init__(self, _id, _x, _y, _name):
		self.id = _id
		self.x = _x
		self.y = _y
		self.tutorialDone = False
		self.inventory = []
		self.locPos = None
		RPGUser.all[_id] = self
		self.name = _name
		self.level = 1
		self.xp = 0
		self.hp = 100
		self.maxhp = 100
	
	def setPos(self, _x : int, _y : int):
		self.x = _x
		self.y = _y
	
	def move(self, _x : int, _y : int):
		self.x = self.x + _x
		self.y = self.y + _y
		
	def getName(self):
		return self.name
		
	def moveIntoLoc(self, loc):
		self.locPos = loc
	
	def isInsideLocation(self):
		return self.locPos != None

	def save(self):
		pickle.dump(self, open(os.path.join(modutil.absolutePath, "world", "users", "u"+str(self.id)), "wb"))
		
	def load(_id : int):
		u = pickle.load(open(os.path.join(modutil.absolutePath, "world", "users", "u"+str(_id)), "rb"))
		RPGUser.all[u.id] = u
		return u
		
	def existsSaveFile(_id : int):
		return os.path.isfile(os.path.join(modutil.absolutePath, "world", "users", "u"+str(_id)))
			
	def getXpForNextLevel(self):
		return self.level * 100
				
# BiomeType class. Stores information about a type of biomes.
class BiomeType:
	all = {} # Keyed by systemName!
	prioritized = None

	def getPrioritized():
		return BiomeType.prioritized

	def get(_sysname):
		return BiomeType.all[_sysname]

	# getAllFirstSpawnable()	-> (BiomeType[]) Returns the <all> list filtered to only contain
	#											 BiomeTypes that can be spawned at first without
	#											 making all the world the same (Filters <all> to
	#											 only contain biomes which can have connections)
	
	def getAllFirstSpawnable():
		return list(filter(lambda t: len(t.possibleBiomesNear) > 0,BiomeType.all.values()))
	
	# systemName			-> (str) How the biome is called internally.
	# name					-> (str) How the biome is called externally (In the language the bot started up with).
	# possibleBiomesNear	-> (dict(BiomeType, int)) The biomes that can be neighbouring this type. Used at
	#										 generation time. (int: Chance of type)
	# representativeChar	-> (str) Obsolete, todo: remove
	# gender				-> (bool) Represents the gender of the biome's name (Masculine or femenine).
	#								  False represents masculine, whereas True represents femenine.
	# possibleLocations		-> (LocationType[]) The locations that can be in this type of biome.
	# loot					-> Not used?
	# emoji					-> (str) Character used at the action menu to represent the biome.
	#								 Defaults to '~'.
	
	# getNameWithDeterminant(self)	-> (str) Returns the biome's name along with its corresponding determinant
	#										 before it ('un' or 'una').
	
	def __init__(self, _sysname, _bnear, _plocs, _char, _gender):
		self.systemName = _sysname
		self.name = "undefined"
		self.possibleBiomesNear = _bnear
		self.representativeChar = _char
		self.gender = _gender
		self.possibleLocations = []
		self.loot = []
		self.emoji = "~"
		BiomeType.all[_sysname] = self
		self.properties = []
		
	def getNameWithDeterminant(self):
		return ("una" if self.gender else "un") + " " + self.name.lower()

# LocationType class. Stores information about a type of location.
class LocationType:
	all = {} # Keyed by systemName!
	
	def get(_sysname):
		return LocationType.all[_sysname]

	# systemName				-> (str) How the location is called internally.
	# name						-> (str) How the location is called externally (In the language the bot started up with).
	# possibleLocationsConnected-> (LocationType[]) The locations that can be connected to this location. Used at
	#										 		generation time.
	# gender					-> (bool) Represents the gender of the location's name (Masculine or femenine).
	#									  False represents masculine, whereas True represents femenine.
	# lootTypes					-> (str[]) List of loot types. Those can be anywhere from DUNGEON, to MINE, to NOLOOT,
	#									   and represent the types of loot that there can be in the location. Used at
	#									   generation time.
	# extraAtttributes			-> (str[]) List of extra attributes given to the location. Until now, the attributes can
	#									   be:
	#									   MORELOOT -> Benefits the location with 50% more loot.
	#									   LESSLOOT -> Gives the location 50% less loot.
	#									   UNIQUE	-> Makes the location generate only once at one position. Used, for
	#												   example, for legendary monster spawns.
	
	# getNameWithDeterminant(self)	-> (str) Returns the location's name along with its corresponding determinant
	#										 before it ('un' or 'una').
	
	def __init__(self, _sysname: str):
		self.systemName = _sysname
		self.name = "undefined"
		self.possibleLocationsConnected = []
		self.gender = False
		self.lootTypes = []
		self.extraAttributes = []
		LocationType.all[_sysname] = self
		
	# Get with "un" or "una" depending on gender.
	def getNameWithDeterminant(self):
		return ("una" if self.gender else "un") + " " + self.name.lower()
		
	# Get with "el" or "la" depending on gender.
	def getNameWithArticle(self):
		return ("la" if self.gender else "el") + " " + self.name.lower()
		
# Class used as base for WeaponTypes, and for normal items that have no use.
class ItemType:
	all = {} # Keyed by systemName!
	
	def get(_sysname):
		return ItemType.all[_sysname]

	# systemName				-> (str) How the item is called internally.
	# name						-> (str) How the item is called externally (In the language the bot started up with).
	# lootConnections			-> ((str, int)[]) List of tuples that signify where does this item appear, and how
	#											  commonly it does. The string is the loot type (DUNGEON, MINE, ...)
	#											  and the integer is a number between 0 and 100 that expresses how
	#											  often does the item appear in that particular loot type.
	#											  In the range, 0 would never appear, while 100 would always appear
	#											  in the loot type specified.
	
	# getNameWithDeterminant(self)	-> (str) Returns the item's name along with its corresponding determinant
	#										 before it ('un' or 'una').
	
	def __init__(self, _sysname):
		self.gender = False
		self.name = "undefined"
		self.systemName = _sysname
		self.lootConnections = []
		ItemType.all[_sysname] = self
	
	def getNameWithDeterminant(self):
		return ("una" if self.gender else "un") + " " + self.name.lower()
	
# WeaponType class. Stores information about a type of weapon.
class WeaponType(ItemType):
	all = {} # Keyed by systemName!

	def get(_sysname):
		return WeaponType.all[_sysname]
	
	# (Derived from ItemType)
	# attack	-> (int) Damage that the weapon inflicts. By comparison, a light sword has 10 attack.
	# agility	-> (int) Agility that the weapon has, ranging from 0 (Slowest) to 100 (Fastest). By comparison, a light
	#					 sword has 70 agility, and a heavy axe 45.
	# hands		-> (int) Number of hands needed to equip the object.
	# attributes-> (str[]) Attribute types that the weapon can have. Those are used to get the real attributes that the
	#					   weapon can have. Examples are UNREAL, CONDITION...
	# rangeType	-> (str) Specifies if the weapon is MELEE or RANGED.
	
	def __init__(self, _sysname):
		ItemType.__init__(self, _sysname)
		
		self.rangeType = None
		self.attack = 0
		self.agility = 0
		self.hands = 0
		self.attributes = []
		WeaponType.all[_sysname] = self
	
class EnemyEventCommandType:
	say = 1
	say_raw = 2

class EnemyEventCommand:
	def __init__(self, _type, _args):
		self.type = _type
		self.args = _args

	def execute(self, enemy, embed):
		if self.type == EnemyEventCommandType.say:
			embed.description += rpglang.getl("ENEMY_SAY").format(enemy = enemy.name, msg = ",".join(_args))
		elif self.type == EnemyEventCommandType.say_raw:
			embed.description += ",".join(_args)

class EnemyEventScript:
	def __init__(self, _type):
		self.type = _type
		self.commands

	def addCommand(c):
		self.commands.append(c)

	def execute(self, enemy, embed):
		for c in self.commands:
			c.execute(enemy)

class EnemyType:
	def __init__(self, systemname):
		self.events = {}
		self.systemName = systemname
		self.name = "undefined"
		self.gender = False
		self.hp = 0
		self.atkMultiplier = 1
		self.weaponsPossible = []
		self.attributes = []
		self.foundIn = {}
		self.xpDrop = 0
		self.specialAttacks = []

	def callEvent(self, event, embed):
		self.events[event].execute(self, embed)

# WAttribute class. Stores information about a weapon attribute/adjective.
class WAttribute:
	all = []
	
	probabilitySum = 0
	# nameM			-> (str) The name that the attribute uses at its masculine form.
	# nameF			-> (str) The name that the attribute uses at its femenine form.
	# classification-> (str) Words used to identify which weapons can the attributes be used with, such as UNREAL or CONDITION.
	# attackMod		-> (float) Percentage used to add or remove attack to the base weapon.
	# agilityMod	-> (float) Percentage used to add or remove agility to the base weapon.
	# rangeType		-> (str) Specifies if the attribute is for MELEE or RANGED weapons.
	
	def __init__(self, _nameM):
		self.nameM = _nameM
		self.nameF = "undefined"
		self.rangeType = None
		self.probability = 0
		# UNREAL, NORMAL...
		self.classification = None
		self.attackMod = 0
		self.agilityMod = 0
		WAttribute.all.append(self)
		
	def chooseRandom():
		r = random.randint(0, WAttribute.probabilitySum)
		for att in WAttribute.all:
			r -= att.probability
			if r<=0:
				return att
	
# Biome class. Stores information about a biome, like its position and type.
class Biome:
	# stype				-> (str) Systemname of the BiomeType this Biome derives from.
	# x,y				-> (int) Position of the biome in the world.
	# loot				-> (Item[]) Loot present in the biome.
	# locationConnected	-> (Location) Location connected to this biome, or None if this Biome has no location.

	def __init__(self, _type, _x, _y):
		self.stype = _type
		self.x = _x
		self.y = _y
		self.loot = []
		self.locationConnected = None
		self.territory = None
		
	def getType(self):
		if self.stype in BiomeType.all.keys():
			return BiomeType.all[self.stype]
		else:
			return None

# Location class. Stores information about a location, like its connections.
class Location:
	# stype			-> (str) Systemname of the LocationType this Location derives from.
	# parentLoc		-> (Location) Parent location, None if doesn't derive from one.
	# biome			-> (Biome) Parent biome.
	# recursion		-> (bool) How many connections apart is this location from its parent biome.
	# connections	-> (Location[]) Connections to other locations.
	# loot			-> (Item[]) Loot present in the location.

	def __init__(self, _type, _biome, _parent):
		self.stype = _type
		self.parentLoc = _parent
		self.biome = _biome
		self.recursion = 0 if _parent == None else _parent.recursion + 1
		self.connections = []
		self.loot = []
		
	#def derivesFromLocation(self):
	#	return
		
	def getType(self):
		return LocationType.all[self.stype]
		
class Item:
	# stype	-> (str) Systemname of the ItemType this item derives from.
	
	# getFullName					-> (str) Virtual void. Returns the full name of the item.
	# getFullNameWithDeterminant	-> (str) Virtual void. Returns the full name of the item along with a determinant.
	# getFullNameWithArticle		-> (str) Virtual void. Returns the full name of the item along with an article.

	def __init__(self, _type):
		self.stype = _type
		
	def getFullName(self):
		return "item definition of getFullName"
		
	def getFullNameWithDeterminant(self):
		return "item definition of getFullNameWithDeterminant"
		
	def getFullNameWithArticle(self):
		return "item definition of getFullNameWithArticle"
		
	def getType(self):
		return ItemType.all[self.stype]
	
class Weapon(Item):
	# (Derived from Item)
	# attributes -> (wAttribute[]) Attributes (adjetives) this weapon has.

	def __init__(self, _type):
		Item.__init__(self, _type)
		
		self.attributes = []
		# Select random attributes
		_adjs = ""
		_adjsAtEnd = ""
		
		for i in range(random.randint(0, 5)):
			_att = WAttribute.chooseRandom()
			if not _att in self.attributes:
				self.attributes.append(_att)
		
	def getFullName(self):
		print(self.attributes)
		_before = list(map(lambda l: l.nameF if self.getType().gender else l.nameM,list(filter(lambda a: not a.nameM.startswith("de "),self.attributes))))
		_last = list(map(lambda l: l.nameF if self.getType().gender else l.nameM,list(filter(lambda a: a.nameM.startswith("de "),self.attributes))))
		return ("{} {} {}".format(self.getType().name, " ".join(_before), " ".join(_last))).rstrip()
		
	def getFullNameWithDeterminant(self):
		_name = self.getFullName()
		print("Full name: " + _name)
		_ret = ("una " if self.getType().gender else "un ") + _name.lower()
		
		if len(self.attributes) == 0:
			_ret = _ret + " normal y corriente"
		
		return _ret
		
	def getFullNameWithArticle(self):
		_name = self.getFullName()
		print("Full name: " + _name)
		_ret = ("la " if self.getType().gender else "el ") + _name.lower()
		
		if len(self.attributes) == 0:
			_ret = _ret + " normal y corriente"
		
		return _ret
		
# Stores groups of 100x100 biomes (10000 in total) for saving/loading data.
class Chunk:
	size = 100
	def __init__(self, _x, _y, defaultBiomeType):
		self.biomes = []
		self.x = _x
		self.y = _y
		
		for iy in range(Chunk.size):
			self.biomes.append([])
			for ix in range(Chunk.size):
				self.biomes[iy].append(Biome(defaultBiomeType,self.x * Chunk.size + ix, self.y * Chunk.size + iy))
		
	def load(_x, _y):
		return pickle.load(open(os.path.join(modutil.absolutePath, "world", "chunks", "c"+str(_x)+"0"+str(_y)), "rb"))
		
	def setPos(self, _b, _x, _y):
		self.biomes[_y][_x] = _b
	
	def getPos(self, _x, _y):
		_x %= Chunk.size			# Get relative position
		_y %= Chunk.size
		return self.biomes[_y][_x]	# Return the corresponding biome
	
	def save(self):
		pickle.dump(self, open(os.path.join(modutil.absolutePath, "world", "chunks", "c"+str(self.x)+"0"+str(self.y)), "wb"))
		
	def containsPos(self, _x, _y):
		return _x >= (self.x*Chunk.size) and _y >= (self.y*Chunk.size) and _x < ((self.x+1)*Chunk.size) and _y < ((self.y+1)*Chunk.size)

	def getRandomPos(self):
		return self.biomes[random.randint(0, size - 1)][random.randint(0, size - 1)]
		
class LandMass:
	def __init__(self, _id, _size, _name):
		self.id = _id
		self.name = _name
		self.size = _size

	def save(self):
		pickle.dump(self, open(os.path.join(modutil.absolutePath, "world", "chunks", "m"+str(self.id)), "wb"))

	def load(_id):
		return pickle.load(open(os.path.join(modutil.absolutePath, "world", "chunks", "m"+str(_id)), "rb"))
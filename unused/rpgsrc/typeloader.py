from .datatypes import BiomeType, LocationType, WAttribute, WeaponType, EnemyType
from libs import modutil
import os

def loadLocationTypes():
	# Load locationtype declarations
	with open(os.path.join(modutil.absolutePath, "lang/spanish/rpgData.txt"),"r", encoding="utf8") as f:
		chunk = f.readline().rstrip("\n")
		while chunk != "eof":
			if chunk == "":
				pass
			elif chunk[0:2] == "$$":
				# Location declaration
				LocationType(chunk[2:])
				
			chunk = f.readline().rstrip("\n")

		f.close()
		
	# Add locationtype connections
	with open(os.path.join(modutil.absolutePath, "lang/spanish/rpgData.txt"),"r", encoding="utf8") as f:
		chunk = f.readline().rstrip("\n")
		selectedLocation = None
		while chunk != "eof":
			if chunk == "":
				pass
			elif chunk[0:2] == "$$":
				# Declaration; select location
				selectedLocation = LocationType.get(chunk[2:])
			elif chunk[0:2] == "$ ":
				# Name
				selectedLocation.name = chunk[2:]
			elif chunk[0:3] == "$->":
				# Possible connection to location
				selectedLocation.possibleLocationsConnected.append(LocationType.get(chunk[3:]))
			elif chunk[0:2] == "$g":
				# Gender
				gender = False if chunk[2:].lstrip(" ") == "M" else True
				selectedLocation.gender = gender
			elif chunk[0:2] == "$l":
				# Loot types
				selectedLocation.lootTypes.append(chunk[2:])
				
			chunk = f.readline().rstrip("\n")

		f.close()

def loadWeaponAttributes():
	with open(os.path.join(modutil.absolutePath, "lang/spanish/rpgData.txt"),"r", encoding="utf8") as f:
		chunk = f.readline().rstrip("\n")
		selectedWAttribute = None
		while chunk != "eof":
			if chunk == "":
				pass
			elif chunk[0:2] == "^ ":
				WAttribute(chunk[2:])
				selectedWAttribute = WAttribute.all[-1]
			elif chunk[0:2] == "^f":
				selectedWAttribute.nameF = chunk[2:]
			elif chunk[0:2] == "^t":
				selectedWAttribute.type = chunk[2:]
			elif chunk[0:2] == "^c":
				selectedWAttribute.classification = chunk[2:]
			elif chunk[0:2] == "^a":
				selectedWAttribute.attackMod = float(chunk[2:])
			elif chunk[0:2] == "^g":
				selectedWAttribute.agilityMod = float(chunk[2:])
			elif chunk[0:2] == "^p":
				selectedWAttribute.probability = int(chunk[2:])
				WAttribute.probabilitySum += int(chunk[2:])
				
			chunk = f.readline().rstrip("\n")

		f.close()
		
def loadWeaponTypes():
	# Add weapontype declarations and attributes
	with open(os.path.join(modutil.absolutePath, "lang/spanish/rpgData.txt"),"r", encoding="utf8") as f:
		chunk = f.readline().rstrip("\n")
		selectedWeapon = None
		while chunk != "eof":
			if chunk == "":
				pass
			elif chunk[0:2] == "**":
				selectedWeapon = WeaponType(chunk[2:])
				selectedWeapon.attributes.append("NORMAL") # Have normal attributes by default
			elif chunk[0:2] == "* ":
				selectedWeapon.name = chunk[2:]
			elif chunk[0:2] == "*t":
				selectedWeapon.stype = chunk[2:]
			elif chunk[0:2] == "*g":
				gender = False if chunk[2:].lstrip(" ") == "M" else True
				selectedWeapon.gender = gender
			elif chunk[0:2] == "*a":
				selectedWeapon.attack = int(chunk[2:])
			elif chunk[0:2] == "*l":
				selectedWeapon.agility = int(chunk[2:])
			elif chunk[0:2] == "*d":
				selectedWeapon.hands = 2 if chunk[2:] == "Double" else 1
			elif chunk[0:2] == "*r":
				# Loot type + rarity
				selectedWeapon.lootConnections.append((chunk[2:].split(":")[0], int(chunk[2:].split(":")[1])))
			elif chunk[0:4] == "*-->":
				selectedWeapon.attributes.append(chunk[4:])
				
			chunk = f.readline().rstrip("\n")

		f.close()
		
def loadBiomeTypes():
	# Load biometype declarations
	with open(os.path.join(modutil.absolutePath, "lang/spanish/rpgData.txt"),"r", encoding="utf8") as f:
		chunk = f.readline().rstrip("\n")
		while chunk != "eof":
			if chunk == "":
				pass
			elif chunk[0:2] == "&&":
				# Biome declaration
				x = BiomeType(chunk[2:], {}, [], "#", False)
				
			chunk = f.readline().rstrip("\n")

		f.close()

	# Load biome attributes
	with open(os.path.join(modutil.absolutePath, "lang/spanish/rpgData.txt"),"r", encoding="utf-8") as f:
		chunk = f.readline().rstrip("\n")
		selectedBiome = None
		bnearthis = 100
		while chunk != "eof":
			if chunk == "":
				pass
			elif chunk[0:2] == "&&":
				if selectedBiome!=None:
					selectedBiome.possibleBiomesNear[selectedBiome] = bnearthis
				selectedBiome = BiomeType.get(chunk[2:])
				bnearthis = 100
			elif chunk[0:2] == "& ":
				selectedBiome.name = chunk[2:]
			elif chunk[0:3] == "&->":
				possiblePlace = BiomeType.get(chunk[3:].split(":")[0])
				# Possible place to go
				selectedBiome.possibleBiomesNear[possiblePlace] = int(chunk[3:].split(":")[1])
				bnearthis-=int(chunk[3:].split(":")[1])
			elif chunk[0:3] == "&o>":
				# Possible location
				selectedBiome.possibleLocations.append(LocationType.get(chunk[3:]))
			elif chunk[0:2] == "&g":
				gender = False if chunk[2:].lstrip(" ") == "M" else True
				selectedBiome.gender = gender
			elif chunk[0:2] == "&e":
				selectedBiome.emoji = chunk[2]
			elif chunk[0:2] == "&p":
				selectedBiome.properties.append(chunk[2:])
				if chunk[2:] == "PRIORITIZED":
					print("Added prioritized biometype!")
					BiomeType.prioritized = selectedBiome
				
			chunk = f.readline().rstrip("\n")
			
		selectedBiome.possibleBiomesNear[selectedBiome] = bnearthis
		f.close()
		
def loadEnemyTypes():
	with open(os.path.join(modutil.absolutePath, "lang/spanish/rpgData.txt"),"r", encoding="utf8") as f:
		chunk = f.readline().rstrip("\n")
		selectedEnemy = None
		while chunk != "eof":
			if chunk == "":
				pass
			elif chunk[0:2] == "!!":
				selectedEnemy = EnemyType(chunk[2:])
			elif chunk[0:2] == "! ":
				selectedEnemy.name = chunk[2:]
			elif chunk[0:2] == "!h":
				selectedEnemy.hp = int(chunk[2:])
			elif chunk[0:2] == "!g":
				gender = False if chunk[2:].lstrip(" ") == "M" else True
				selectedEnemy.gender = gender
			elif chunk[0:2] == "!m":
				selectedEnemy.attackMultiplier = float(chunk[2:])
			elif chunk[0:2] == "!a":
				selectedEnemy.attributes.append(chunk[2:])
			elif chunk[0:2] == "!x":
				selectedEnemy.xpDrop = int(chunk[2:])
			elif chunk[0:2] == "!l":
				# Found in + rarity
				selectedEnemy.foundIn[chunk[2:].split(":")[0]] = int(chunk[2:].split(":")[1])
			elif chunk[0:2] == "!w":
				for wps in chunk[2:].split("|"):
					selectedEnemy.weaponsPossible.append(tuple(map(lambda wp: WeaponType.get(wp), wps.split(";"))))
				
			chunk = f.readline().rstrip("\n")

		f.close()

def loadAll():
	loadLocationTypes()
	loadWeaponAttributes()
	loadWeaponTypes()
	loadBiomeTypes()
	#loadEnemyTypes()
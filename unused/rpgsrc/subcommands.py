import discord, asyncio, random, time
from . import world, worldToImage, rpglang, menus
from .datatypes import RPGUser, BiomeType, LocationType, Biome, Location, ItemType, Item, Weapon, WeaponType, WAttribute, Chunk
from libs import modutil
from ..rpg import rpgcmd
from discord.ext import commands
import discord

def check_if_user_is_loaded(ctx):
	return RPGUser.isLoaded(ctx.message.author.id)

@rpgcmd.command(name="user")
async def userSubCommand(ctx, *args):
	_u = RPGUser.get(args[0])
	
	_toSend = "```\n---- USER ----\nID: {id}\nPosition: ({x}, {y})\nFighters: {fighters}\nTutorialDone: {tutorialState}\nInventory: {inv}```".format(
	id = _u.id,
	x = _u.x,
	y = _u.y,
	fighters = ", ".join(list(map(lambda f: f.name, _u.fighters))),
	tutorialState = str(_u.tutorialDone),
	inv = ", ".join(list(map(lambda f: f.getFullName(), _u.inventory))) if len(_u.inventory) > 0 else "(Nothing)"
	)
	
	await ctx.send(_toSend)
	
@rpgcmd.command(name="loc")
async def infoSubCommand(ctx, *args):
	_x = int(args[0])
	_y = int(args[1])
	_b = world.getPos(_x, _y)
	
	_toSend = "```\n---- BIOME ----\nType: {type}\nx, y: ({x}, {y})\nLoot: {loot}\nLocation Connected: {location}".format(
	type = _b.stype,
	x = _b.x,
	y = _b.y,
	loot = ", ".join(list(map(lambda l: l.getType().name,_b.loot))) if len(_b.loot) > 0 else "(Nothing)",
	location = _b.locationConnected.getType().systemName if _b.locationConnected != None else "None"
	)
	
	if _b.locationConnected != None:
		_l = _b.locationConnected
		_toSend = _toSend + "\n\n---- LOCATION ----\nType: {type}\nrecursion: {recursion}\nConnections: {connections}\nLoot: {loot}".format(
		type = _l.stype,
		recursion = _l.recursion,
		connections = ", ".join(list(map(lambda l: l.getType().systemName, _l.connections))) if len(_l.connections) > 0 else "(Nothing)",
		loot = ", ".join(list(map(lambda l: l.getType().systemName, _l.loot))) if len(_l.loot) > 0 else "(Nothing)"
		)
	
	await ctx.send(_toSend + "```")
	
@rpgcmd.command(name="tp")
async def tpSubCommand(ctx, *args):
	if len(args) == 1: # tp player
		user = RPGUser.get(ctx.message.author.id)
		_x = int(RPGUser.get(args[0]).x)
		_y = int(RPGUser.get(args[0]).y)
	elif len(args) == 2: # tp x y
		_x = int(args[0])
		_y = int(args[1])
		user = RPGUser.get(ctx.message.author.id)
	elif len(args) == 3: # tp player x y
		user = RPGUser.get(args[0])
		_x = int(args[1])
		_y = int(args[2])
	else:
		await ctx.send("`Usage: rpg tp <player [x y] / x y>`")
		return

	if user==None:
		await ctx.send(rpglang.getl("USER_NOT_REGISTERED"))
		return
	user.setPos(_x, _y)
	await ctx.send("Teleported {} to ({}, {}).".format(user.getName(), _x, _y))
	
@rpgcmd.group(invoke_without_command=True, name="data")
async def datacmd(ctx):
	await ctx.send("`Usage: rpg data <biome/location/weapon/wattribute> [systemname]`")

@datacmd.command(name="biome")
async def data_biomecmd(ctx, *args):
	if len(args) > 0:
		_x = list(filter(lambda n: n.systemName == args[0], BiomeType.all.values()))[0]
		_toSend = "```\n--------- Biome ---------\nname: {name}\npossibleBiomesNear: {possibleBiomesNear}\npossibleLocations: {possibleLocations}\ngender: {gender}\nemoji: {emoji}```".format(
		name = _x.name,
		possibleBiomesNear = ",".join(list(map(lambda n: n.name, _x.possibleBiomesNear.keys()))),
		possibleLocations = ",".join(list(map(lambda n: n.name, _x.possibleLocations))),
		gender = "Female" if _x.gender else "Male",
		emoji = _x.emoji)
			
		await ctx.send(_toSend)
	else:
		await ctx.send("```\nBiomes:\n{}```".format("\n".join(list(map(lambda b: b.systemName,BiomeType.all.values())))))
			
@datacmd.command(name="location")
async def data_locationcmd(ctx, *args):
	await ctx.send("```\nLocations:\n{}```".format("\n".join(list(map(lambda b: b.systemName,LocationType.all.values())))))

@datacmd.command(name="weapon")
async def data_weaponcmd(ctx, *args):
	await ctx.send("```\nWeapons:\n{}```".format("\n".join(list(map(lambda b: b.systemName,WeaponType.all.values())))))
	
@datacmd.command(name="wattribute")
async def data_wattcmd(ctx, *args):
	if len(args) > 0:
		_x = list(filter(lambda n: n.nameM == args[0], WAttribute.all))[0]
		_toSend = "```\n--------- wAttribute ---------\nnameM: {nameM}\nnameF: {nameF}\ntype: {type}\nclassification: {classification}\nattackMod: {attackMod}\nagilityMod: {agilityMod}```".format(
		nameM = _x.nameM,
		nameF = _x.nameF,
		type = _x.type,
		classification = _x.classification,
		attackMod = _x.attackMod,
		agilityMod = _x.agilityMod)
			
		await ctx.send(_toSend)
	else:
		await ctx.send("```\nWeapon Adjectives:\n{}```".format("\n".join(list(map(lambda b: b.nameM,WAttribute.all)))))
	

# Sends a map of the world to a channel.
@rpgcmd.command(name="map")
async def worldSubCommand(ctx, *args):
	user = RPGUser.get(ctx.message.author.id)
	if user==None:
		await ctx.send(rpglang.getl("USER_NOT_REGISTERED"))
		return

	cx = int(args[0]) * Chunk.size
	cy = int(args[1]) * Chunk.size
	ux = user.x
	uy = user.y
	worldmap = ""
	for iy in range(cx, cx + Chunk.size):
		for ix in range(cy, cy + Chunk.size):
			if ux == ix and uy == iy:
				worldmap += "X"
			elif world.getPos(ix,iy).locationConnected != None:
				worldmap += "C"
			else:
				worldmap += world.getPos(ix,iy).getType().emoji
		worldmap += "\n"
		
	worldmap.rstrip("\n")
	
	worldToImage.represent(worldmap, modutil.absolutePath + "/map.png")
	
	await ctx.send(file=discord.File(modutil.absolutePath + "/map.png"))

@rpgcmd.command(name="save")
async def saveSubCommand(ctx, *args):
	RPGUser.saveAll()
	await ctx.send("Saved!")
	
@rpgcmd.command(name="inv")
async def invSubCommand(ctx):
	user = RPGUser.get(ctx.message.author.id)
	if user==None:
		await ctx.send(rpglang.getl("USER_NOT_REGISTERED"))
		return

	await menus.showInventoryMenu(ctx, user)

@rpgcmd.command(name="s")
async def startSubCommand(ctx):
	user = RPGUser.get(ctx.message.author.id)
	if user==None:
		await ctx.send(rpglang.getl("USER_NOT_REGISTERED"))
		return

	if not user.tutorialDone:
		await menus.showTutorialMenu(ctx, user)
	else:
		await menus.showActionMenu(ctx, user, rpglang.getl("CONTINUE_ADVENTURE"))
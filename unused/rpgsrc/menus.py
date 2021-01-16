import discord, asyncio, random, time
from . import world, rpglang
from .datatypes import RPGUser, BiomeType, LocationType, Biome, Location, ItemType, Item, Weapon, WeaponType, WAttribute
from .. import rpg
from libs import modutil

async def sendEmbed(ctx, _msg, _title, _footer = "Retramonger PG", _thumb = None):
	embed=discord.Embed(description=_msg)
	embed.set_author(name=_title, icon_url="https://cdn.discordapp.com/avatars/461294492121694209/168015a6373496a6472bcf25eb86e717.jpg")
	if _thumb!=None:
		embed.set_thumbnail(url=_thumb)
	embed.set_footer(text=_footer)
	return await ctx.send(embed=embed)

# Sends a menu with information about an user's fighters and status.
async def showUserMenu(ctx, user):
	embed=discord.Embed(title=" ")
	embed.set_author(name="Retramonger PG -- {}".format(user.name), icon_url="https://cdn.discordapp.com/avatars/461294492121694209/168015a6373496a6472bcf25eb86e717.jpg")
	embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/435805657611108362/563063176779005952/vsaus.jpg")
	embed.add_field(name="Level & XP", value="Level {} ({} / {} xp)".format(user.level, user.xp, user.getXpForNextLevel()), inline=True)
	embed.add_field(name="HP", value="{} / {}".format(user.hp, user.maxhp),inline = True)
	embed.set_footer(text=rpglang.getl("MENU_FOOTER"))
	await ctx.send(embed=embed)
	
async def showInventoryMenu(ctx, user):
	# Make the message out of the items in the player's inventory
	_toSend = "\n".join(list(map(lambda i: i.getFullName(),user.inventory)))
	
	# If inventory is empty, show #EMPTY_INVENTORY
	if _toSend == "":
		_toSend = rpglang.getl("EMPTY_INVENTORY")
		
	# Send the message along with #INVENTORY as title
	await sendEmbed(ctx, _toSend,_title = rpglang.getl("INVENTORY").format(user.getName()))

async def showItemMenu(ctx, user):
	if user.isInsideLocation():
		loot = user.locPos.loot
	else:
		loot = world.getPos(user.x, user.y).loot
	_loot = ", ".join(list(map(lambda l: l.getFullNameWithDeterminant(),loot)))
	_toSend = rpglang.getl("LOOT_SEARCHED").format(_loot)
	_toGet = loot[0]
	msg = await sendEmbed(ctx, _msg=_toSend, _title = rpglang.getl("LOOT_SEARCHED_TITLE"))
	
	await msg.add_reaction("✅")
	await msg.add_reaction("❎")

	allowedReactions = ["✅","❎"]
	
	def check(reaction, user):
		return user == ctx.message.author and str(reaction.emoji) in allowedReactions

	try:
		rec, usr = await rpg.bot.wait_for("reaction_add", timeout = 30.0, check=check)
	except asyncio.TimeoutError:
		await ctx.send(rpglang.getl("REACTION_TIMEOUT"))
		return
	
	_lootArticle = ", ".join(list(map(lambda l: l.getFullNameWithArticle(),loot)))
	if rec.emoji == "✅":
		if len(loot) == 0:
			await ctx.send(rpglang.getl("LOOT_DOES_NOT_EXIST"))
		elif _toGet != loot[0]:
			await ctx.send(rpglang.getl("LOOT_DOES_NOT_EXIST"))
		else:
			await ctx.send(rpglang.getl("LOOT_PUT_IN_INVENTORY").format(_lootArticle))
			# Add item to user's inventory
			user.inventory.append(loot[0])
			# Delete item from biome/location's loot list
			del loot[0]
			# Show the player its inventory
			await showInventoryMenu(ctx, user)
	else:
		await ctx.send(rpglang.getl("LOOT_LEFT_IN_LOCATION").format(_lootArticle))

# Shows an user the possible actions they can do, such as moving, fighting, picking up items...
async def showActionMenu(ctx, user, _actionBefore = ""):
	if _actionBefore != "":
		_actionBefore += "\n\n"

	print("User {}: ({}, {})".format(user.getName(), user.x, user.y))
	_biome = world.getPos(user.x, user.y).getType().getNameWithDeterminant()
	
	allowedReactions = []
	
	_thingsSeeing = ""
	
	if not user.isInsideLocation():
		if (user.x, user.y) in list(map(lambda u: None if user == u else (u.x, u.y), RPGUser.all.values())):
			_thingsSeeing = "\n\n" + rpglang.getl("SEEING_USER").format(list(filter(lambda u: False if user == u else (u.x, u.y) == (user.x, user.y), RPGUser.all.values()))[0].getName())
		
		if world.getPos(user.x, user.y).locationConnected != None:
			_thingsSeeing += "\n" + rpglang.getl("LOCATION_IN_BIOME").format(world.getPos(user.x, user.y).locationConnected.getType().getNameWithDeterminant())
			
			_thingsSeeing += " " + rpglang.getl("LOCATION_HAS_CONNECTIONS_IN_BIOME")
			allowedReactions.append("📥")
		
		
		def getBiome(x, y):
			return world.getPos(x,y).getType().getNameWithDeterminant() if world.isPositionValid(x,y) else "un acantilado"

		_n = "⬆"+rpglang.getl("THING_IN_DIRECTION").format(rpglang.getl("NORTH"), getBiome(user.x, user.y-1))
		_s = "⬇"+rpglang.getl("THING_IN_DIRECTION").format(rpglang.getl("SOUTH"), getBiome(user.x, user.y+1))
		_e = "➡"+rpglang.getl("THING_IN_DIRECTION").format(rpglang.getl("EAST"), getBiome(user.x+1, user.y))
		_w = "⬅"+rpglang.getl("THING_IN_DIRECTION").format(rpglang.getl("WEST"), getBiome(user.x-1, user.y))
		
		if world.isPositionValid(user.x, user.y-1):
			allowedReactions.append("⬆")
		if world.isPositionValid(user.x, user.y+1):
			allowedReactions.append("⬇")
		if world.isPositionValid(user.x-1, user.y):
			allowedReactions.append("⬅")
		if world.isPositionValid(user.x+1, user.y):
			allowedReactions.append("➡")
		
		_thingsSeeing+="\n\n{}\n{}\n{}\n{}".format(_n, _s, _e, _w)
		
		_tosend = _actionBefore + world.getPos(user.x, user.y).getType().emoji + rpglang.getl("ACTION_MENU_IN_BIOME").format(_biome,_thingsSeeing)
	else:
		allowedReactions.append("📤")
		
		if len(user.locPos.connections) > 0:
			_thingsSeeing += " " + rpglang.getl("LOCATION_HAS_CONNECTIONS_IN_LOCATION")
			allowedReactions.append("📥")
			
		if len(user.locPos.loot) > 0:
			_thingsSeeing += "\n" + rpglang.getl("LOOT_IN_LOCATION").format(", ".join(list(map(lambda l: l.getType().getNameWithDeterminant(),user.locPos.loot))))
			allowedReactions.append("🔍")
		
		_location = user.locPos.getType().getNameWithDeterminant()
		_tosend = _actionBefore + world.getPos(user.x, user.y).getType().emoji + rpglang.getl("ACTION_MENU_IN_LOCATION").format(_location,_biome,_thingsSeeing)
	
	# Set default nothing seen in biome message if nothing was set
	if _thingsSeeing == "":
		_thingsSeeing = " " + rpglang.getl("NOTHING_IN_BIOME")
		
	_totitle = rpglang.getl("ACTION_MENU_TITLE").format(user.getName())
	
	msg = await sendEmbed(ctx, _tosend, _title = _totitle)
	
		
	for r in allowedReactions:
		await msg.add_reaction(r)
	
	def check(reaction, user):
		return user == ctx.message.author and str(reaction.emoji) in allowedReactions

	try:
		rec, usr = await rpg.bot.wait_for("reaction_add", timeout = 30.0, check=check)
	except asyncio.TimeoutError:
		await ctx.send(rpglang.getl("REACTION_TIMEOUT"))
		return
	
	_actionNext = ""
	if rec.emoji == "⬆":
		user.move(0,-1)
		_actionNext = rpglang.getl("ACT_MOVE").format(rpglang.getl("NORTH"))
	if rec.emoji == "⬇":
		user.move(0,1)
		_actionNext = rpglang.getl("ACT_MOVE").format(rpglang.getl("SOUTH"))
	if rec.emoji == "⬅":
		user.move(-1,0)
		_actionNext = rpglang.getl("ACT_MOVE").format(rpglang.getl("WEST"))
	if rec.emoji == "➡":
		user.move(1,0)
		_actionNext = rpglang.getl("ACT_MOVE").format(rpglang.getl("EAST"))
		
	if rec.emoji == "📥":
		user.moveIntoLoc(user.locPos.connections[0] if user.isInsideLocation() else world.getPos(user.x, user.y).locationConnected)
		_actionNext = rpglang.getl("ACT_ENTER_LOCATION").format(user.locPos.getType().getNameWithArticle())
	if rec.emoji == "📤":
		_actionNext = rpglang.getl("ACT_EXIT_LOCATION").format(user.locPos.getType().getNameWithArticle()).replace("de el", "del")
		user.moveIntoLoc(user.locPos.parentLoc)
	
	if rec.emoji == "🔍":
		await showItemMenu(ctx,user)
		
	# Create new async Action Menu task
	asyncio.ensure_future(showActionMenu(ctx, user, _actionNext))

# Makes an user start the tutorial.
async def showTutorialMenu(ctx, user):
	await sendEmbed(ctx, rpglang.getl("TUTORIAL_1").format(world.getPos(user.x, user.y).getType().getNameWithDeterminant()), _title = rpglang.getl("NEW_ADVENTURE"))
	await sendEmbed(ctx, rpglang.getl("TUTORIAL_2"), _title = rpglang.getl("NEW_ADVENTURE"))
	msg = await ctx.send(rpglang.getl("TUTORIAL_3"))
	await msg.add_reaction("✅")

	def check(reaction, user):
		return user == ctx.message.author and str(reaction.emoji) == "✅"

	try:
		await rpg.bot.wait_for("reaction_add", timeout = 30.0, check=check)
	except asyncio.TimeoutError:
		await ctx.send(rpglang.getl("REACTION_TIMEOUT"))
	else:
		user.tutorialDone = True
		await showActionMenu(ctx, user)
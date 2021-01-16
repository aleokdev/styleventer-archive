#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Typing used to specify what do functions return and what type variables hold
from typing import List

# IMPORTS #
import asyncio
import discord
import json
import random
from discord.ext import commands
from libs import modutil, assets


# DEPRECATED #

class Action:
    """Deprecated. Don't use."""
    actionBase = ["You spawn on {}.", "You grab the {}.", "You shoot {}!", "You carefully aim at {}.",
                  "You heal yourself with the {} you had in your backpack."]


# GLOBAL VARIABLES #

# lobby: List<Fighter>. Contains all users present in the game.
lobby = []
# turnNo: Turn number. Starts at 1.
turnNo = 1

bot = None

# Map. List of MapZones. No bidimensionality, use mapSize as pitch.
world = []
worldSize = 5

# The percentage of times the bullet will fail to hit a target when the user is not aiming.
noaimRisk = 50.0


class MapZone:
    """
    Depicts a zone inside the map.

    Attributes
    ----------
    self.weapons : list<Weapon>
        Contains all the weapons of this MapZone.
    self.throwables : list<Throwables>
        Contains all the throwables of this MapZone.
    self.x : int
        X Position of this zone.
    self.y : int
        Y Position of this zone.
    """

    def __init__(self, x, y):
        self.weapons = []
        self.throwables = []
        self.x = x
        self.y = y

    def __str__(self):
        return "<MapZone at {}, {} with {} weapons and {} throwables>".format(self.x, self.y, len(self.weapons),
                                                                              len(self.throwables))

    @property
    def fighters(self):
        return list(filter(lambda f: f.x == self.x and f.y == self.y, lobby))


def replaceLast(s, old, new):
    li = s.rsplit(old, 1)
    return new.join(li)


async def addReactionsAndWait(msg, userToCheck, reactions: List[str]) -> discord.Reaction:
    for reaction in reactions:
        await msg.add_reaction(reaction)

    def check(reaction, user):
        return str(reaction.emoji) in reactions and user == userToCheck and user != bot.user

    rec, user = await bot.wait_for("reaction_add", check=check)
    return rec


defaultAttributes = {}

weaponData = []


class NullWeapon:
    def __init__(self):
        self.id = None

    def __getattr__(self, name):
        return None


class Weapon(NullWeapon):
    def __init__(self, id):
        self.id = id

    def __getattr__(self, name):
        try:
            return weaponData[self.id][name]
        except:
            return defaultAttributes[name]


throwableData = []


class Throwable:
    def __init__(self, _id):
        self.id = _id

    def __getattr__(self, name):
        try:
            return throwableData[self.id][name]
        except:
            return defaultAttributes[name]


covers = []


class Fighter:
    # Fighter.bodyParts
    # Contains a dict with the name of each body part as key
    # and a tuple containing the percentage to hit as first value
    # and the health of the part as second value.
    bodyParts = {"Left shoulder": (6, 50),
                 "Right shoulder": (6, 50),
                 "Left arm": (7.5, 30),
                 "Right arm": (7.5, 30),
                 "Chest": (40, 100),
                 "Head": (9, 50),
                 "Left leg": (12, 40),
                 "Right leg": (12, 40)}

    def __init__(self, userID):
        self.id = userID
        self.user = bot.get_user(userID)
        self.isReady = False
        self.x = 0  # random.randint(0, mapSize-1)
        self.y = 0  # random.randint(0, mapSize-1)
        self.healthState = {}
        for bodyPart in Fighter.bodyParts.keys():
            self.healthState[bodyPart] = Fighter.bodyParts[bodyPart][1]
        self.equippedWeapon = None
        self.throwables = []
        self.aiming_at: Fighter = None

    @property
    def zone(self) -> MapZone:
        return world[self.x + self.y * worldSize]

    @property
    def dead(self) -> bool:
        return self.healthState["Head"] == 0 or self.healthState["Chest"] == 0

    def beFiredAt(self, weapon: Weapon, isAiming: bool) -> (str, int):
        """

        :param weapon: The weapon to use to fire to this fighter.
        :param isAiming: Is the other user aiming at this fighter?
        :return: Returns a tuple with a string and an int.
                 The string depicts which bodypart of the user has been affected (None if missed)
                 The int depicts how much damage the user has been dealed on that bodypart
        """
        if not isAiming:
            if noaimRisk >= random.randint(1, 100):
                return None, 0

        # i am not sure if this is 100% correctly random but it works so it ok
        randBodypartNum = random.randint(1, 100)
        bodypartAffected: str = None
        for bodypart, value in Fighter.bodyParts.items():
            randBodypartNum -= value[0]
            if randBodypartNum <= 1:
                bodypartAffected = bodypart
        # todo: implement weapon area damage

        self.healthState[bodypartAffected] -= weapon.damage
        return bodypartAffected, weapon.damage


    async def seeFightersMenu(self, otherFighters, lastAction=None) -> (bool, str):
        """
        Sends an embed message to the user saying that they've seen one or many fighters,
        and allows them to choose what they want to do.
        :param otherFighters: The list of fighters the user has seen.
        :param lastAction: The last action result, if any. (i.e. "You aim at the user", etc)
        :return: Bool is true only if the user's turn should end.
                 str is the action result of this menu.
        """
        embed = discord.Embed(title=f"Turn {turnNo}", description=lastAction)
        fighters_str = replaceLast(", ".join(list(map(lambda f: f.user.name, otherFighters))), ",", " and")
        base = ""
        base += f"At the distance, you recognize {fighters_str}."

        embed.add_field(name="You see someone!", value=base, inline=False)

        availableReactions = []
        if len(otherFighters) == 1:
            actions = ""
            if self.equippedWeapon is not None:
                actions += "🔫 Attack with your main weapon without aiming first\n"
                actions += "🔻 Aim with your main weapon\n"
                availableReactions.extend(["🔫", "🔻"])
            if len(self.throwables) > 0:
                actions += "🗡 Throw something at them...\n"
                availableReactions.append("🗡")
            actions += """🔎 Stand still and keep an eye on them
            ❌ Ignore them and do something else
            """
            availableReactions.extend(["🔎", "❌"])
            embed.add_field(name="Actions available", value=actions, inline=False)
        else:
            actions = ""
            for i, fighter in enumerate(otherFighters):
                actions += "{} Interact with {}...\n".format(str(i) + "⃣", fighter.user.name)
            actions += "❌ Ignore them and do something else"
            availableReactions = list(str(i) + "⃣" for i in range(len(otherFighters)))
            availableReactions.extend("❌")
            embed.add_field(name="Actions available", value=actions, inline=False)

        msg = await self.user.send(embed=embed)
        if len(otherFighters) > 1:
            reaction = await addReactionsAndWait(msg, self.user, availableReactions)
            if str(reaction.emoji) == "❌":
                return False, "You ignore them."  # Continue turn
            return await self.seeFightersMenu([otherFighters[int(str(reaction.emoji)[0])]])
        else:
            reaction = await addReactionsAndWait(msg, self.user, availableReactions)
            if str(reaction.emoji) == "🔫": # todo: fix shooting without aiming (doesn't return message?)
                bodypartAffected, damage = otherFighters[0].beFiredAt(weapon=self.equippedWeapon, isAiming=False)
                resultingAction = "You fire at {}. ".format(otherFighters[0].name)
                if bodypartAffected is None:
                    resultingAction += "The bullet misses completely, and they notice you!"
                else:
                    resultingAction += f"The bullet hits them, causing them damage in the {bodypartAffected}!"
                return True, resultingAction

            if str(reaction.emoji) == "🔻": # todo: completely add aiming (next turn, choose between aim again, stop aiming or shoot)
                self.aiming_at = otherFighters[0]
                return True, "You aim at " + otherFighters[0].name + "."

            if str(reaction.emoji) == "❌":
                return False, "You ignore them."  # Continue turn

    async def seeItemsMenu(self, items, zoneToGrabFrom: MapZone, lastAction=None)-> (bool, str):
        """
            Sends an embed message to the user saying that they've seen one or many items,
            and allows them to choose what they want to do with them.
            :param items: The list of items (Weapons and throwables) the user has seen.
            :param lastAction: The last action result, if any. (i.e. "You aim at the user", etc)
            :return: Bool is true only if the user's turn should end.
                     str is the action result of this menu.
        """
        embed = discord.Embed(title=f"Turn {turnNo}", description=lastAction)
        base = ""
        print(len(items), items)
        actual_items = list(filter(lambda i: type(i) is Weapon or type(i) is Throwable, items))
        if len(actual_items) == 0:
            return False, "You couldn't find anything on the ground..."
        items_str = replaceLast(", ".join(list(map(lambda i: i.name, actual_items))), ",", " and")
        if len(actual_items) == 1:
            base += f"While you were walking around, you saw a {actual_items[0].name} on the ground."
        else:
            base += f"While you were walking around, you saw some items on the ground."

        base += "\nWhat will you do now?"

        embed.add_field(name="You found something!", value=base)

        availableReactions = list(str(i) + "⃣" for i in range(len(actual_items)))
        availableReactions.append("❌")
        actions = ""
        for index, item in enumerate(actual_items):
            if type(item) is Weapon:
                actions += f"{index}⃣ Equip the {item.name}\n"
            elif type(item) is Throwable:
                actions += f"{index}⃣ Grab the {item.name}\n"
        actions += "❌ Don't grab anything and continue"
        embed.add_field(name="Actions", value=actions)

        msg = await self.user.send(embed=embed)
        reaction = await addReactionsAndWait(msg, self.user, availableReactions)
        if str(reaction.emoji) == "❌":
            return False, None  # Continue turn
        else:
            itemToGrab = actual_items[int(str(reaction.emoji)[0])]
            if itemToGrab not in zoneToGrabFrom.weapons and itemToGrab not in zoneToGrabFrom.throwables:
                return False, f"W-What?! Someone was quicker than you and took the {itemToGrab.name} before you!"
            if type(itemToGrab) is Weapon:
                self.equippedWeapon = itemToGrab
                zoneToGrabFrom.weapons[zoneToGrabFrom.weapons.index(itemToGrab)] = NullWeapon()
                return True, "You equip the " + itemToGrab.name
            elif type(itemToGrab) is Throwable:
                self.throwables.append(itemToGrab)
                zoneToGrabFrom.throwables[zoneToGrabFrom.throwables.index(itemToGrab)] = NullWeapon()
                return True, "You grab the " + itemToGrab.name

    async def endTurnMenu(self, lastAction):
        embed = discord.Embed(title=f"Turn {turnNo}", description=lastAction)
        embed.add_field(name="End of turn", value="That's the end of your turn! Please wait until everyone has "
                                                  "finished choosing...")
        await self.user.send(embed=embed)

    async def showTurn(self):
        lastAction = f"You spawn in ({self.zone.x}, {self.zone.y})." if turnNo == 1 else "Next turn..."
        fightersInThisZone: list = self.zone.fighters
        if len(fightersInThisZone) > 1:
            fightersInThisZone.remove(self)
            shouldEnd, lastAction = await self.seeFightersMenu(fightersInThisZone, lastAction=lastAction)
            if shouldEnd:
                await self.endTurnMenu(lastAction)
                return
        itemsInThisZone: list = self.zone.weapons.copy()
        itemsInThisZone.extend(self.zone.throwables)
        if len(itemsInThisZone) > 0:
            shouldEnd, lastAction = await self.seeItemsMenu(itemsInThisZone, zoneToGrabFrom=self.zone, lastAction=lastAction)
            if shouldEnd:
                await self.endTurnMenu(lastAction)
                return
        await self.endTurnMenu(lastAction)


async def showLobbyPlayers(ctx):
    embed = discord.Embed(title="Battle Royale Lobby")
    fighterNames = ""
    for fighter in lobby:
        fighterNames += fighter.user.name + "\n"
    embed.add_field(name="Fighters", value=fighterNames)
    await ctx.send(embed=embed)


async def doRound():
    global turnNo
    futures = []
    for fighter in lobby:
        futures.append(asyncio.ensure_future(fighter.showTurn()))

    for future in futures:
        await future
    turnNo += 1


async def roundLoop():
    while len(list(filter(lambda f: not f.dead, lobby))) > 1:
        await doRound()


async def checkIfEveryoneReady(ctx):
    for fighter in lobby:
        if not fighter.isReady:
            return False

    await ctx.send("Everyone is ready!")
    return True


async def waitForReady(ctx, user):
    embed = discord.Embed(title="")
    embed.add_field(name="Battle Royale", value="Please react with the checkmark below when you're ready!")

    msg = await user.send(embed=embed)
    await msg.add_reaction("✅")

    def check(reaction, u):
        return str(reaction.emoji) == "✅" and u == user

    await ctx.bot.wait_for("reaction_add", check=check)
    await ctx.send("Reaction given by " + user.name)
    list(filter(lambda f: f.id == user.id, lobby))[0].isReady = True


async def waitForEveryoneReady(ctx):
    futures = []
    for fighter in lobby:
        futures.append(asyncio.ensure_future(waitForReady(ctx, fighter.user)))

    for future in futures:
        await future


async def startGame(ctx):
    await waitForEveryoneReady(ctx)
    await ctx.send("Everyone is ready, starting round loop")
    await roundLoop()
    await ctx.send(list(filter(lambda f: not f.dead, lobby))[0].user.name + " won the game!")


@commands.command(name="br", alias=["fortnite"], usage="<join>", hidden=True,
                  description="Join or create a battle royale game! You get options to choose from, only one can "
                              "survive!")
async def battleroyaleCmd(ctx, *args):
    if len(args) > 0:
        if args[0] == "join":
            if ctx.message.author.id not in map(lambda f: f.id, lobby):
                lobby.append(Fighter(ctx.message.author.id))
            else:
                await ctx.send("You've already joined the lobby!")
        if args[0] == "start":
            await startGame(ctx)

    await showLobbyPlayers(ctx)


def loadDefaults(json_string):
    global defaultAttributes
    defaultAttributes = json.loads(json_string)["defaults"]
    print(defaultAttributes)


def loadWeaponData(json_string):
    global weaponData
    weaponData = json.loads(json_string)["guns"]
    print(weaponData)


def loadThrowableData(json_string):
    global throwableData
    throwableData = json.loads(json_string)["throwables"]
    print(throwableData)


def loadCovers(json_string):
    global covers
    covers = json.loads(json_string)["covers"]
    print(covers)


def generateMap():
    for i in range(worldSize * worldSize):
        world.append(MapZone(x=i % worldSize, y=int(i / worldSize)))


def generateWeapons():
    for wpindex, wpdata in enumerate(weaponData):
        for i in range(int((wpdata["percent_amount"] / 100.0) * (worldSize * worldSize))):
            world[random.randint(0, worldSize - 1) * worldSize + random.randint(0, worldSize - 1)].weapons.append(
                Weapon(wpindex))


def generateThrowables():
    for tindex, tdata in enumerate(throwableData):
        for i in range(int((tdata["percent_amount"] / 100.0) * (worldSize * worldSize))):
            world[random.randint(0, worldSize - 1) * worldSize + random.randint(0, worldSize - 1)].throwables.append(
                Throwable(tindex))


def loadAllData():
    print("Loading all 'br data...")
    with open(assets.get("battleroyale.json"), "r") as f:
        string = f.read()
        loadDefaults(string)
        loadWeaponData(string)
        loadThrowableData(string)
        loadCovers(string)
    print("Done!")


def setup(_bot):
    global bot
    bot = _bot
    _bot.add_command(battleroyaleCmd)
    loadAllData()
    generateMap()
    generateWeapons()
    world[0].weapons.append(Weapon(0)) # todo: This is debug, remove
    generateThrowables()
    for zone in world:
        print(str(zone))

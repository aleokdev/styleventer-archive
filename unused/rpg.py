from libs import modutil
from .rpgsrc.datatypes import RPGUser, BiomeType, LocationType, Biome, Location, ItemType, Item, Weapon, WeaponType, WAttribute
import discord, os, random, asyncio,time
from .rpgsrc import datatypes, world, menus, worldToImage, typeloader, rpglang
from discord.ext import commands

bot = None

version = "0.1"

# Sends an embed message with the attributes specified.
async def sendEmbed(ctx, _msg, _title, _footer = "Retramonger PG v."+version):
    embed=discord.Embed(description=_msg)
    embed.set_author(name=_title, icon_url="https://cdn.discordapp.com/avatars/461294492121694209/168015a6373496a6472bcf25eb86e717.jpg")
    #embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/435805657611108362/563063176779005952/vsaus.jpg")
    embed.set_footer(text=_footer)
    return await ctx.send(embed=embed)

# Called when 'rpg is typed in.
@commands.group(invoke_without_command=True, name="OLD-NajDkw01-rpg", hidden=True,
                usage="[s / map / tp / inv / user / info / data / save]",
                description="Start a new adventure with 'rpg! Battle monsters, grab loot and visit new places, all inside of discord!\nTo start or continue your adventure, use 'rpg s.")

async def rpgcmd(ctx):
    uid = ctx.message.author.id
    if not RPGUser.isLoaded(uid):
        if RPGUser.existsSaveFile(uid):
            await ctx.send(rpglang.getl("DATA_LOADED"))
            RPGUser.load(uid)
        else:
            u = RPGUser(_id=uid, _x=int(world.worldSize/2), _y=int(world.worldSize/2), _name=ctx.message.author.name)
            await ctx.send(rpglang.getl("NEW_USER").format(ctx.message.author.name))

    user = RPGUser.get(uid)

    await menus.showUserMenu(ctx, user)

from .rpgsrc import subcommands

#--------------------- INIT ---------------------#
def setup(_bot, **kwargs):
    return


    global bot
    bot = _bot
    print("Parsing RPG locations...")
    typeloader.loadLocationTypes()

    print("Parsing RPG weapon attributes...")
    typeloader.loadWeaponAttributes()

    print("Parsing RPG weapons...")
    typeloader.loadWeaponTypes()

    print("Parsing RPG biomes...")
    typeloader.loadBiomeTypes()

    print("Adding commands...")
    bot.add_command(rpgcmd)
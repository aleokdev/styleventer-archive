from libs import modutil
from discord.ext import commands
import discord

@commands.command(name="potato")
async def testcmd(ctx):
    await ctx.send(":potato:{0}:potato:\n\n:potato:{0}:potato:".format(" "*50))
    
# Init
def setup(bot, **kwargs):
	bot.add_command(testcmd)
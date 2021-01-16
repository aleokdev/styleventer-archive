import os, random
from libs import modutil
from discord.ext import commands
import discord

memeDirs = []

# Functions
@commands.command(name="meme",
				  usage="",
				  description="do a funni")
@commands.check(modutil.check_if_semi_extended_server)
@commands.cooldown(1, 5, commands.BucketType.user)
async def memecmd(ctx):
	await ctx.send("Thanks for your participation in `memecmd`. Your actions have been recorded.")
	#x = random.choice(memeDirs)
	#await ctx.send(file = discord.File(os.path.join(modutil.absolutePath,"memes", x)), content = "`{}`".format(x))
	
# Init
def setup(bot, **kwargs):
	#global memeDirs
	#memeDirs = [f for f in os.listdir(os.path.join(modutil.absolutePath, "memes")) if os.path.isfile(os.path.join(modutil.absolutePath, "memes", f))]
	bot.add_command(memecmd)
	#print("{} memes initialized.".format(len(memeDirs)))
from libs import modutil, lang
from discord.ext import commands
import discord


@commands.command(name="fact", hidden=True)
async def factcmd(ctx):
	try:
		await ctx.send(lang.getl(ctx.guild, "randFun", "FUN"))
	except:
		await ctx.send("Not available in your country! (Just like Mother 3)")
    
# Init
def setup(bot, **kwargs):
	bot.add_command(factcmd)

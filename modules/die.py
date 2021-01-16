from discord.ext import commands
import os, sys

# Called when 'die is said
@commands.command(name="die",
				  usage="",
				  description="Kills the bot's process.")
@commands.is_owner()
async def diecmd(ctx):
	await ctx.send("Bruh")
	sys.exit()

def setup(bot, **kwargs):
	bot.add_command(diecmd)
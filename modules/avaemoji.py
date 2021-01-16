import discord
from discord.ext import commands

@commands.command(name="avaemoji")
@commands.is_owner()
async def avaemojiCmd(ctx):
	msg = await ctx.send("React with the emoji to edit.")
	reaction, user = await ctx.bot.wait_for("reaction_add")
	await reaction.emoji.edit(name="AVAEMOJI_EDIT", roles=[discord.Object(645274641056923661)])
	
def setup(bot):
	bot.add_command(avaemojiCmd)
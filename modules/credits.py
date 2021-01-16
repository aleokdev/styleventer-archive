import discord
from discord.ext import commands

@commands.command(name="credits", usage="",
				  description="Show the credits and thank-you-s for the bot.")
async def creditsCmd(ctx):
	embed=discord.Embed(title="", color=0x0b0b73)
	embed.add_field(name="Styleventer Credits", value=
"""Styleventer ©2018~2020 by aleok (AlexINF)

Congratulations to "has no idea of what he's doing" patataofcourse
and "big meme" WarThog for winning StylPRG19!

Big thanks to icarus for the fanart they made!""")
	await ctx.send(embed=embed)
	
def setup(bot):
	bot.add_command(creditsCmd)
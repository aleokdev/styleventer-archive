import discord
from discord.ext import commands
import discord.opus

bot = None

@commands.command(name="join", hidden=True)
@commands.is_owner()
async def joinCmd(ctx, *args):
	print(f"Joined voice channel {ctx.message.author.voice.channel.id}")
	voiceClient = await ctx.message.author.voice.channel.connect()
	print(" ".join(args).strip(" "))
	voiceClient.play(discord.FFmpegPCMAudio(" ".join(args).strip(" ")))

@commands.command(name="leave", hidden=True)
@commands.is_owner()
async def leaveCmd(ctx):
	await bot.voice_clients[0].disconnect()
	
def setup(_bot, **kwargs):
	global bot
	_bot.add_command(joinCmd)
	_bot.add_command(leaveCmd)
	bot = _bot
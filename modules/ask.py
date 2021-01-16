from libs import modutil
from discord.ext import commands
import discord

@commands.command(name="ask")
async def testcmd(ctx):
    await ctx.send("""Rule 2.1: **Actually ask your question.**\nPosting "Can somebody help me?" or similar messages is annoying and doesn't help anyone, including you.""")
    
# Init
def setup(bot, **kwargs):
	bot.add_command(testcmd)

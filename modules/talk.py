import discord
from discord.ext import commands

@commands.command(name="talk", aliases=["t"], hidden=True, description="Shhhh, it's a secret!")
async def cmdtalk(ctx, channel: int, msg: str):
    await ctx.bot.get_channel(channel).send(msg)

def setup(bot):
    bot.add_command(cmdtalk)
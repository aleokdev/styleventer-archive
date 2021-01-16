import png
import discord
from discord.ext import commands

import argparse


@commands.command(name="imgedit", hidden=True)
async def imgedit(ctx, *args):
    if len(ctx.message.attachments) != 1:
        await ctx.send("Please input one single image to imgedit.")
        return

    imagebytes = await ctx.message.attachments[0].read()
    image = png.Reader(bytes=imagebytes)
    await ctx.send("Editing.")

def setup(bot):
    bot.add_command(imgedit)
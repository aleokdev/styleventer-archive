from discord.ext import commands
import os, sys
from libs import modutil

default_args = ["-msg", "{ctx.message.channel.id}", "Successfully reset."]

# Called when 'reset is said
@commands.command(name="reset",
                  usage="",
                  description="Reboots the bot's script.")
@commands.is_owner()
async def resetcmd(ctx, *args):
    bot_args = args

    if len(args) == 0:
        await ctx.send("Resetting with default arguments.")
        bot_args = default_args

    bot_args = list(map(lambda arg: arg.format(ctx=ctx), bot_args))
    bot_args.insert(0, f"{modutil.absolutePath}/bot.py")
    await ctx.send(f"Reset command: `/usr/bin/python3 {' '.join(bot_args)}`")

    os.execv(f"/usr/bin/python3", bot_args)


def setup(bot, **kwargs):
    bot.add_command(resetcmd)

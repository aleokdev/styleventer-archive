from discord.ext import commands
import discord, sys, os
import traceback
import datetime
from libs import settings

async def oncmderror(ctx: discord.ext.commands.Context, error):
    if type(error) == commands.CommandOnCooldown:
        if int(error.retry_after) == 0:
            await ctx.send("Wait a few seconds before using this command again!")
        else:
            await ctx.send("Wait at least {} more seconds to use this command again!".format(int(error.retry_after)))
    elif type(error) == commands.CommandNotFound:
        setting = settings.get_setting("prefix_response_channels", [ctx.message.guild.id])
        if setting is None:
            await ctx.send("Command `{}` doesn't exist!".format(ctx.message.content.split()[0]))
        elif str(ctx.message.channel.id) in setting:
            await ctx.send("Command `{}` doesn't exist!".format(ctx.message.content.split()[0]))
    elif type(error) == commands.errors.NotOwner:
        await ctx.send("That command is only usable by aleok.")
    elif type(error) == commands.errors.MissingRequiredArgument:
        cmdname = ctx.message.content.split()[0].lstrip(ctx.bot.command_prefix)
        command = next(filter(lambda cmd: cmdname in cmd.aliases or cmdname == cmd.name, ctx.bot.commands))
        await ctx.send(f"Syntax: `'{command.name} {command.usage}`")
    elif type(error) == commands.errors.BadArgument:
        await ctx.send(f"Wrong syntax ({str(error)}). Try using `'help command`")
    elif type(error) == commands.errors.ExpectedClosingQuoteError:
        await ctx.send("Expected a closing quote (\")")
    elif type(error) == commands.errors.UnexpectedQuoteError:
        await ctx.send("Unexpected quote mark (\") in non-quoted argument")
    else:
        error_str = "\n".join(traceback.format_exception(type(error), error, error.__traceback__))
        timenow = datetime.datetime.now()
        errorcode = f"{timenow.year}{timenow.month:02}{timenow.day:02}{timenow.hour:02}{timenow.minute:02}{timenow.second:02}"
        errorcode = format(int(errorcode), "X")
        await ctx.send(
            "There was an unknown error! Please send the following error code to aleok: `{}`".format(errorcode))
        try:
            owner = ctx.bot.get_user(ctx.bot.owner_id)
            if owner is None:
                await ctx.send(f"Error `{errorcode}`:```python\n{error_str[:1700]}```")
            else:
                await owner.send(f"Error `{errorcode}`:```python\n{error_str[:1700]}```")
        except Exception as e:
            await ctx.send(f"Error IN sending error, yay! (internal cmderr error: {e})")
            print(error_str)



def setup(bot, **kwargs):
    bot.on_command_error = oncmderror

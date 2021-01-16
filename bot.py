import sys
import traceback
import discord
import os
import argparse
import random
import datetime
from discord.ext import commands
from discord.ext.commands.errors import ExtensionNotFound
import getpass

print("Discord.py version: " + discord.__version__)

# Argument parsing #
parser = argparse.ArgumentParser(description="Styleventer, the discord bot!")
parser.add_argument("-msg", "--message", type=str, nargs=2, metavar=("CHANNEL", "MESSAGE"), dest="message",
                    help="Sets a message that the bot will communicate through one channel on startup.")
parser.add_argument("--debug", action="store_true", default=False,
                    help="Makes the bot initialize as styldeventer instead of styleventer.")
parser.add_argument("-p", "--presence", dest="presence",
                    help="Changes the presence (Game being played) of the bot. Default is 'help or \"help, depending "
                         "on whether or not --debug is being used.")
parser.add_argument("-t", "--presence-type", dest="presence_type", type=str, metavar="ACTIVITY_TYPE",
                    choices=[i.name.lower() for i in discord.ActivityType], default="streaming",
                    help="Sets the presence activity type of the bot. For example, can be 'playing', 'streaming', etc. "
                         "Default is 'streaming'.")
parser.add_argument("-s", "--status", dest="status", type=str, metavar="STATUS_TYPE",
                    choices=[i.name.lower() for i in discord.Status], default="online",
                    help="Sets the member status of the bot. Can be, for example, 'idle'. Default is 'online'.")
parser.add_argument("-P", "--prefix", dest="prefix", type=str, metavar="PREFIX",
                    help="Overrides the command prefix of the bot. Default is ' or \", depending on whether --debug is "
                         "used or not.")
parser.add_argument("-u", dest="force_current_user", action="store_true", default=False,
                    help="Allows the execution of the bot by this current user. This is normally not allowed since some"
                         " aspects of the bot require root permissions.")
parsed_args = parser.parse_args(sys.argv[1:])

if (not parsed_args.force_current_user) and getpass.getuser() != "root":
    print(f"User running script is '{getpass.getuser()}'. This is not valid, please use the local root user or the -u "
          "parameter to skip this check.")
    sys.exit()

# Variables #
localPath = os.path.dirname(os.path.realpath(__file__))
debugmsgs = ""
print("Local path: " + localPath)

# Add libs folder to path #
if localPath not in sys.path:
    print("Styleventer path is not in sys.path, updating...")
    sys.path.append(localPath)

print("Using debug.log from now on.")
import libs.debug as debug

debug.log("Testing,", "testing...")
debug.log("Importing assets.py...")
import libs.assets as assets


class ModuleInfo:
    def __init__(self, filename, modname, cmds, state):
        self.filename = filename
        self.name = modname
        self.commands = cmds
        self.state = state


# Token and bot loading #
if parsed_args.debug:
    # Stylusventer
    bot = commands.Bot(command_prefix='"' if parsed_args.prefix is None else parsed_args.prefix,
                       description="how are you seeing this????")
    tokenf = open(assets.get("tokend"), "r")
    token = tokenf.read()
    tokenf.close()
else:
    # Styleventer
    bot = commands.Bot(command_prefix="'" if parsed_args.prefix is None else parsed_args.prefix, description="how are "
                                                                                                             "you seeing this????")
    tokenf = open(assets.get("token"), "r")
    token = tokenf.read()
    tokenf.close()

# Module loading #
debug.log("Loading modules...")
bot.moduleInfos = []
if __name__ == "__main__":
    for fname in [f for f in os.listdir(os.path.join(localPath, "modules")) if
                  os.path.isfile(os.path.join(localPath, "modules", f))]:
        if fname.endswith("__init__.py"):
            continue
        modulename = "modules." + fname.replace(".py", "")
        try:
            debug.log(f">> {modulename}")
            cmdsBefore = bot.commands
            bot.load_extension(modulename)
            cmdsAfter = bot.commands
            cmdsImported = list(filter(lambda cmd: cmd not in cmdsBefore, cmdsAfter))
            bot.moduleInfos.append(
                ModuleInfo(filename=fname, modname=modulename, cmds=cmdsImported, state="Loaded"))
        except ExtensionNotFound as e:
            debug.log("Error loading {}: {}".format(modulename, str(e.__cause__)))
            bot.moduleInfos.append(
                ModuleInfo(filename=fname, modname=modulename, cmds="<error>", state="Load Error"))
            debugmsgs += str(e.__cause__) + "\n\n"
        except Exception as e:
            debug.log("Error loading {}: {}".format(modulename, str(e)))
            debugmsgs += str(e) + "\n\n"

debug.log(bot.moduleInfos)


@bot.event
async def on_ready():
    """http://discordpy.readthedocs.io/en/rewrite/api.html#discord.on_ready"""

    # Changes the bot's Playing Status. type=1(streaming) for a standard game you could remove type and url.
    await bot.change_presence(status=discord.Status[parsed_args.status], activity=discord.Activity(
        name=bot.command_prefix + "help" if parsed_args.presence is None else parsed_args.presence,
        type=discord.ActivityType[parsed_args.presence_type],
        url='https://twitch.tv/thisisaneasteregg'))
    debug.log('Successfully logged in!')
    if parsed_args.message is not None:
        message = parsed_args.message[1]
        channel = int(parsed_args.message[0])
        await bot.get_channel(channel).send(message)


@commands.command(name="debug",
                  usage="",
                  description="Returns the module errors produced at startup, if any.")
@commands.is_owner()
async def debugcmd(ctx):
    if debugmsgs == "":
        await ctx.send("No errors! :D")
        return
    msglength = 1500
    for msg in [debugmsgs[i:i + msglength] for i in range(0, len(debugmsgs), msglength)]:
        await ctx.send("```" + msg + "```")


last_module_reloaded = None


@commands.command(name="reload",
                  usage="",
                  description="Reloads a module.")
@commands.is_owner()
async def reloadcmd(ctx, extension):
    global last_module_reloaded
    extension_to_reload = ""
    if extension == "":
        extension_to_reload = last_module_reloaded
    else:
        extension_to_reload = extension
    last_module_reloaded = extension_to_reload
    msg = await ctx.send(f"Reloading '{extension_to_reload}'...")
    try:
        bot.reload_extension(extension_to_reload)
    except ModuleNotFoundError:
        await msg.edit(content=f"Reloading '{extension_to_reload}'... Error: Module not found.")
    except:
        await msg.edit(content=f"Reloading '{extension_to_reload}'... Error loading module.")
    else:
        await msg.edit(content=f"Reloading '{extension_to_reload}'... Success.")


@commands.command(name="load",
                  usage="",
                  description="Loads a module.")
@commands.is_owner()
async def loadcmd(ctx, extension):
    bot.load_extension(extension)


epic_iteration = 0


@commands.command(name="epic", usage="", hidden=True)
async def epiccmd_easteregg(ctx):
    global epic_iteration
    await ctx.send(file=discord.File(assets.get(["epic.jpg", "epic2.jpg"][epic_iteration])))
    epic_iteration += 1
    epic_iteration %= 2


@commands.command(name="k", usage="", hidden=True)
async def kcmd_easteregg(ctx):
    await ctx.send("ok " + random.choice(["boomer", "paisano", "", "bro", "bruh"]))


bot.add_command(debugcmd)
bot.add_command(epiccmd_easteregg)
bot.add_command(kcmd_easteregg)
bot.add_command(reloadcmd)
bot.add_command(loadcmd)
# -- Main Loop --#
try:
    bot.run(token, bot=True, reconnect=True)
except Exception as e:
    error, det, tb = sys.exc_info()
    logtxt = f"\n\n{'='*50}\n{datetime.datetime.now()}\n{'='*50}\n{str(error)}\n\n{''.join(traceback.format_tb(tb))}"
    with open("log.txt", "a") as f:
        f.write(logtxt)
    debug.log("Bot couldn't load. Check log.txt for more details.")

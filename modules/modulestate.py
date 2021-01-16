import discord
from discord.ext import commands
from libs import debug

modules = None


@commands.command(name="modulestate", aliases=["modstate", "modinfo", "modstat", "modulestat"],
                  usage="", description="Checks the state of each loaded module.")
@commands.is_owner()
async def modstatecmd(ctx):
    global modules
    embed = discord.Embed(title="Modules", color=0x0b0b73)
    for mod in modules:
        modcommands = mod.commands if type(mod.commands) is str else "\n".join(map(lambda cmd: cmd.name, mod.commands))
        embed.add_field(name=f"{mod.filename}: {mod.state}", value=modcommands if modcommands != "" else "<empty>")

    await ctx.bot.get_user(ctx.bot.owner_id).send(embed=embed)
    await ctx.send("DM'd.")


def setup(_bot, **kwargs):
    global modules
    _bot.add_command(modstatecmd)
    modules = _bot.moduleInfos
    debug.log(modules)

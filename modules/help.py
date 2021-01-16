from discord.ext import commands
import discord, inspect
from libs import modutil, lang

bot = None


@commands.command(name="help",
                  usage="[command]",
                  description="Shows the available commands or information about a specific one.")
async def helpcmd(ctx, *args):
    embed = discord.Embed(title="", color=0x0b0b73)
    if len(args) == 0:
        embed.set_author(name=lang.getl(ctx.guild, "cmdHelp", "TITLE"),
                         icon_url="https://cdn.discordapp.com/avatars/461294492121694209/168015a6373496a6472bcf25eb86e717.jpg")
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/icons/{id}/{icon}.webp".format(id=ctx.guild.id, icon=ctx.guild.icon))

        normalCommands = []
        extendedCommands = []
        adminCommands = []
        for c in bot.commands:
            if not c.hidden:
                async def checkCmdChecks():
                    cmdType = ""
                    for ch in c.checks:
                        cmdType = str(ch)
                        if inspect.iscoroutinefunction(ch):
                            try:
                                if (not await ch(ctx)): return False
                            except:
                                return False
                        else:
                            if (not ch(ctx)): return False
                    if ("is_owner" in cmdType):
                        adminCommands.append(c.name)
                    elif ("extended" in cmdType):
                        extendedCommands.append(c.name)
                    else:
                        normalCommands.append(c.name)
                    return True

                await checkCmdChecks()

        if len(normalCommands) > 0:
            embed.add_field(name=lang.getl(ctx.guild, "cmdHelp", "NORMALCMDS"), value="\n".join(normalCommands),
                            inline=False)
        if len(extendedCommands) > 0:
            embed.add_field(name=lang.getl(ctx.guild, "cmdHelp", "EXTENDEDCMDS"), value="\n".join(extendedCommands),
                            inline=False)
        if len(adminCommands) > 0:
            embed.add_field(name=lang.getl(ctx.guild, "cmdHelp", "ADMINCMDS"), value="\n".join(adminCommands),
                            inline=False)

        embed.set_footer(text=lang.getl(ctx.guild, "cmdHelp", "PROTIP"))

        await ctx.send(embed=embed)
    else:
        cmd = bot.get_command(" ".join(args))
        embed.set_author(name=lang.getl(ctx.guild, "cmdHelp", "CMD_TITLE").format(args[0]),
                         icon_url="https://cdn.discordapp.com/avatars/461294492121694209/168015a6373496a6472bcf25eb86e717.jpg")
        if cmd is None:
            embed.add_field(name=lang.getl(ctx.guild, "cmdHelp", "ERROR"),
                            value=lang.getl(ctx.guild, "cmdHelp", "CMD_NOTFOUND"))
        else:
            if cmd.usage is None and cmd.description == "":
                embed.add_field(name=lang.getl(ctx.guild, "cmdHelp", "ERROR"),
                                value=lang.getl(ctx.guild, "cmdHelp", "NO_HELP"))
            else:
                embed.add_field(name=lang.getl(ctx.guild, "cmdHelp", "SYNTAX"),
                                value="{} {}".format(cmd.name, cmd.usage), inline=False)
                if len(cmd.aliases) > 0:
                    embed.add_field(name="Aliases", value=", ".join(cmd.aliases))
                embed.add_field(name=lang.getl(ctx.guild, "cmdHelp", "DESCRIPTION"),
                                value=cmd.description if cmd.description != "" else lang.getl(ctx.guild, "cmdHelp",
                                                                                              "NO_DESCRIPTION"),
                                inline=False)

        await ctx.send(embed=embed)


def setup(_bot, **kwargs):
    global bot
    bot = _bot
    bot.remove_command("help")
    bot.add_command(helpcmd)

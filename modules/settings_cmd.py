import discord, asyncio, random
from discord.ext import commands
from libs import settings

async def show_reaction_menu(ctx, title, description, values):
    embed = discord.Embed(title=title,
                          description=description + "\n" + "\n".join(
                              list(map(lambda x: f"{x['emoji']} {x['text']}", values))))
    msg = await ctx.send(embed=embed)
    for v in values:
        await msg.add_reaction(v["emoji"])

    def check(reaction, user):
        return user == ctx.message.author and str(reaction) in map(lambda x: str(x['emoji']), values)

    try:
        reaction, user = await ctx.bot.wait_for("reaction_add", timeout=60.0, check=check)
    except asyncio.TimeoutError:
        await ctx.send("Timeout!")
    else:
        for v in values:
            if str(reaction) == v["emoji"]:
                await v["func"](ctx)
                return

async def show_prefix_response_setting(ctx):
    async def change_prefix_response_val(ctx):
        await ctx.send("Send a list of channels (separated by anything).")

        def check(m):
            return m.author == ctx.message.author

        msg = await ctx.bot.wait_for('message', check=check)
        channels = msg.channel_mentions
        settings.set_local_setting(ctx.message.guild.id, "prefix_response_channels", list(map(lambda x: str(x.id), channels)))
        await ctx.send("Setting changed!")

    async def clear_prefix_response_val(ctx):
        pass

    await show_reaction_menu(ctx, "Show prefix response",
                             """This setting allows for selecting where the bot can reply with the "Command 'x was not found" response.""",
                             [{"emoji": "✅",
                               "text": "Modify the value of this setting",
                               "func": change_prefix_response_val},
                              {"emoji": "🗑️",
                               "text": "Reset this setting to default (Allow bot to reply on all channels)",
                               "func": clear_prefix_response_val}])

async def show_user_settings(ctx):
    embed = discord.Embed(title="User settings",
                          description="There are currently no user settings available.")
    await ctx.send(embed=embed)


async def show_server_settings(ctx):
    await show_reaction_menu(ctx, "Server-wide settings",
                             "React with the emoji corresponding to one of the following menus:",
                             [{"emoji": "🔊", "text": "Prefix response", "func": show_prefix_response_setting}])


@commands.command(name="settings")
async def settingscmd(ctx):
    are_server_settings_available = ctx.message.author.permissions_in(
        ctx.message.channel).administrator or await ctx.bot.is_owner(ctx.message.author)
    if are_server_settings_available:
        await show_reaction_menu(ctx, "Styleventer settings",
                                 "React with the emoji corresponding to one of the following menus:",
                                 [{"emoji": "🔧", "text": "User settings", "func": show_user_settings},
                                  {"emoji": "🛠️", "text": "Server-wide settings", "func": show_server_settings}])
    else:
        await show_user_settings(ctx)


def setup(bot):
    bot.add_command(settingscmd)

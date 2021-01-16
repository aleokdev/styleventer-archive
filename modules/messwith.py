import discord, asyncio, json, random
from discord.ext import commands
from libs import modutil, assets

nickDict = {}


@commands.command(name="messwith", usage="<user>", hidden=True,
                  description="patataofcourse's reward for winning StylPRG19. Changes the nick of somebody randomly.")
async def bruh(ctx, username):
    global nickDict
    await ctx.send("Doing the haha funny...")
    username = username.split("#")[0]
    user = None
    for member in ctx.message.guild.members:
        if member.name == username:
            user = member
    if user is None:
        await ctx.send("Couldn't find anyone with that name. (Have you inputted the name <not nick> correctly?)")
        return
    nickBefore = user.nick
    choices = nickDict["general"][:]
    if str(user.id) in nickDict.keys():
        choices.extend(nickDict[str(user.id)])
    await user.edit(nick=random.choice(choices))
    await asyncio.sleep(10)
    await user.edit(nick=nickBefore)


def setup(_bot):
    global nickDict
    _bot.add_command(bruh)
    with open(assets.get("messwith.json"), "r") as f:
        nickDict = json.loads(f.read())
    print(nickDict)

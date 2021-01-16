import discord, random, json
from discord.ext import commands
from libs import assets

words = {}

@commands.command(name="anton",
                  description="anton_everything")
async def antonCmd(ctx):
    await ctx.send(f"`anton_{random.choice(words)}`")


def setup(_bot, **kwargs):
    global words
    with open(assets.get("words_dictionary.json"), "r") as f:
            words = list(json.loads(f.read()).keys())
    _bot.add_command(antonCmd)

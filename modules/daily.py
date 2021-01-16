import discord, datetime, random, json
from discord.ext import commands
from libs import modutil, assets

latestUpdateUID = None
wordsDict = {}
wordOfTheDay = None


@commands.command(name="daily",
                  description="Gives some information depending on the current day.")
async def dailyCmd(ctx):
    global latestUpdateUID
    global wordsDict
    global wordOfTheDay
    day = datetime.datetime.now()
    dayuid = day.year * 365 + day.month * 12 + day.day
    random.seed(dayuid)
    if dayuid != latestUpdateUID:
        latestUpdateUID = dayuid
        await ctx.send("Updating data, please wait...")
        with open(assets.get("words_dictionary.json"), "r") as f:
            wordsDict = json.loads(f.read())
        wordOfTheDay = random.choice(list(wordsDict.keys()))
        wordsDict = None

    random.seed(dayuid)
    text = day.strftime("Today is %A, %d of %B %Y!")
    embed = discord.Embed(title=text, color=0x0b0b73)
    embed.add_field(name="Number of the day", value=random.randint(1, 99))
    embed.add_field(name="Word of the day", value=wordOfTheDay)
    embed.add_field(name="User of the day", value=random.choice(ctx.guild.members).name)

    await ctx.send(embed=embed)


def setup(_bot, **kwargs):
    _bot.add_command(dailyCmd)

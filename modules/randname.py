import random
from discord.ext import commands

first	=	["Hel",	"Ar",	"Al",	"At",	"Er",	"Et",	"La",	"El",	"Ivo",	"Iko",	"Yoto",	"Poco",	"Hol",	"Hil",	"Hal",	"Baz",	"Khem",	"Scy",	"De",	"Fort",	"Bu",	"Re"]
second	=	["vel",	"lan",	"neu",	"hül",	"kol",	"loc",	"boc",	"bac",	"bec",	"bic",	"buc",	"kul",	"kil",	"kel",	"in",	"port",	"vo",	"ni",	"po",	"kka",	"tard"]
third	=	["tica",	"ica",	"vica",	"lica",	"meta",	"ta",	"ca",	"he",	"be",	"pale",	"ga",	"fi",	"bo",	"ya",	"te",	"le",	"ke"]

def getRandomName():
	return random.choice(first) + random.choice(second) + (random.choice(third) if random.randint(0, 1) else "")

@commands.command(name="name",
				  usage="",
				  description="Returns a random fantasy-like name for a location.")
async def namecmd(ctx):
	await ctx.send(getRandomName())

def setup(bot, **kwargs):
	bot.add_command(namecmd)
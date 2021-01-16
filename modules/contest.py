import discord, operator, json, os.path
from discord.ext import commands
from libs import modutil

userProgress = {}

solutions = ["TFCT-8844-VabNwvcABP", "UAYO-7359-hUfJvMCss7x", "Kvrx-1219-VnUXuCllrA", "edTS-8357-LhSfKCtYNK", "SGIG-7164-ECmMRdcFve", "sIlA-8370-fMUsNOyjMf", "DONE-asjduashdhd"]

bot = None

def serializeProgress():
	with open(modutil.absolutePath + "/stylprg19.json", "w") as f:
		f.write(json.dumps(userProgress))

async def updateLeaderboard():
	serializeProgress()
	channel = bot.get_channel(611920087405821952)
	if(channel.last_message):
		await channel.last_message.delete()
	embed = discord.Embed(title="##### `StylPRG19 Leaderboard` #####", color=0xe74c3c)
	users = []
	progresses = []
	for userID, progress in sorted(userProgress.items(), key=operator.itemgetter(1)):
		users.append(bot.get_user(userID).name)
		progresses.append(str(progress) if progress < 6 else "Finished")
	embed.add_field(name="User", value="\n".join(users))
	embed.add_field(name="Score", value="\n".join(progresses))
	await channel.send(embed=embed)

@commands.command(name="flag", usage="[solution]", description="Participate in StylPRG19!", hidden=True)
async def contestCmd(ctx, *args):
	await ctx.send("StylPRG19 has ended! Thanks for your interest :)")
	return

	if ctx.message.author.id not in userProgress.keys():
		userProgress[ctx.message.author.id] = 0
		await updateLeaderboard()
	
	if len(args) == 1:
		if(args[0] == solutions[userProgress[ctx.message.author.id]]):
			userProgress[ctx.message.author.id] += 1
			await updateLeaderboard()
		else:
			await ctx.send("No, that's not it! Try again later.")
			return
	
	embed = discord.Embed(title="StylPRG Contest")
	if userProgress[ctx.message.author.id] == 0:
		embed.add_field(name="First challenge", value=
"""
Thank you for your interest!

First, I'd like to mention that the challenges include logic puzzles, programming challenges, and basically anything I came up with. Don't worry if you don't get them all correct, what is important here is the fun you'll have!

Challenges will be sent through a message, like this one. The answer to all of them is a string of 20 lower or upper-case letters, numbers and dashes like this `ABcD-1234-ABcdEFGhIJ`. The numbers and letters can change, but the dashes stay where they are (They are constant). When you find the solution (also named flag), enter it into the flag command by typing `'flag <solution>`. I HIGHLY recommend sending your solutions through DMs and not servers, since other people could benefit from your progress.

The solution of this (extremely easy) first challenge is the first letter of each paragraph, plus `8844-VabNwvcABP`.""")
		await ctx.send(embed=embed)
		
	elif userProgress[ctx.message.author.id] == 1:
		embed.add_field(name="Second challenge", value=
"""
Congratulations! Although that was terribly easy. Time to ramp up the difficulty.
From this point on, I really recommend using a scripting language to solve the challenges you'll be facing. It'll make things much easier. 
Here's your first real challenge: (Hint: `substract 1`)
`VBZP.846:.iVgKwNDtt8y`""")
		await ctx.send(embed=embed)
		
	elif userProgress[ctx.message.author.id] == 2:
		embed.add_field(name="Third challenge", value=
"""
Woah!! You did it!! Congratulations, and extra kudos if you did it manually :P
Here's your next challenge. All I've got to say is, remember the solution format. (And you'll probably need a bit of programming knowledge (or a lot of patience) to extract this one out...) Hint: `order is key`.

`$51$71$18r$14u$4-$15C$17l$62$10V$11n$19A$89$13X$2r$0K$9-$3x$1v$12U$16l`""")
		await ctx.send(embed=embed)
	
	elif userProgress[ctx.message.author.id] == 3:
		embed.add_field(name="Fourth & Fifth challenge", value=
"""
Amazing!!! However, there's a problem... I'm not going to give you any string or anything for this challenge. You'll need to find it yourself.
There are two challenges in one here, first you'll have to find *something that isn't a solution* and then *find the solution there*.
For the first challenge, here's a hint: `invite 2nd flag last seven chars`
For the second challenge, hint: `decimal is flag`.""")
		await ctx.send(embed=embed)
	
	elif userProgress[ctx.message.author.id] == 4:
		embed.add_field(name="Sixth challenge", value=
"""
You did it! I'm proud of you for getting this far, thanks for completing these challenges! :D

I must warn you however, this is the final puzzle, and it's going to be much harder than the other ones. Reverse-engineering time!""")
		with open(modutil.absolutePath + "/obfuscated.py", "rb") as f:
			await ctx.send(embed=embed, file=discord.File(f, filename="final.py"))
	elif userProgress[ctx.message.author.id] == 5:
		embed.add_field(name="Last challenge", value=
"""
""final puzzle"" not really. Patata was speedrunning through all of the problems (And this was supposed to be for until Sunday) so I had to create another one.

Good luck with this one. Hint: `brainfuck, but not really`"""
)
		with open(modutil.absolutePath + "/brainfuck.bf", "rb") as f:
			await ctx.send(embed=embed, file=discord.File(f,filename="brainfuck.bf"))
	else:
		embed.add_field(name="Congratulations!!", value=
		"""
		You did all the challenges I had to offer, and you won the contest! I hope you had fun getting the solutions, just as I had fun coding this. Thanks for everything! :D
		You'll be granted a space in `'credits` and you'll also be able to create your own command! DM me and I'll take any idea and put it in the bot. (Please stick to simple things :p)
		""")
		await ctx.send(embed=embed)
		
	
def setup(_bot):
	global bot, userProgress
	_bot.add_command(contestCmd)
	bot = _bot
	if os.path.exists(modutil.absolutePath + "/stylprg19.json"):
		jsonProgress = {}
		with open(modutil.absolutePath + "/stylprg19.json", "r") as f:
			jsonProgress = json.loads(f.read())
		for key, value in jsonProgress.items(): # Transform str keys to int
			userProgress[int(key)] = value
			
			
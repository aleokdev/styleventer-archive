import discord, random, asyncio, re
from discord.ext import commands
from discord import utils

bot = None
hasBeenTriggered = False
daknigMessagesCountdown = 0
ouijaMsg = ""
ouijaQuestion = ""

async def onMsgChecks(message):
    if message.author.id == bot.user.id:
        return
    if message.channel.id == CENSORED or message.channel.id == CENSORED: #ouija
        global ouijaMsg
        global ouijaQuestion
        msg = message.content.lstrip(bot.command_prefix)
        if ouijaQuestion != "":
            if len(msg) == 1:
                ouijaMsg += msg.upper()
            elif msg.lower() == "goodbye":
                if "_" in ouijaQuestion:
                    await message.channel.send(ouijaQuestion.replace("_", f"**{ouijaMsg}**"))
                else:
                    await message.channel.send(f"Question: Ouija, {ouijaQuestion}\nAnswer: **{ouijaMsg}**")
                ouijaMsg = ""
                ouijaQuestion = ""
            else:
                await message.delete()
        elif msg.lower().startswith("ouija"):
            pattern = re.compile(r'((o|O)(u|U)(i|I)(j|J)(a|A),? *)(.+)')
            ouijaQuestion = pattern.sub(r'\7', msg)

    if message.channel.id == CENSORED: #CENSORED
        if message.author.id == CENSORED: # CENSORED
            global daknigMessagesCountdown
            if daknigMessagesCountdown <= 0:
                await message.add_reaction(utils.get(bot.emojis, name="daknig"))
                daknigMessagesCountdown = 10
            else:
                daknigMessagesCountdown -= 1
        if message.author.id == CENSORED: # CENSORED
            if len(message.mentions) > 5: # Pinged daily reminder
                await message.channel.send("<@CENSORED> u dumb")
        return
    global hasBeenTriggered
    if message.guild == None:
        return

    #if message.channel.id == 610842783246319681:
        #if message.content != "hi":
            #if random.randint(0, 5) == 1 and not hasBeenTriggered:
                #hasBeenTriggered = True
                #await message.channel.send("""HAHA. FUNNY. Do you think you're fucking clever for breaking a chain? Who the fuck do you think you are? Like, are you kidding me? You had ONE job. ONE SINGLE JOB, you just HAD TO PUT "hi". But no, that's too complex for your tiny mind. You have to say something different, because you have a certain grade of stupidity unknown to mankind until now. Fuck you. FUCK YOU.""")
                #await asyncio.sleep(10)
                #await message.channel.send("ok not really but dont do that again")
            #else:
                #await message.delete()
        #return
    #if "fortnite" in message.content.lower():
            #	if len(list(filter(lambda role: role.name == "fortnutter", message.author.roles))) == 0:
            #		await message.channel.send("you're now in gay baby jail for saying \"fortnite\".")
    #		await message.author.add_roles(discord.Object(610832944877010944), reason="fucking said fortnite")
        #elif "<:blj:611203131207843841>" in message.content.lower():
            #	if len(list(filter(lambda role: role.name == "fortnutter", message.author.roles))) == 1:
            #		await message.channel.send("congrats, you escaped Gay Baby Jail by BLJing.")
    #		await message.author.remove_roles(discord.Object(610832944877010944), reason="ok mrs fritz im boutta head out")
    #if "nick" in message.content.lower():
            #	if random.randint(0,2) == 1:
            #		randomUser = random.choice(message.guild.members)
            #		while randomUser.name == message.author.nick or randomUser.nick == message.author.nick:
            #			randomUser = random.choice(message.guild.members)
            #		await message.channel.send("DID SOMEONE SAY NICK?!?!?!??!")
            #		nickBefore = message.author.nick
            #		await message.author.edit(nick=randomUser.nick or randomUser.name)
            #		await asyncio.sleep(10)
    #		await message.author.edit(nick=nickBefore)
    #if message.content.lower() == "haha nerd" and message.channel.id != CENSORED:
            #	if random.randint(0, 5) == 1:
#		await message.channel.send("go to #nakbot idiot")


def setup(_bot, **kwargs):
    global bot
    _bot.add_listener(onMsgChecks, "on_message")
    bot = _bot

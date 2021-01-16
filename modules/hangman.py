import os, random
from libs import modutil, lang
from discord.ext import commands
import discord
from libs import assets

# A dict containing a word for the users that have started a game. user : (str, list1, list2)
# where str -> word to guess;
# list1 -> letters right;
# list2 -> letters wrong.
hangmanGames = {}

lifeThumbnails = [
    "https://cdn.discordapp.com/attachments/332594692388683777/583741197583909070/life4.png",
    "https://cdn.discordapp.com/attachments/332594692388683777/583741195650596913/life3.png",
    "https://cdn.discordapp.com/attachments/332594692388683777/583741203904725040/life2.png",
    "https://cdn.discordapp.com/attachments/332594692388683777/583741202080464931/life1.png",
    "https://cdn.discordapp.com/attachments/332594692388683777/583741199655895218/life0.png"
]


def isGameWon(wrd: (str, list, list)):
    for letter in wrd[0]:
        if letter != " ":
            if letter not in wrd[1]: return False
    return True


def getWordAsHidden(wrd: (str, list, list)):
    print(wrd[0])
    return "".join(map(lambda x: x if (x in wrd[1] or x == "   ") else '\_ ', list(wrd[0])))


async def showGame(ctx):
    embed = discord.Embed(title=" ", color=0x1137ee)
    embed.set_author(name=lang.getl(ctx.guild, "cmdHangman", "TITLE"),
                     icon_url="https://cdn.discordapp.com/avatars/461294492121694209/168015a6373496a6472bcf25eb86e717.jpg")

    embed.set_thumbnail(url=lifeThumbnails[len(hangmanGames[ctx.author][2])])

    embed.add_field(name=lang.getl(ctx.guild, "cmdHangman", "WORD_TITLE"),
                    value=getWordAsHidden(hangmanGames[ctx.author]), inline=False)
    if len(hangmanGames[ctx.author][1]) > 0: embed.add_field(name=lang.getl(ctx.guild, "cmdHangman", "USEDLETTERS"),
                                                             value=" ".join(hangmanGames[ctx.author][1]), inline=True)
    if len(hangmanGames[ctx.author][2]) > 0: embed.add_field(name=lang.getl(ctx.guild, "cmdHangman", "FAILEDLETTERS"),
                                                             value=" ".join(hangmanGames[ctx.author][2]), inline=True)
    await ctx.send(embed=embed)


# Functions
@commands.command(name="hangman", aliases=["h"],
                  usage="[letter]",
                  description="Start a new game of hangman, or continue one by giving a letter as a parameter.")
async def hangcmd(ctx, *args):
    if ctx.author not in hangmanGames.keys():
        # Start a new game with an user. Get a random word and set it in the dict.
        hangmanGames[ctx.author] = (lang.getl(ctx.guild, "cmdHangman", "WORDS"), [], [])

        # Show the word and return
        await showGame(ctx)
        return

    if len(args) == 0:
        await showGame(ctx)

    elif len(args) == 1:
        if len(args[0]) == 1:
            # Entered a letter
            if args[0].upper() in hangmanGames[ctx.author][1]:
                await ctx.send(lang.getl(ctx.guild, "cmdHangman", "ALREADY_ENTERED_LETTER"))
                return

            if args[0].upper() in hangmanGames[ctx.author][0]:
                hangmanGames[ctx.author][1].append(args[0].upper())
            else:
                hangmanGames[ctx.author][1].append(args[0].upper())
                hangmanGames[ctx.author][2].append(args[0].upper())

            await showGame(ctx)
        else:
            # Entered the entire word to guess
            pass
    else:
        await ctx.send(lang.getl(ctx.guild, "cmdHangman", "WRONG_N_ARGS"))

    if (isGameWon(hangmanGames[ctx.author])):
        await ctx.send(lang.getl(ctx.guild, "cmdHangman", "GAME_WON").format(hangmanGames[ctx.author][0]))
        del hangmanGames[ctx.author]
        return

    if (len(hangmanGames[ctx.author][2]) > 3):
        await ctx.send(lang.getl(ctx.guild, "cmdHangman", "GAME_LOST").format(hangmanGames[ctx.author][0]))
        del hangmanGames[ctx.author]


# Init
def setup(bot, **kwargs):
    global hangmanWords
    hangmanWordsf = open(assets.get("hangmanWords.txt"), "r")
    hangmanWords = hangmanWordsf.read().split("\n")
    hangmanWordsf.close()
    bot.add_command(hangcmd)

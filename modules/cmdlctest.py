from discord.ext import commands
from libs import assets
import discord
from PIL import ImageDraw, Image, ImageFont

@commands.command("lctest", hidden=True)
async def lctest(ctx):
    exception_text = "<#CHAR#o>\"0\"o-1+?>/"
    font = ImageFont.truetype(assets.get("consola.ttf"), size=32)
    im = Image.new("RGB", font.getsize(exception_text), (60,50,50,255))
    d = ImageDraw.Draw(im)

    d.text((0,0), exception_text, fill=(255,255,255,255), font=font)

    im.save("temp-lctest.png", "PNG")
    await ctx.send(file=discord.File("temp-lctest.png"))

def setup(bot):
    bot.add_command(lctest)
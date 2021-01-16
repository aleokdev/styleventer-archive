from discord.ext import commands
import discord
from discord.ext.commands import Greedy
from libs import assets, modutil
import json
import random
from PIL import Image, ImageDraw, ImageFont

jsonDoc = {}

class TagsGetter:
    def __getattr__(self, name):
        shouldReturn = random.choice(jsonDoc[name])
        shouldReturn = shouldReturn.format(tags=TagsGetter())
        return shouldReturn


def get_clickbait_text(do_extra_bait = False, base_node = "basic", add_bait = True):
    shouldReturn = random.choice(jsonDoc[base_node])
    if add_bait:
        if do_extra_bait:
            bait_to_add = random.sample(jsonDoc["bait"], random.randint(1, 3))
            shouldReturn += " " + " ".join(bait_to_add)
        else:
            bait_to_add = random.choice(jsonDoc["bait"])
            shouldReturn += " " + bait_to_add

    return shouldReturn.format(tags=TagsGetter())

@commands.command(name="clickbaitimg", usage="[Attached image] [video title in quotes]",
                  description="Creates an image for a clickbaity youtube video!"
                              " My favourite command.\n\n"
                              "If the video title is not specified, one will be generated"
                              " automatically. You can also use your own thumbnail for the"
                              " video, to do so just attach the image to the message [**DO NOT put a"
                              " link, those won't get detected**]. If no thumbnail is given, a "
                              "default one is placed instead.",
                  aliases=["climg", "clickbaitify"]
                  )
async def newClickbaitCmd(ctx: discord.ext.commands.Context, video_title = None):
    img = Image.new("RGB", (862, 157), color="white")

    fnt = ImageFont.truetype(assets.get("Roboto-Regular.ttf"), 19, encoding="unic")
    subtitle_text = ImageFont.truetype(assets.get("Roboto-Regular.ttf"), 13, encoding="unic")

    d = ImageDraw.Draw(img)

    # Draw title
    if video_title is None:
        video_title = get_clickbait_text()

    if len(video_title) > 55:
        video_title = video_title[:55]+"..."
    d.text((269, 9), video_title, font=fnt, fill=(13,13,13))

    # Draw channel name
    d.text((268, 34), ctx.message.author.name, font=subtitle_text, fill=(96,96,96))

    # Draw verified icon
    verified_pos = (273 + subtitle_text.getsize(ctx.message.author.name)[0], 36)
    verified_icon = Image.open(assets.get("verified.png"))
    img.paste(verified_icon, verified_pos, mask=verified_icon)

    # Draw views & time posted
    d.text((verified_pos[0]+20, 34), "a trillion views xd • 3 femtoseconds ago", font=subtitle_text, fill=(96,96,96))

    # Draw description
    description_text = f"{get_clickbait_text(base_node='description', add_bait=False)}\n\n" \
                       f"{get_clickbait_text(base_node='desc_link', add_bait=False)}..."
    d.multiline_text((268, 54), description_text,
                     font=subtitle_text, fill=(96,96,96))

    # Draw thumbnail
    if len(ctx.message.attachments) > 0:
        await ctx.message.attachments[0].save(modutil.absolutePath+"/tempcopy.png")
        thumb = Image.open(modutil.absolutePath+"/tempcopy.png")
    else:
        thumb = Image.open(assets.get("defaultthumb.jpg"))
    thumb = thumb.resize((246, 138), resample=Image.BICUBIC)
    img.paste(thumb, box=(6, 9))

    # Draw timestamp
    timestamp = Image.open(assets.get("timestamp.png"))
    img.paste(timestamp, box=(207, 127), mask=timestamp)

    # Save & send
    img.save(modutil.absolutePath+"/temp.png")
    await ctx.send(file=discord.File(modutil.absolutePath+"/temp.png"))

@commands.command(name="clickbait", description="Generates a clickbaity youtube title. Basically a basic version of"
                                                " 'clickbaitimg.", usage="[--extra-bait]", aliases=["cl"])
async def clickbaitCmd(ctx, *args):
    await ctx.send(get_clickbait_text("--extra-bait" in args))


def setup(bot):
    global jsonDoc
    with open(assets.get("clickbait.json")) as f:
        jsonDoc = json.loads(f.read())
    bot.add_command(clickbaitCmd)
    bot.add_command(newClickbaitCmd)
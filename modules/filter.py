from PIL import ImageFilter, Image
from discord.ext import commands
from libs import modutil
from libs import assets
import discord

filters = {
    "blur": ImageFilter.BLUR,
    "contour": ImageFilter.CONTOUR,
    "detail": ImageFilter.DETAIL,
    "edge_enhance": ImageFilter.EDGE_ENHANCE,
    "edge_enhance_more": ImageFilter.EDGE_ENHANCE_MORE,
    "emboss": ImageFilter.EMBOSS,
    "find_edges": ImageFilter.FIND_EDGES,
    "sharpen": ImageFilter.SHARPEN,
    "smooth": ImageFilter.SMOOTH,
    "smooth_more": ImageFilter.SMOOTH_MORE
}


@commands.command(name="imgfilter", aliases=["imgf", "filter"],
                  usage=" ".join(f"[{i}]" for i in filters),
                  description="Filters an image given with whatever arguments you choose. Important: **Images must be"
                              " uploaded to the message, not given the link to.**")
async def imgfilterCmd(ctx, *args):
    if len(args) == 0:
        await ctx.send(
            "No arguments given! Please input some filters. Look at the available ones by executing `'help imgf`.")
        return
    if len(ctx.message.attachments) != 1:
        await ctx.send("Please send an image to edit!")
        return

    await ctx.message.attachments[0].save(modutil.absolutePath + "/tempfilter.png")
    img = Image.open(modutil.absolutePath + "/tempfilter.png")
    for arg in args:
        if type(arg) is not str:
            await ctx.send(f"Argument '{arg}' is not valid.")
            return
        if arg not in filters.keys():
            await ctx.send(f"Argument '{arg}' is not valid.")
            return

        img = img.filter(filters[arg])
    filter_result_path = assets.gettemppath() + ".png"
    img.save(filter_result_path)
    await ctx.send(file=discord.File(filter_result_path))


def setup(bot):
    bot.add_command(imgfilterCmd)

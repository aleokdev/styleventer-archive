from discord.ext import commands
import requests
from lxml import etree


@commands.command(name="gangsta", usage="<text>",
                  description="Translates a text into gangsta speech! Uses gizoogle.net.")
async def gangstify(ctx, *txt):
    text = " ".join(txt)
    if type(text) is not str:
        await ctx.send("Argument supplied must be text (inside \"quotes\")")
        return
    if len(text) == 0:
        await ctx.send("Input something to gangstify! Argument supplied must be text (inside \"quotes\")")
        return
    url = "http://www.gizoogle.net/textilizer.php"
    req = {"translatetext": text}
    html = requests.post(url=url, data=req).text
    dom = etree.HTML(html)
    result = dom.xpath("//form/text()")[1] #Second element: There are some newlines n shit around there.
    await ctx.send(result.rstrip("\r\n"))


def setup(bot):
    bot.add_command(gangstify)

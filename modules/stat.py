from discord.ext import commands
import discord
import psutil


@commands.command(name="stats",
                  usage="",
                  description="Returns some stadistics regarding the bot.")
async def memcmd(ctx: commands.Context):
    embed = discord.Embed(title="Stadistics", color=0x0b0b73)

    memory = psutil.virtual_memory()
    totalmem = memory.total >> 20
    currentmem = totalmem - (memory.available >> 20)
    percentmem = memory.percent
    embed.add_field(name="Memory Usage", value=f"{percentmem}% ({currentmem}/{totalmem}MB)")

    # sensors_temperatures is linux-exclusive
    if hasattr(psutil, "sensors_temperatures"):
        temp = psutil.sensors_temperatures()['cpu-thermal'][0].current
        embed.add_field(name="CPU Temperature", value=f"{temp}ºC")
    embed.add_field(name="Guild Count", value=str(len(ctx.bot.guilds)))
    await ctx.send(embed=embed)


# Init
def setup(bot, **kwargs):
    bot.add_command(memcmd)

import discord
from discord.ext import commands
import typing
from datetime import timedelta
import asyncio


class DatetimeConverter(commands.Converter):
    async def convert(self, ctx, arg):
        times = {"s": timedelta(seconds=1),
                 "m": timedelta(minutes=1),
                 "h": timedelta(hours=1),
                 "d": timedelta(days=1),
                 "w": timedelta(weeks=1)}

        if len(arg) < 2:
            raise commands.BadArgument("Syntax for time: <number><s|m|h|d|w>")

        number = 0
        try:
            number = int(arg[0:-1])
        except:
            raise commands.BadArgument("Syntax for time: <number><s|m|h|d|w>")

        if arg[-1] not in times:
            raise commands.BadArgument("Syntax for time: <number><s|m|h|d|w>")

        return times[arg[-1]] * number


@commands.command(name="remindme", aliases=["r"], usage="<number><s|m|h|d|w>... [reminder]",
                  description="Reminds you to do something in a specific amount of time.")
async def remindcmd(ctx, time_first: DatetimeConverter, times: commands.Greedy[DatetimeConverter], *, reminder: str):
    total_remind_time = timedelta()
    times.append(time_first)
    for time in times:
        total_remind_time += time
    await ctx.send(f"Got it. I'll remind you in {total_remind_time}.")
    await asyncio.sleep(total_remind_time.total_seconds())
    await ctx.author.send(f"Reminder: {reminder}")


def setup(bot):
    bot.add_command(remindcmd)

import discord
from discord.ext import commands
from subprocess import Popen
import os

def is_allowed(ctx):
    return ctx.author.id == 329357113480708106 or ctx.author.id == 222275966485921792

@commands.command(name="invoke")
@commands.check(is_allowed)
async def invokeCmd(ctx, to_invoke: str):
    if to_invoke is None:
        await ctx.send("Please specify what to invoke as an argument.")
        return
    if to_invoke == "patatsu":
        invocation_cmd = ['nohup', 'python3', '/share/patatsu/patatsu.py']
        await ctx.send(f"Invoking `{' '.join(invocation_cmd)}`")
        Popen(invocation_cmd, cwd='/share/patatsu/')
    elif to_invoke == "asbot":
        invocation_cmd = ['nohup', 'python3', '/share/yatg/main.py']
        await ctx.send(f"Invoking `{' '.join(invocation_cmd)}`")
        Popen(invocation_cmd, cwd='/share/yatg/')
    else:
        invocation_cmd = to_invoke.split()
        await ctx.send(f"Invoking `{' '.join(invocation_cmd)}`")
        Popen(invocation_cmd, cwd='/share/')

def setup(bot):
    bot.add_command(invokeCmd)

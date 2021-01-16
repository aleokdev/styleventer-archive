from .linecrypt import tokenizer, execute
from discord.ext import commands
import discord
import signal


def clean_input(ctx) -> (str, str):
    command = ctx.prefix + ctx.invoked_with
    basemsg = ctx.message.content.replace(command, "", 1)
    prgparts = basemsg.split("|||")
    if len(prgparts) == 0:
        return "", ""

    program = prgparts[0].strip().strip("\n").strip("`").strip("\n")
    if len(prgparts) == 1:
        return program, ""

    prginput = prgparts[1]
    return program, prginput


def timeout_handler(signum, frame):
    raise TimeoutError()

def internal_exec_program(embed, ctx):
    program, prg_input = clean_input(ctx)

    embed.add_field(name="Program", value="<empty>" if program == "" else (f"```{program}```" if "\n" in program else f"`{program}`"), inline=False)
    embed.add_field(name="Input", value="<empty>" if prg_input == "" else f"`{prg_input}`", inline=False)
    try:
        execCtx = execute.execute(program, prg_input)
        stackStr = "\n".join(f"{k}: {s}" for k, s in execCtx.all_stacks.items())
        embed.add_field(name="Output stack", value=f"`{stackStr}`", inline=False)
        embed.add_field(name="Output", value="<empty>" if execCtx.output == "" else f"```{execCtx.output}```",
                        inline=False)
    except tokenizer.TokenizationException as e:
        embed.add_field(name="Tokenization error!", value=f"Error: '{e.message}' in character {e.culprit_pc}",
                        inline=False)
    except tokenizer.ExecutionError as e:
        embed.add_field(name="Execution error!", value=f"Error: '{e.message}' in token {e.token}",
                        inline=False)

    return embed

@commands.command(name="linecrypt", aliases=["lc"], usage="<program>\n<input>",
                  description="Verifies and interprets a Linecrypt program, a "
                              "self-made language. Docs:\n"
                              "https://docs.google.com/document/d/1lT0dyjJ8pQ"
                              "-Ewbnxw4wvx1njFK7sZXtniU32sXbqgb4/edit?usp=sharing")
async def execute_program(ctx):
    embed = discord.Embed(title="Linecrypt program")
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(2)
    try:
        embed = internal_exec_program(embed, ctx)
        signal.alarm(0)
        await ctx.send(embed=embed)
    except TimeoutError:
        embed.add_field(name="Timeout!", value="Your program took more than 2 seconds to run. Check for infinite loops.")
        await ctx.send(embed=embed)
    except Exception as e:
        signal.alarm(0)
        raise e


def setup(bot):
    bot.add_command(execute_program)

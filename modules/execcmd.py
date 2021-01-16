from discord.ext import commands


async def aexec(code, ctx):
    # Make an async function with the code and `exec` it
    exec(
        f'async def __ex(ctx): ' +
        ''.join(f'\n {l}' for l in code.split('\n'))
    )

    # Get `__ex` from local variables, call it and return the result
    return await locals()['__ex'](ctx)


@commands.command(name="exec",
                  usage="<args...>",
                  description="Evaluates an expression.")
@commands.is_owner()
async def execcmd(ctx):
    await aexec(ctx.message.content.replace(ctx.bot.command_prefix + "exec ", ""), ctx)


def setup(bot, **kwargs):
    bot.add_command(execcmd)

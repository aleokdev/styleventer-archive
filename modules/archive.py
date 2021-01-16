from discord.ext import commands
import discord
import html
from libs import assets

@commands.command(name="archive")
@commands.is_owner()
async def archivecmd(ctx: commands.Context):
    channels = ctx.message.channel_mentions
    for channel in channels:
        progress_msg = await ctx.send("Initializing... This will take a while.")
        # I could use the iterable async for here, but how do I check the channel message count then?
        msgs = await channel.history(limit=None).flatten()
        archive_str = f"Archiving <#{channel.id}>... ({{msg_count}} / {len(msgs)} messages read)"
        per_msg_serialization = '''{{"i":{msg.id},"c":"{content}","a":{msg.author.id}}},'''
        full_data = '''{"messages":['''
        msg_count = 0
        await progress_msg.edit(content=archive_str.format(msg_count = msg_count))
        for message in msgs:
            full_data += per_msg_serialization.format(msg = message, content = html.escape(message.content.replace('\n', '\\n')))
            msg_count += 1
            if msg_count % 100 == 0:
                await progress_msg.edit(content=archive_str.format(msg_count = msg_count))
        full_data+="]}"
        await progress_msg.edit(content="Writing file contents...")
        fpath = assets.gettemppath()
        with open(fpath, "w") as f:
            f.write(full_data)
        await progress_msg.edit(content="Done!")
        await ctx.send(f"Here's your archived data file for <#{channel.id}>:", file=discord.File(fpath, filename=f"{channel.name}.json"))


def setup(bot):
    bot.add_command(archivecmd)

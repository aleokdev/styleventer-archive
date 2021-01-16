import discord
from discord.ext import commands
import datetime

class ChannelScore:
    def __init__(self, n_messages, last_message_date: datetime.datetime, time_difference: datetime.timedelta,
                 last_conversation_length: int):
        self.n_messages = n_messages
        self.datetime_difference = time_difference
        self.last_conversation_length = last_conversation_length
        if time_difference.total_seconds() == 0:
            time_difference = datetime.timedelta(days=1)
        # Assuming 100 messages in a span of 1 day is the healthiest...
        # Assuming a channel halves its score for every day without messages...
        self.average_score = min((n_messages/100) ** 2.0, 100) * 100 * (datetime.timedelta(days=1) / time_difference) / (2.0 ** ((datetime.datetime.now() - last_message_date) / datetime.timedelta(days=1)))

async def get_score(channel: discord.TextChannel) -> ChannelScore:
    messages = []
    last_message = None
    conversation_length = 0
    # Assuming 12 hours between messages means that the conversation has ended
    async for msg in channel.history(limit=500):
        if last_message is not None:
            if last_message.created_at - msg.created_at >= datetime.timedelta(hours=12):
                break
        messages.append(msg)
        conversation_length += 1
        last_message = msg
    if len(messages) == 0:
        return ChannelScore(0, datetime.datetime.now(), datetime.timedelta(days=1), 0)

    first_message_datetime = messages[0].created_at
    last_message_datetime = messages[-1].created_at

    return ChannelScore(len(messages), last_message_datetime, first_message_datetime - last_message_datetime, conversation_length)

@commands.command(name="serverscore", aliases=["ssc"], description="Calculates the 'death score' of a server based on"
                                                                   "how dead are its chats.")
async def ssccmd(ctx):
    progress_msg = await ctx.send("Calculating based on last 500 messages of each channel...")
    scores = {}
    channels = list(filter(lambda c: c.permissions_for(ctx.me).read_message_history and c.permissions_for(ctx.me).read_messages,ctx.guild.channels))
    for i, channel in enumerate(channels):
        if type(channel) is discord.TextChannel:
            scores[channel] = await get_score(channel)
            await progress_msg.edit(content=f"Calculating based on last 500 messages of each channel... ({i+1}/{len(channels)})")

    embed = discord.Embed(title="Server score (Dead-o-meter)")

    await progress_msg.edit(content=f"Sorting and sending...")

    scores = {k: v for k, v in sorted(scores.items(), key=lambda item: item[1].average_score, reverse=True)}
    for channel, score in scores.items():
        embed.add_field(name="#"+channel.name, value=f"Average score: {score.average_score:.2f}%\nLast conversation length: {score.last_conversation_length}")

    await progress_msg.edit(content=None, embed=embed)

def setup(bot):
    bot.add_command(ssccmd)
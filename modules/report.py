from discord.ext import commands

reportFormat = "\r\n[Bug report] Made by {0.message.author.name} on {0.message.created_at}:\r\n{1}\r\n"

@commands.command(name="report",
				  usage="<description>",
				  description="Creates a bug report so it can be fixed.")
async def reportcmd(ctx, *description):
	if len(description) == 0:
		await ctx.send("Please input an error description.")
		return
	
	report = "<Failed to report>"
	try:
		report = reportFormat.format(ctx, " ".join(description))
		with open("log.txt", "a", encoding="utf-8") as f:
			f.write(report)
	except:
		await ctx.send("Error when creating bug report! WOW, this bot truly is garbage...")
	else:
		await ctx.send(f"Reported successfully! Thanks for your time! :D\nReport:```\n{report}```")
		
def setup(bot, **kwargs):
	bot.add_command(reportcmd)
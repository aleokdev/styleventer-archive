import os
from . import debug

debug.log("Initializing modutil")

absolutePath = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
debug.log("absolutePath: " + absolutePath)

extended_servers = ['293094037202665472']
semi_extended_servers = ['331718482485837825']
default_language = 'en-us'
server_languages = CENSORED

version = "1.2d"


def getServerLanguage(server):
    if str(server.id) not in server_languages:
        return default_language
    return server_languages[str(server.id)]


def check_if_extended_server(ctx):
    return str(ctx.guild.id) in extended_servers

def check_if_semi_extended_server(ctx):
    return str(ctx.guild.id) in extended_servers or str(ctx.guild.id) in semi_extended_servers

def check_if_extended_or_nsfw(ctx):
    return (str(ctx.guild.id) in extended_servers) or ctx.channel.is_nsfw()


def setup(bot, **kwargs): pass

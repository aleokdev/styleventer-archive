import os, random, discord
from libs import modutil, lang
from discord.ext import commands
import discord


class JuagStream:
    def __init__(self, string):
        self.caps_lock = False
        self.data = string

    def pop(self):
        self.data = self.data[1:]

    def peek(self):
        chr = self.data[0]
        if self.caps_lock and chr.isalpha():
            if chr.islower():
                chr = chr.upper()
            else:
                chr = chr.lower()
        return chr


keyboard = "º1234567890'¡&" \
           "&qwertyuiop`+¬" \
           "@asdfghjklñ'ç¬" \
           "~<zxcvbnm,.-~~"
shifted_keyboard = "ª!\"·$%&/()=?¿&" \
                   "&QWERTYUIOP^*¬" \
                   "@ASDFGHJKLÑ¨Ç¬" \
                   "~>ZXCVBNM;:_~~"
keyboard_width = len("º1234567890'¡&")


def caps_lock_k(stream):
    print(f"Before setting caps lock: {stream.caps_lock}")
    stream.caps_lock = not stream.caps_lock
    print(f"After setting caps lock: {stream.caps_lock}")


def shift_k(stream):
    key_index = keyboard.find(stream.peek())
    if key_index == -1:
        key_index = shifted_keyboard.find(stream.peek())
        if key_index == -1:
            return
        stream.data = keyboard[key_index] + stream.data[1:]
    else:
        stream.data = shifted_keyboard[key_index] + stream.data[1:]


def null_k(stream): pass


def enter_k(stream):
    stream.data = "\n" + stream.data


shift_key_symbol = "~"
special_keys = {
    "@": caps_lock_k,
    shift_key_symbol: shift_k,
    "&": null_k,
    "¬": enter_k
}

"""
# Functions
@commands.command(name="juagnacion", usage="[$s]")
@commands.check(modutil.check_if_extended_server)
async def juagcmd(ctx, *args):
	if len(args)==0:
		f = open(os.path.join(modutil.absolutePath, "juagnaciones.txt"), "r", encoding="utf-8")
		juagnaciones = f.read().split("\n")
		f.close()
		r = random.choice(range(len(juagnaciones)))
		
		embed=discord.Embed(title="Juagnación Aleatoria", color=0x1137ee)
		embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/317300463781543947.png?v=1')
		embed.add_field(name="Palabra", value=juagnaciones[r].split(":")[0], inline=True)
		embed.add_field(name="Definición", value=juagnaciones[r].split(":")[1:], inline=False)
		embed.set_footer(text="#{} -- Usa 'juagnacion $s para ver todas las juagnaciones".format(r))
		await ctx.send(embed=embed)
	else:
		if args[0] == "$s":
			f = open(os.path.join(modutil.absolutePath, "juagnaciones.txt"), "r")
			juagnaciones = f.read().split("\n")
			f.close()
			embed=discord.Embed(title="Juagnaciones", color=0x1137ee)
			for juagnacion in juagnaciones:
				embed.add_field(name=juagnacion.split(":")[0],value=juagnacion.split(":")[1],inline=False)
			embed.set_footer(text= lang.getl(ctx.guild, "randFun", "FUN"))
			await ctx.send(embed=embed)
"""

# The chance the algorithm has to shift the pressed key to the left or to the right. Goes from 0 to 1.
default_move_horz_chance = 0.1

# The chance the algorithm has to shift the pressed key up or down. Goes from 0 to 1.
default_move_vert_chance = 0.01

# The chance the algorithm has to reorder by one space the letters. Goes from 0 to 1.
default_reorder_chance = 0.15


def randomize(key, stream, move_horz_chance, move_vert_chance):
    key_index = keyboard.find(stream.peek())
    grab_from = keyboard
    if key_index == -1:
        key_index = shifted_keyboard.find(stream.peek())
        if key_index == -1:
            return key
        grab_from = shifted_keyboard
    if random.random() <= move_horz_chance:
        index = key_index + random.choice([-1, 1])
        if 0 < index < len(grab_from):
            return grab_from[index]
        else:
            return ""
    if random.random() <= move_vert_chance:
        index = key_index + random.choice([-1, 1]) * keyboard_width
        if 0 < index < len(grab_from):
            return grab_from[index]
        else:
            return ""
    return key


def algo(stream, move_horz_chance, move_vert_chance, reorder_chance):
    mistyped_string = ""
    while len(stream.data) > 0:
        if len(stream.data) >= 2 and random.random() <= reorder_chance:
            a = stream.peek()
            stream.data = stream.data[1] + a + stream.data[2:]
        char = stream.peek()
        char = randomize(char, stream, move_horz_chance, move_vert_chance)
        stream.pop()
        print(f"After popping: {stream.data}")

        if char in special_keys.keys():
            print(f"Special char `{char}`")
            special_keys[char](stream)
        else:
            mistyped_string += char
    return mistyped_string


@commands.command(name="jg", aliases=["tpyo"],
                  usage="<string> [--gagospeech] [--no-horz-shift] [--no-vert-shift] [--no-reorder]")
async def juagcmd(ctx, *args):
    move_horz_chance = default_move_horz_chance
    move_vert_chance = default_move_vert_chance
    reorder_chance = default_reorder_chance
    msg_skip = len(ctx.bot.command_prefix) + len(ctx.invoked_with)
    if "--gagospeech" in args:
        move_horz_chance = 1
        move_vert_chance = 1
        reorder_chance = 1
        msg_skip += len("--gagospeech ")
    if "--no-vert-shift" in args:
        move_vert_chance = 0
        msg_skip += len("--no-vert-shift ")
    if "--no-horz-shift" in args:
        move_horz_chance = 0
        msg_skip += len("--no-horz-shift ")
    if "--no-reorder" in args:
        reorder_chance = 0
        msg_skip += len("--no-reorder ")

    if msg_skip >= len(ctx.message.content):
        ctx.send("Send a string to mix up!")
        return
    raw_to_translate = ctx.message.content[msg_skip:]
    to_translate = ""
    # Parse the string first to separate caps to its base components
    for letter in raw_to_translate:
        found_index = shifted_keyboard.find(letter)
        if found_index != -1:
            to_translate += shift_key_symbol + keyboard[found_index]
        else:
            to_translate += letter

    stream = JuagStream(to_translate)
    await ctx.send(algo(stream, move_horz_chance, move_vert_chance, reorder_chance))


# Init
def setup(bot, **kwargs):
    bot.add_command(juagcmd)

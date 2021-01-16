from discord.ext import commands
from libs import modutil
import discord
import asyncio
import noise
import random
import math
from libs import assets
from PIL import Image

def parse_kwargs(args):
    kwargs = {}
    for arg in args:
        kwargs[arg.split("=")[0]] = arg.split("=")[1]
    return kwargs

# TODO: fix
@commands.command(name="map",
                  usage="[width=500] [height=500] [fade_edges=0.0] [edges_start=20] [offset=0.0] [octaves=3]"
                        "[highs=0.0] [lows=0.0] [fequency=4.0] [seed=<random>] [noise=simplex/perlin]",
                  description="Returns a randomly generated 100x100 map of an island or continent.",
                  )
@commands.cooldown(1, 15, commands.BucketType.user)
async def mapcmd(ctx, *args):
    kwargs = parse_kwargs(args)
    original_msg = await ctx.send("Loading map... This might take a few seconds.")
    width = int(kwargs.get("width", 500))
    height = int(kwargs.get("height", 500))
    if width > 500 or height > 500:
        await original_msg.edit(content="The map's width and height must be a number lower or equal to 500.")
        return
    fade_edges = float(kwargs.get("fade_edges", 0))
    edges_start = int(kwargs.get("edges_start", 20))
    offset = float(kwargs.get("offset", 0))
    octaves = int(kwargs.get("octaves", 3))
    highs = float(kwargs.get("highs", 0))
    lows = float(kwargs.get("lows", 0))
    max_value = 0
    min_value = 0
    frequency = float(kwargs.get("frequency", 4.0))
    seed = int(kwargs.get("seed", random.randint(-10000, 10000)))
    imgbytes = bytearray()
    if kwargs.get("noise", "simplex") == "perlin":
        noisefunc = noise.pnoise3
    else:
        noisefunc = noise.snoise3

    color_map = {0.06: 0x254cb0,    # Deep sea
                 0.2: 0x3c64c9,     # Sea
                 0.3: 0x5d83e3,     # Beach sea
                 0.36: 0xfaf9b6,    # Beach
                 0.52: 0x43cf3c,    # Ground
                 0.6: 0x737270,     # Mountain
                 0.9: 0xededed      # Mountain snow
                }

    for x in range(width):
        for y in range(height):
            noise_val = (noisefunc(x/width*frequency, y/height*frequency, seed, octaves=3)+1) * 5
            if x < edges_start or x > width - edges_start:
                noise_val = noise_val - (1-max(edges_start/(x+1), edges_start/(width-x+1))) * fade_edges
            if y < edges_start or y > width - edges_start:
                noise_val = noise_val - (1-max(edges_start/(y+1), edges_start/(height-y+1))) * fade_edges
            noise_val = noise_val - offset
            if noise_val > max_value:
                max_value = noise_val
            elif noise_val < min_value:
                min_value = noise_val

            mapped_noise_val = max(min(1-noise_val / 7, 1), 0.001)
            mapped_noise_val = mapped_noise_val - (math.log((1-mapped_noise_val)*10)*-lows) - (math.log(mapped_noise_val*10)*-highs)

            final_color = 0
            for max_color_val, color in color_map.items():
                final_color = color
                if max_color_val >= mapped_noise_val:
                    break

            imgbytes.extend(final_color.to_bytes(3, "big"))
        await asyncio.sleep(0)

    image = Image.frombytes("RGB", (width, height), bytes(imgbytes))
    map_path = assets.gettemppath()+".png"
    image.save(map_path)

    embed = discord.Embed(title="Map result")
    embed.add_field(name="Minimum value", value=str(min_value))
    embed.add_field(name="Maximum value", value=str(max_value))
    embed.add_field(name="Frequency", value=str(frequency))
    embed.add_field(name="Seed", value=str(seed))
    await ctx.send(embed=embed, file=discord.File(map_path))


def setup(bot, **kwargs): bot.add_command(mapcmd)

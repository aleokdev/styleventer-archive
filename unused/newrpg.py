import json, os.path
import discord, time
from discord.ext import commands

# generation.py
import noise, random
from .rpgsrc import newWorldToImg


def GetSingleNoise(x, y, seed, freq):
    return noise.snoise3(x / (500 * freq), y / (500 * freq), seed, 128)


def GetNoise(x, y, seed):
    return GetSingleNoise(x, y, seed, 15) + GetSingleNoise(x, y, seed, 5) - GetSingleNoise(x, y, seed,
                                                                                           0.5) + GetSingleNoise(x, y,
                                                                                                                 seed,
                                                                                                                 0.1)


def GetHumidityNoise(x, y, seed):
    return GetSingleNoise(x, y, seed, 7) + GetSingleNoise(x, y, seed, 2) - GetSingleNoise(x, y, seed,
                                                                                          0.2) + GetSingleNoise(x, y,
                                                                                                                seed,
                                                                                                                0.05)


seaLevel = 0.4


def GetTypeByPos(seed: int, x: int, y: int) -> str:
    height = GetNoise(x, y, seed)
    if height > seaLevel:
        if height > (seaLevel + 0.2):
            if height > (seaLevel + 0.75):
                return "mountain"
            else:
                hum = GetHumidityNoise(x, y, seed)
                return "forest" if hum > 0.7 else ("plains" if (hum > 0.3 or height < seaLevel + 0.35) else "desert")
        else:
            return "beach"
    else:
        return "ocean"


class RPGBiome:
    def __init__(self, x: int, y: int, type: str, landmass: int):
        self.x = x
        self.y = y
        self.type = type
        self.landmass = landmass

    def Serialize(self) -> str:
        return json.dumps(
            {
                "x": self.x,
                "y": self.y,
                "type": self.type,
                "landmass": self.landmass
            })


class RPGChunk:
    # Size in biomes
    size = 100

    # How chunks are named in file format
    namingFormat = "c{x}{y}"

    def __init__(self, parent, x: int, y: int):
        self.x = x
        self.y = y
        self.parent = parent
        self.biomes = []

    def TryLoadFromDir(dir: str, x: int, y: int):
        "Returns a chunk if it exists in dir given, None otherwise."
        pathToLoad = path.join(dir, namingFormat.format(str(x), str(y)))
        if path.exists(pathToLoad):
            with open(pathToLoad, "r") as f:
                rawChunkBiomes = json.loads(f.read())

            chunkToReturn = RPGChunk(x, y)
            chunkToReturn.biomes = map(lambda data: RPGBiome(data["x"], data["y"], data["type"], data["landmass"]),
                                       rawChunkBiomes)
        else:
            return None

    def Generate(self):
        for ix in range(RPGChunk.size):
            for iy in range(RPGChunk.size):
                # TODO: calculate landmass
                self.biomes.append(RPGBiome(ix + self.x * RPGChunk.size, iy + self.y * RPGChunk.size,
                                            GetTypeByPos(self.parent.seed, ix + self.x * RPGChunk.size,
                                                         iy + self.y * RPGChunk.size), 0))

    def GetAbsolute(self, x: int, y: int) -> RPGBiome:
        x -= self.x * RPGChunk.size
        y -= self.y * RPGChunk.size
        return self.biomes[x + y * RPGChunk.size]

    def GetRelative(self, x: int, y: int) -> RPGBiome:
        return self.biomes[x + y * RPGChunk.size]

    def Serialize(self) -> str:
        return json.dumps(map(lambda b: b.Serialize(), self.biomes))


class RPGLandmass:
    def __init__(self):
        self.uid = 0


class RPGWorld:
    def __init__(self):
        # The chunks this world's divided into.
        # list(Chunk)
        self.chunks = []

        # The landmasses present in the world.
        # list(Landmass)
        self.landmasses = []
        self.seed = random.randint(0, 1000000.0)

    def GetLandmassByID(self, id) -> RPGLandmass:
        return self.landmasses[id - 1]

    def AddChunk(self, chunk: RPGChunk) -> None:
        self.chunks.append(chunk)

    # Returns true only if the position specified is within the currently generated bounds of the world.
    # TODO: def IsPositionGenerated(x : int, y : int) -> bool:

    # Returns the biome of a position in the world.
    # If not generated, depending on the intrusive bool...
    # If intrusive is false: Returns None
    # If intrusive is true: Forces chunk generation
    def GetPos(x: int, y: int, intrusive: bool) -> RPGBiome:
        for c in world:
            if c.containsPos(x, y):
                return c.getPos(x, y)

        print("Doesn't exist on chunks loaded")
        c = Chunk.load(floor(x / Chunk.size), floor(y / Chunk.size))

        world.append(c)

        return c.getPos(x, y)

    def AddLandmass(l: RPGLandmass) -> None:
        landmasses.append(l)


@commands.command(name="rtest", hidden=True)
@commands.cooldown(1, 15, commands.BucketType.user)
@commands.is_owner()
async def rtestcmd(ctx, seed=None, size=1):
    size = min(10, size)
    await ctx.send(f"Creating world and creating {size}*{size} chunks...")
    start = time.time()
    world = RPGWorld()
    if seed != None:
        world.seed = int(seed)
    for iy in range(size):
        for ix in range(size):
            world.AddChunk(RPGChunk(world, ix, iy))
    await ctx.send("Took {:.3f} seconds.".format(time.time() - start))
    await ctx.send("Generating chunks...")
    start = time.time()
    for chunk in world.chunks:
        chunk.Generate()
    await ctx.send("Took {:.3f} seconds.".format(time.time() - start))
    await ctx.send("Creating image...")
    start = time.time()
    newWorldToImg.represent(world.chunks[0], "result.png")
    await ctx.send("Took {:.3f} seconds.".format(time.time() - start))
    await ctx.send("Uploading...")
    with open("result.png", "rb") as f:
        await ctx.send(file=discord.File(f))


def setup(bot, **kwargs):
    return

    bot.add_command(rtestcmd)

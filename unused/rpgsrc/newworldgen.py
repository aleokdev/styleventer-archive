from modules.rpgsrc import worldToImage
from libs import modutil
import random, sys
from noise import pnoise3, snoise3
from math import floor, log
from operator import attrgetter

seed = 0


def generateNewSeed():
    global seed
    seed = random.randint(-10000.0, 10000.0)
    print("Generated seed " + str(seed))


if len(sys.argv) > 2:
    offset = float(sys.argv[2])
else:
    offset = 0.4
print("World seed: " + str(seed))
print("Perlin offset: " + str(offset))
seaLevel = 0.4


class PieceType:
    WATER = 1
    LAND = 2
    BEACH = 3
    MOUNTAIN = 4
    FOREST = 5
    DESERT = 6
    RIVER = 7


class Piece:
    conversionEmoji = {PieceType.WATER: "🌊", PieceType.LAND: "🏞", PieceType.BEACH: "🏖", PieceType.MOUNTAIN: "🏔",
                       PieceType.FOREST: "🌲", PieceType.DESERT: "🏜", PieceType.RIVER: "🛶"}
    conversionType = {PieceType.WATER: "OCEAN", PieceType.LAND: "PLAINS", PieceType.BEACH: "BEACH",
                      PieceType.MOUNTAIN: "MOUNTAIN", PieceType.FOREST: "FOREST", PieceType.DESERT: "DESERT",
                      PieceType.RIVER: "RIVER"}

    def startRiver(self):
        neighbours = []
        for ix in [self.x - 1, self.x, self.x + 1]:
            for iy in [self.y - 1, self.y, self.y + 1]:
                if isValid(ix, iy):
                    neighbours.append(getPiece(ix, iy))

        if max(neighbours, key=attrgetter('height')) == self:
            self.continueRiver()  # Start river if is highest point

    def continueRiver(self):
        if self.type == PieceType.WATER or self.type == PieceType.RIVER:
            return

        self.type = PieceType.RIVER

        neighbours = []
        for ix in [self.x - 1, self.x, self.x + 1]:
            for iy in [self.y - 1, self.y, self.y + 1]:
                if isValid(ix, iy):
                    neighbours.append(getPiece(ix, iy))

        minN = min(neighbours, key=attrgetter('height'))

        if minN == self:
            self.type = PieceType.WATER
        else:
            minN.continueRiver()

    def setHeight(self, _h):
        if _h > seaLevel:
            if _h > (seaLevel + 0.2):
                if _h > (seaLevel + 0.75):
                    self.type = PieceType.MOUNTAIN
                else:
                    hum = getHumidityNoise(self.x, self.y)
                    self.type = PieceType.FOREST if hum > 0.7 else (
                        PieceType.LAND if (hum > 0.3 or self.height < seaLevel + 0.35) else PieceType.DESERT)
            else:
                self.type = PieceType.BEACH
        else:
            self.type = PieceType.WATER

    def __init__(self, x, y, _t, _h):
        self.height = _h
        self.x = x
        self.y = y
        self.setHeight(_h)

    def getEmoji(self):
        return Piece.conversionEmoji[self.type]


pworld = []
pworldSize = 500
octaves = 128


def createWorld():
    for i in range(pworldSize * pworldSize):
        pworld.append(Piece(i % pworldSize, floor(i / pworldSize), PieceType.WATER,
                            getNoise(i % pworldSize, floor(i / pworldSize))))


def createRivers():
    for p in pworld:
        if p.height > (seaLevel + 1) and getRiverNoise(p.x, p.y) > 0.7:
            p.startRiver()


def getPiece(x, y):
    return pworld[x + y * pworldSize]


def isValid(x, y):
    return x >= 0 and y >= 0 and x < pworldSize and y < pworldSize


def getAxisBorderRemoval(x, m=5):
    return max(m / (x + 1), m / (pworldSize - x + 1))


def getBorderRemoval(x, y):
    return getAxisBorderRemoval(x) + getAxisBorderRemoval(y)


def getSingleNoise(x, y, freq):
    return snoise3(x / (pworldSize * freq), y / (pworldSize * freq), seed, octaves)


def getNoise(x, y):
    return getSingleNoise(x, y, 15) + getSingleNoise(x, y, 5) - getSingleNoise(x, y, 0.5) + getSingleNoise(x, y,
                                                                                                           0.1) - getBorderRemoval(
        x, y) + offset


def getHumidityNoise(x, y):
    return getSingleNoise(x, y, 7) + getSingleNoise(x, y, 2) - getSingleNoise(x, y, 0.2) + getSingleNoise(x, y,
                                                                                                          0.05) - getBorderRemoval(
        x, y) + offset


def getRiverNoise(x, y):
    return getSingleNoise(x, y, 0.0001) + 1


def main(transferToWorld, filename="map.png", save=False, worldseed=None):
    global seed
    print("Creating base world... This might take a few minutes.")
    if worldseed == None:
        generateNewSeed()
    else:
        print("setting seed manually")
        seed = worldseed
    print("seed = " + str(seed))
    createWorld()

    # print("Creating rivers...")
    # createRivers()				# They look awful!! :(

    worldmap = ""
    print("Transforming world to string...")
    for iy in range(pworldSize):
        for ix in range(pworldSize):
            worldmap += getPiece(ix, iy).getEmoji()
        worldmap += "\n"

    worldmap.rstrip("\n")

    print("Transforming string to image...")
    worldToImage.represent(worldmap, modutil.absolutePath + "/" + filename, cellSize=1)

    if not transferToWorld: return

    print("Importing world modules...")
    from modules.rpgsrc import world, worldgen

    print("Importing datatype modules...")
    from modules.rpgsrc import datatypes, typeloader

    print("Loading datatypes...")
    typeloader.loadAll()

    print("Clearing world...")
    worldgen.clearWorld()

    print("Transferring pworld to world...")
    for p in pworld:
        world.getPos(p.x, p.y).stype = Piece.conversionType[p.type]
        world.getPos(p.x, p.y).x = p.x
        world.getPos(p.x, p.y).y = p.y

    print("Checking if successful...")
    if world.getPos(0, 0).stype != None:
        print("Was successful!")
    else:
        raise Exception("Something didn't work!")
    print("Saving world...")
    world.save()

    print("Finished!")


if __name__ == "__main__": main(True, save=True)

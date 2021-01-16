# ------------------------- world.py -------------------------
# Here are some notes:
# In the next version, there will be a major overhaul
# done to the world system. Biomes will be divided in 100x100
# chunks, and loading will be done dynamically.
# To store the world, a new folder will be made to store it
# (server-bot/world/chunks). Each chunk will have its own file,
# to prevent various players loading the same file at the same time.

# New world will be composed out of 25x25 of these chunks, effectively
# making the world 2500 x 2500 biomes wide/tall.

from tqdm import tqdm, trange
from .datatypes import Chunk, LandMass, Biome
import random, os
from math import floor
from libs import modutil


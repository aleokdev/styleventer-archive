from modules.rpgsrc import world, typeloader, worldgen
import sys

if len(sys.argv) == 1:
	print("Usage: python3 worldgen.py [-w] [-l]")
	print("-w will generate an entire world and replace the current one.")
	print("-l will generate and replace the loot of the current world.")
else:
	typeloader.loadAll()

	if "-w" in sys.argv:
		print("Resetting world.")
		worldgen.generateWorld()
		
	if "-l" in sys.argv:
		print("Resetting loot.")
		worldgen.generateLoot()
	
	print("Saving world.")
	world.save()
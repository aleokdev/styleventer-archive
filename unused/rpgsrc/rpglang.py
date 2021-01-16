# ------------------------------ rpglang.py ------------------------------
# Module that defines a single function (getl) that is used for getting
# an usable string from a "key". These keys and strings are defined in
# a file called rpgLang.txt, that connects every key to an usable string.
#
# There are two types of keys: choice and single keys.
# Single keys may contain text of one of more lines, while
# choice keys contain several lines, of which only one will be returned.
#
# aleok (c) 2019

from libs import modutil
import os, random

languagePath = "lang/en-us"

# Function that gets a string from the rpgLang file found in languagePath.
def getl(key):
	# Open rpgLang file found at languagePath
	f = open(os.path.join(modutil.absolutePath, languagePath, "rpgLang.txt"), "r", encoding="utf-8")
	
	chunk = f.readline()						# Get every "chunk" (line) of the file, and parse it...
	while chunk != "":							# Stop if the chunk is blank (That means eof!)
		if chunk == ("#" + key + "\n"):			# Check if the chunk is the key given (as a "single key").
			chunk = f.readline()				# If yes, proceed to get all data proceeding to the declaration and return that.
			total = ""
			while chunk != "":
				if chunk[0] == "#" or chunk[0] == "¬":
					break
				total = total + chunk
				chunk = f.readline()
			f.close()
			return total.rstrip("\n")
		
		if chunk == ("¬" + key + "\n"):			# Check if the chunk is the key given (as a "choice key").
			chunk = f.readline()
			choices = []						# Get all possible return values.
			while chunk != "":
				if chunk[0] == "#" or chunk[0] == "¬":
					break
				if chunk!="\n":
					choices.append(chunk.rstrip("\n"))
				chunk = f.readline()
			f.close()
			return random.choice(choices)		# Then return a random one.
			
		
		chunk = f.readline()					# If the key is not detected in this line, go to the next.
		
	return "#" + key							# If the key is not detected at all, return a placeholder text.
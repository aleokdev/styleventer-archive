import png

pal = {
"🏞":"2",
"🌲":"1",
"🏔":"4",
"🏜":"3",
"🎑":"5",
"X":"6",
"🌊":"7",
"🏖":"8",
"🛶":"9",
"C":"10",
}

def represent(inp, path, cellSize=8):
	# Scale the string depending on cellSize
	scaled = ""
	for x in inp.split("\n"):
		# Go line by line multiplying the input string by cellSize.
		line = ""
		for char in x:
			line += char * cellSize
		scaled += (line+ "\n") * cellSize
		
	# Remove last, empty line
	scaled = scaled.rstrip("\n")
	
	# Here comes the magic. We need to turn this to a bidimensional array of palette indexes.
	# This converts each emoji present in scaled to its equivalent in the variable <pal>.
	s = list(map(lambda l: "".join(list(map(lambda ch: pal[ch] ,l))),scaled.split("\n")))
	
	# Convert the strings into arrays of integers.
	s = list(map(lambda x: list(map(int, x)), s))
	
	# Define the palette.
	palette = [(0x00,0x00,0x00),(0x22,0xb1,0x4c),(0xb5,0xe6,0x1d),(0xef,0xe4,0xb0),(0xc3,0xc3,0xc3),(0xb9,0x7a,0x57),(0xff,0x0,0x0), (0x00, 0xa2, 0xe8), (0xff,0xff,0x80), (0x99,0xd9,0xea), (0x50, 0x0, 0x70)]
	# Set the writer and write the data.
	writer = png.Writer(len(s[0]), len(s), palette=palette, bitdepth=8)
	file = open(path, 'wb')
	writer.write(file, s)
	file.close()

def representCustom(s, path, palette):	
	# Set the writer and write the data.
	writer = png.Writer(len(s[0]), len(s), palette=palette, bitdepth=8)
	file = open(path, 'wb')
	writer.write(file, s)
	file.close()
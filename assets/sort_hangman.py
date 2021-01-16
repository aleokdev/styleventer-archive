file = open("hangmanWords.txt", "r")
words = file.read().split("\n")
words.sort()
file.close()

file = open("hangmanWords.txt", "w")
file.write('\n'.join(words))
file.close()

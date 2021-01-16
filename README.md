# Styleventer
This a repository containing the entire codebase for Styleventer, the Discord bot,
including but not limited to:
- All the commands it offered
- All the easter eggs it had
- All the unused commands and experiments that never made it into the bot (inside the `unused/` folder)
- The original [Linecrypt](https://github.com/alexdevteam/lcc) interpreter
- All the assets it used (With some exceptions, keep reading)

The codebase's original structure has been kept intact, but some documents (cache and sensitive data)
have been excluded from the repository. As such, in its current state, this project **will not run**,
since data such as the bot token or certain hardcoded values have been removed.

## Okay, but what is this?
Styleventer is a Discord bot created around 2018 that started as a project to make some kind of automated
system to be able to change the names & descriptions of channels according to which day it was (thus the name
Style-event -> Styleventer). While trying to finish the functionality, I became interested in some other ideas
and ended up adding them to the bot as well. Since the bot was meant for a single friends server, I almost
never polished it, which is why every single command in it has a 50% chance of either throwing an error or
exploding the Raspberry Pi it was hosted on.

The reason the style-change functionality is gone from the codebase, I'm not sure about. I believe I ended up
either removing it completely, or moving it to the precursor of this bot (which is not present in this repo).

## About the code itself
It's horrible. As I mentioned earlier, this was _never_ meant to be a public bot, so I had very little reason
to refactor the code in it, even though I thought of rewriting the entire thing in C# and even in C++ (See
[Dualventer](https://github.com/alexdevteam/dualventer))

The reason I am putting the code public is to shame myself publicly and to allow those interested to scrap
for modules or parts.

## Any interesting stuff?
This is like dumpster diving, you might find something mildly interesting you may like. As such, feel free to
look around in the code. Beware: There will be a lot of garbage and stuff to cringe about.

Since I want this to be like ~dumpster diving~ an easter egg hunt, I won't share any information about where my favourite parts
of it are.

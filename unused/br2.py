from discord.ext import commands
import discord
from libs import assets
import json
import random

brData = None


class BRPlayer:
    def __init__(self, user: discord.Member):
        self.member = user
        self.is_dead = False
        self.weapon = None

    def __str__(self):
        return self.member.name

    def get_attack_text(self):
        if self.weapon is None:
            attacks_text = "attacks"
        else:
            if "attack_text" not in self.weapon:
                attacks_text = "attacks" if self.weapon["type"] == "melee" else "shoots"
            else:
                attacks_text = self.weapon["attack_text"]
        return attacks_text


class BRGame:
    def __init__(self):
        self.players = []
        self.dead_last_round = []

    @property
    def alive_players(self):
        return list(filter(lambda player: not player.is_dead, self.players))

    def check_for_results(self, situation, players_involved):
        if "result" in situation:
            if "dead" in situation["result"]:
                for dead_player in situation["result"]["dead"]:
                    players_involved[dead_player].is_dead = True
                    self.dead_last_round.append(players_involved[dead_player])
            if "get" in situation["result"]:
                players_involved[0].weapon = random.choice(brData["weapons"])

    def execute_situation(self, situation, players, execute_causes: bool) -> str:
        n_of_players_involved = situation["people_involved"]
        if n_of_players_involved > len(players) + 1:
            return ""
        players_involved = players[:n_of_players_involved]
        if "requires" in situation and "weapon" in situation["requires"]:
            if players_involved[0].weapon is None:
                return ""
            # TODO: require type, etc
            # require = situation["requires"]["weapon"]
            # elif players_involved.weapon
        del players[:situation["people_involved"]]

        text_to_return = situation["text"].format(people=players_involved, attacks=players_involved[0].get_attack_text())
        text_to_return += "\n"

        if execute_causes and "causes" in situation:
            causes_tags = situation["causes"]
            # text_to_return += f"!!{causes_tags}!!"
            situation_caused = random.choice(list(filter(lambda s: "tags" in s and len(set(s["tags"]).intersection(set(causes_tags))) > 0,
                                 brData["situations"])))
            if situation_caused is None:
                raise Exception(f"Could not find situation with tag {causes_tags}")
            if "text" not in situation_caused:
                raise Exception(f"Text doesn't exist in situation {situation_caused}")
            # Make people in situation caused be reversed so that the first player is the one that was told the joke (or done the action to)
            people_in_situation_caused = players_involved[:]
            people_in_situation_caused.reverse()
            # Add the rest of the players involved to fill up situation spaces and to allow others to join in
            people_in_situation_caused.extend(filter(lambda p: p not in people_in_situation_caused, players))

            text_to_return += situation_caused["text"].format(people=people_in_situation_caused, attacks=people_in_situation_caused[0].get_attack_text())
            text_to_return += "\n"
            self.check_for_results(situation_caused, people_in_situation_caused)

        self.check_for_results(situation, players_involved)

        text_to_return += "\n"
        return text_to_return

    def next_round(self) -> str:
        text_to_return = ""
        self.dead_last_round = []

        players_to_take_action = self.alive_players
        random.shuffle(players_to_take_action)
        while len(players_to_take_action) > 1:
            possible_situations = list(filter(lambda s: "tags" in s and "basic" in s["tags"], brData["situations"]))
            text_to_return += self.execute_situation(random.choice(possible_situations), players_to_take_action, True)

        return text_to_return


def defaultIfEmpty(string, default):
    if string == "":
        return default
    return string

@commands.command(name="battle", hidden=True)
async def SimpleBRCmd(ctx: discord.ext.commands.Context):
    lobby = []
    for m in ctx.guild.members:
        if not m.bot:
            lobby.append(BRPlayer(m))
    game = BRGame()
    game.players = lobby

    await ctx.send(",".join(str(p) for p in game.players))
    while len(game.alive_players) > 1:
        embed = discord.Embed(title="Epic Battle Royale", footer="F to pay respects")
        embed.add_field(name="Round", value=game.next_round(), inline=False)
        embed.add_field(name="People still alive", value=defaultIfEmpty(", ".join(str(p) for p in game.alive_players), "None"))
        embed.add_field(name="Dead this round", value=defaultIfEmpty(", ".join(str(p) for p in game.dead_last_round), "None"))
        await ctx.send(embed=embed)
    await ctx.send(f":tada: {game.alive_players[0]} has won the battle royale!! :tada:")



def setup(bot):
    global brData
    with open(assets.get("simplebr.json")) as f:
        brData = json.loads(f.read())
    bot.add_command(SimpleBRCmd)
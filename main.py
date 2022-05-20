import discord
from discord.ext import commands, tasks
import os
import random
from datetime import datetime
import requests
import youtube_dl
from os import path
import json
import time
import urllib.request
from bs4 import BeautifulSoup as BS

SERVER_ID = 564004879417212928
TEST_VOICE_CHANNEL = 564004879417212932
TEST_TEXT_CHANNEL = 564004879417212930
FLAVOR_TOWN_VOICE = 438791959444717568
THE_FIERI_LAIR_TEXT = 698323553493188640
POKEMON_TEXT_CHANNEL = 848755220292436009
POKEDEX_TEXT_CHANNEL = 851262216292007938

api_key = "3f9e50e00f2c68a7c68a87b870d15575"
base_url = "http://api.openweathermap.org/data/2.5/weather?"

APEX_KEY = "mkK7MnR0WXkeUP3TYDkd"

cooldown = 0


# get the bot token
def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()


token = read_token()
# client = discord.Client()
# set the bot command to '!' before every command
client = commands.Bot(command_prefix='!')


@client.command(brief='test command.')
async def test(ctx):
    with open("names.json", "r", encoding="utf8") as jsonFile:
        names = json.load(jsonFile)

    for player in names["players"]:
        player["items"]["masterball"] += 1

    # save it to the json file
    with open("names.json", "w") as jsonFile:
        json.dump(names, jsonFile)


@client.command()
async def mypokemon(ctx):
    # display the current users party pokemon
    with open("names.json", "r", encoding="utf8") as jsonFile:
        names = json.load(jsonFile)

    for player in names["players"]:
        if player["name"] == ctx.message.author.nick or player["name"] == ctx.message.author.name:
            if len(player["party"]) == 0:
                embed = discord.Embed(title="You don't have any pokemon . . . :'c ")
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)

            else:
                embed = discord.Embed(
                    title=ctx.message.author.name + "'s Pokemon! \n1. " + player["party"][0]["name"].capitalize(),
                    color=0xa832a4)
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                embed.set_thumbnail(url=player["party"][0]["icon"])
                await ctx.channel.send(embed=embed)
                i = 1
                index = 0
                for pokemon in player["party"]:
                    if i != 1:
                        embed = discord.Embed(
                            title=str(i) + ". " + pokemon[
                                "name"].capitalize(),
                            color=0xa832a4)
                        embed.set_thumbnail(url=pokemon["icon"])
                        await ctx.channel.send(embed=embed)
                    i += 1
                    index += 1

                embed = discord.Embed(
                    title="NUMBER OF POKEMON IN BOX: " + str(len(player["box"])),
                    color=0xa832a4)
                await ctx.channel.send(embed=embed)


@client.command()
async def deposit(ctx, pokemon: str):
    # display the current users party pokemon
    with open("names.json", "r", encoding="utf8") as jsonFile:
        names = json.load(jsonFile)

    for player in names["players"]:
        if player["name"] == ctx.message.author.nick or player["name"] == ctx.message.author.name:
            none = 0
            for party_member in player["party"]:
                if party_member["name"] == pokemon.lower():
                    embed = discord.Embed(title=pokemon.upper() + " HAS BEEN SENT TO THE BOX!")
                    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                    embed.set_thumbnail(url=party_member["icon"])
                    await ctx.channel.send(embed=embed)
                    player["box"].append(party_member)
                    player["party"].remove(party_member)
                    # save it to the json file
                    with open("names.json", "w") as jsonFile:
                        json.dump(names, jsonFile)
                    return
                else:
                    none += 1
                    if none == len(player["party"]):
                        embed = discord.Embed(title=pokemon.upper() + " WAS NOT FOUND!")
                        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                        await ctx.channel.send(embed=embed)


@client.command()
async def withdraw(ctx, pokemon: str):
    # display the current users party pokemon
    with open("names.json", "r", encoding="utf8") as jsonFile:
        names = json.load(jsonFile)

    for player in names["players"]:
        if player["name"] == ctx.message.author.nick or player["name"] == ctx.message.author.name:
            if len(player["party"]) == 6:
                embed = discord.Embed(title="YOUR PARTY IS FULL!")
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                await ctx.channel.send(embed=embed)
                return
            for box_pokemon in player["box"]:
                if box_pokemon["name"] == pokemon:
                    player["party"].append(box_pokemon)
                    player["box"].remove(box_pokemon)
                    embed = discord.Embed(title=pokemon.upper() + " HAS BEEN WITHDRAWN FROM THE BOX!")
                    embed.set_thumbnail(url=box_pokemon["icon"])
                    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                    await ctx.channel.send(embed=embed)
                    # save it to the json file
                    with open("names.json", "w") as jsonFile:
                        json.dump(names, jsonFile)
                    return


@client.command()
async def gift(ctx, other_player_name: str, emoji: str, pokemon: str):
    with open("names.json", "r", encoding="utf8") as jsonFile:
        names = json.load(jsonFile)

    for player in names["players"]:
        if player["name"] == ctx.message.author.nick or player["name"] == ctx.message.author.name:
            for other_player in names["players"]:
                if other_player["name"].startswith(other_player_name[:3]):

                    for party_pokemon in player["party"]:
                        if party_pokemon["name"] == pokemon.lower():
                            other_player["box"].append(party_pokemon)
                            player["party"].remove(party_pokemon)
                            embed = discord.Embed(
                                title=ctx.message.author.name + " gave " + other_player_name + " a " + pokemon.upper() + "!")
                            embed.set_thumbnail(url=party_pokemon["icon"])
                            await ctx.send(embed=embed)
                            with open("names.json", "w") as jsonFile:
                                json.dump(names, jsonFile)
                            return

                    for box_pokemon in player["box"]:
                        if box_pokemon["name"] == pokemon.lower():
                            other_player["box"].append(box_pokemon)
                            player["box"].remove(box_pokemon)
                            embed = discord.Embed(
                                title=ctx.message.author.name + " gave " + other_player_name + " a " + pokemon.upper() + "!")
                            embed.set_thumbnail(url=box_pokemon["icon"])
                            await ctx.send(embed=embed)
                            with open("names.json", "w") as jsonFile:
                                json.dump(names, jsonFile)
                            return


@client.command()
async def tradecheck(ctx, check: str):
    # display the current users party pokemon
    with open("names.json", "r", encoding="utf8") as jsonFile:
        names = json.load(jsonFile)

    for player in names["players"]:
        if player["name"] == ctx.message.author.nick or player["name"] == ctx.message.author.name:
            if check == "yes":
                embed = discord.Embed(
                    title="YOU HAVE SET YOUR TRADE CHECK TO 'YES'!\n\nWARNING: MAKE SURE THE OTHER PARTY IS READY FOR TRADE!")
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                await ctx.channel.send(embed=embed)
                player["trade-pokemon"]["trade-check"] = "yes"
            elif check == "no":
                embed = discord.Embed(
                    title="YOU HAVE SET YOUR TRADE CHECK TO 'NO'!")
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                await ctx.channel.send(embed=embed)
                player["trade-pokemon"]["trade-check"] = "no"
            with open("names.json", "w") as jsonFile:
                json.dump(names, jsonFile)
            return


@client.command()
async def putupfortrade(ctx, pokemon: str):
    # display the current users party pokemon
    with open("names.json", "r", encoding="utf8") as jsonFile:
        names = json.load(jsonFile)

    for player in names["players"]:
        if player["name"] == ctx.message.author.nick or player["name"] == ctx.message.author.name:
            if player["trade-pokemon"]["pokemon"]:
                embed = discord.Embed(title="THERE IS ALREADY A POKEMON UP FOR TRADE!")
                embed.set_thumbnail(url=player["trade-pokemon"]["pokemon"]["icon"])
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                await ctx.channel.send(embed=embed)
                return
            for party_pokemon in player["party"]:
                if pokemon.lower() == party_pokemon["name"]:
                    player["trade-pokemon"]["pokemon"] = party_pokemon
                    player["party"].remove(party_pokemon)
                    embed = discord.Embed(title=pokemon.upper() + " HAS BEEN PUT UP FOR TRADE!")
                    embed.set_thumbnail(url=party_pokemon["icon"])
                    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                    await ctx.channel.send(embed=embed)
                    # save it to the json file
                    with open("names.json", "w") as jsonFile:
                        json.dump(names, jsonFile)
                    return


@client.command()
async def pokemonfortrade(ctx):
    with open("names.json", "r", encoding="utf8") as jsonFile:
        names = json.load(jsonFile)
    for player in names["players"]:
        if player["trade-pokemon"]["pokemon"]:
            embed = discord.Embed(title=player["trade-pokemon"]["pokemon"]["name"].upper())
            embed.set_thumbnail(url=player["trade-pokemon"]["pokemon"]["icon"])
            await ctx.channel.send(embed=embed)


@client.command()
async def trade(ctx, other_player: str):
    with open("names.json", "r", encoding="utf8") as jsonFile:
        names = json.load(jsonFile)

    for player in names["players"]:
        if player["name"] == ctx.message.author.nick or player["name"] == ctx.message.author.name:
            for other in names["players"]:
                if other["name"].startswith(other_player.capitalize()):
                    if player["trade-pokemon"]["trade-check"] != "yes" or other["trade-pokemon"][
                        "trade-check"] != "yes":
                        embed = discord.Embed(
                            title="YOU OR THE OTHER PLAYER DO NOT HAVE THEIR TRADE CHECKS SET TO 'YES'!   MAKE SURE BOTH ARE SET TO 'YES' BEFORE TRADING!")
                        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                        await ctx.channel.send(embed=embed)
                        return
                    else:
                        player["trade-pokemon"]["pokemon"], other["trade-pokemon"]["pokemon"] = other["trade-pokemon"][
                                                                                                    "pokemon"], \
                                                                                                player["trade-pokemon"][
                                                                                                    "pokemon"]
                        player["trade-pokemon"]["trade-check"] = "no"
                        other["trade-pokemon"]["trade-check"] = "no"
                        player["box"].append(player["trade-pokemon"]["pokemon"].copy())
                        other["box"].append(other["trade-pokemon"]["pokemon"].copy())
                        player["trade-pokemon"]["pokemon"].pop("name")
                        player["trade-pokemon"]["pokemon"].pop("icon")
                        other["trade-pokemon"]["pokemon"].pop("name")
                        other["trade-pokemon"]["pokemon"].pop("icon")
                        embed = discord.Embed(
                            title="YOU HAVE SUCCESSFULLY TRADED!")
                        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                        await ctx.channel.send(embed=embed)
                        # save it to the json file
                        with open("names.json", "w") as jsonFile:
                            json.dump(names, jsonFile)
                        return


@client.command()
async def takeoutoftrade(ctx, pokemon: str):
    # display the current users party pokemon
    with open("names.json", "r", encoding="utf8") as jsonFile:
        names = json.load(jsonFile)

    for player in names["players"]:
        if player["name"] == ctx.message.author.nick or player["name"] == ctx.message.author.name:
            if player["trade-pokemon"]["pokemon"]["name"] == pokemon.lower():
                player["box"].append(player["trade-pokemon"]["pokemon"].copy())
                embed = discord.Embed(title=pokemon.upper() + " HAS BEEN REMOVED FROM TRADE AND PUT INTO THE BOX!")
                embed.set_thumbnail(url=player["trade-pokemon"]["pokemon"]["icon"])
                player["trade-pokemon"]["pokemon"].pop("name")
                player["trade-pokemon"]["pokemon"].pop("icon")
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                await ctx.channel.send(embed=embed)
                # save it to the json file
                with open("names.json", "w") as jsonFile:
                    json.dump(names, jsonFile)
                return


@client.command()
async def mybox(ctx):
    # display the current users box pokemon
    with open("names.json", "r", encoding="utf8") as jsonFile:
        names = json.load(jsonFile)

    for player in names["players"]:
        if player["name"] == ctx.message.author.nick or player["name"] == ctx.message.author.name:

            list_of_pokemon = "```\n"
            for pokemon in player["box"]:
                # check to see if this pokemon will have character overflow
                if len(list_of_pokemon + pokemon["name"].capitalize() + "\n") > 1024:
                    list_of_pokemon += "\n```"
                    await ctx.channel.send(list_of_pokemon)
                    list_of_pokemon = "```\n"
                else:
                    list_of_pokemon = list_of_pokemon + pokemon["name"].capitalize() + "\n"

            list_of_pokemon += "```"
            await ctx.channel.send(list_of_pokemon)


@client.command()
async def search(ctx, pokemon_name: str):
    with open("names.json", "r", encoding="utf8") as jsonFile:
        names = json.load(jsonFile)

    for player in names["players"]:
        if player["name"] == ctx.message.author.nick or player["name"] == ctx.message.author.name:
            for pokemon in player["party"]:
                if pokemon["name"] == pokemon_name:
                    embed = discord.Embed(title="YOU HAVE A " + pokemon["name"].upper() + "!")
                    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                    embed.set_thumbnail(url=pokemon["icon"])
                    await ctx.channel.send(embed=embed)
                    return
            for pokemon in player["box"]:
                if pokemon["name"] == pokemon_name:
                    embed = discord.Embed(title="YOU HAVE A " + pokemon["name"].upper() + "!")
                    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                    embed.set_thumbnail(url=pokemon["icon"])
                    await ctx.channel.send(embed=embed)
                    return
            embed = discord.Embed(title="YOU DO NOT HAVE A " + pokemon_name.upper())
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            await ctx.channel.send(embed=embed)
            return


@client.command()
async def sort(ctx, sort_type: str):
    with open("names.json", "r", encoding="utf8") as jsonFile:
        names = json.load(jsonFile)

    for player in names["players"]:
        if player["name"] == ctx.message.author.nick or player["name"] == ctx.message.author.name:
            if sort_type == "name":
                embed = discord.Embed(title="SORTING BOX BY NAME!")
                await ctx.channel.send(embed=embed)
                player["box"] = sorted(player["box"], key=lambda k: k['name'])
                # save it to the json file
                with open("names.json", "w") as jsonFile:
                    json.dump(names, jsonFile)
            elif sort_type == "number":
                """TODO try to figure out a way to add the dex numbers to the box and party"""


async def updatepokedex(pokemon_number: int, pokemon: str):
    channel = client.get_channel(TEST_TEXT_CHANNEL)
    with open("pokedex.json", "r", encoding="utf8") as jsonFile:
        pokedex = json.load(jsonFile)

    stats = await channel.fetch_message(853534991647506442)
    if 1 <= pokemon_number <= 90:
        block = await channel.fetch_message(853534947599319040)
        if len(str(pokemon_number)) > 9:
            old_entry = block.content[block.content.index(str(pokemon_number)):23]
        else:
            old_entry = block.content[block.content.index(str(pokemon_number)):22]
        print(old_entry)
        new_entry = str(pokemon_number) + ". " + pokemon.capitalize()
        block.content.replace(old_entry, new_entry)
        print(block.content)
    # block_2 = await channel.fetch_message(853534948404363284)
    # block_3 = await channel.fetch_message(853534949076107274)
    # block_4 = await channel.fetch_message(853534949806047282)
    # block_5 = await channel.fetch_message(853534950540574720)
    # block_6 = await channel.fetch_message(853534968878071810)
    # block_7 = await channel.fetch_message(853534969656770591)
    # block_8 = await channel.fetch_message(853534970617659403)
    # block_9 = await channel.fetch_message(853534971255324682)
    # block_10 = await channel.fetch_message(853534971889057792)
    # block_10 = await channel.fetch_message(853534990919008286)

    i = 0
    while i < len(block.content):
        if block.content[i] == str(pokemon_number):
            pass

    # for i in block.content:
    #     if i == str(pokemon_number):
    #         entry =

    print(block.content)
    return
    text = "```\n"

    seen_pokemon = 0
    obtained_pokemon = 0

    i = 1
    while i <= 899:
        if i == 899:
            text += "\n```"
            await channel.send(text)

            for pokemon in pokedex:
                if "?" not in pokedex.get(pokemon):
                    if "\u25D3" in pokedex.get(pokemon):
                        obtained_pokemon += 1
                        seen_pokemon += 1
                    else:
                        seen_pokemon += 1

            stats = "```\nNumber of Pokemon Caught: " + str(obtained_pokemon) + "\nNumber of Pokemon Seen: " + str(
                seen_pokemon) + "\n```"
            await channel.send(stats)

            return
        text = text + str(i) + ". " + pokedex[str(i)].capitalize() + "\n"
        i += 1
        if i == 899:
            text += ""
        if len(text + str(i) + ". " + pokedex[str(i)].capitalize() + "\n") > 1996:
            print(len(text))
            text += "\n```"
            await channel.send(text)
            text = "```\n"

    for pokemon in pokedex:
        if "?" not in pokedex.get(pokemon):
            if "\u25D3" in pokedex.get(pokemon):
                obtained_pokemon += 1
                seen_pokemon += 1
            else:
                seen_pokemon += 1
    embed = discord.Embed(
        title="Number of Pokemon Caught:  " + str(obtained_pokemon) + "\nNumber of Pokemon Seen:  " + str(seen_pokemon))
    await channel.send(embed=embed)


async def display_pokedex_entry(pokemon: str):
    channel = client.get_channel(POKEMON_TEXT_CHANNEL)
    with open("pokedex.json", "r", encoding="utf8") as jsonFile:
        pokedex = json.load(jsonFile)

    if pokemon in pokedex.values():
        is_caught = False
    elif pokemon + " \u25D3" in pokedex.values():
        is_caught = True

    name_difficulties = {
        "nidoran-f": "nidoran-female",
        "nidoran-m": "nidoran-male",
        "unown-a": "unown",
        "deoxys-normal": "deoxys",
        "burmy-plant": "burmy",
        "arceus-normal": "arceus",
        "basculin-red-striped": "basculin",
        "spewpa-icy-snow": "spewpa",
        "flabebe-red": "flabebe",
        "floette-red": "floette",
        "pumpkaboo-average": "pumpkaboo",
        "oricorio-baile": "oricorio",
        "silvally-normal": "silvally",
        "minior-red-meteor": "minior",
        "mimikyu-disguised": "mimikyu",
        "sinistea-phony": "sinistea",
        "indeedee-male": "indeedee",
        "morpeko-full-belly": "morpeko",
        "zamazenta-hero": "zamazenta"
    }

    if pokemon == "silvally-normal":
        pokemon = "silvally"
    if pokemon == "arceus-normal":
        pokemon = "arceus"
    if pokemon == "burmy-plant":
        pokemon = "burmy"
    if pokemon == "spewpa-icy-snow":
        pokemon = "spewpa"
    if pokemon == "flabebe-red":
        pokemon = "flabebe"
    if pokemon == "floette-red":
        pokemon = "floette"
    if pokemon == "sinistea-phony":
        pokemon = "sinistea"
    if pokemon == "morpeko-full-belly":
        pokemon = "morpeko"
    if pokemon == "unown-a":
        pokemon = "unown"

    official_pokemon = pokemon
    if pokemon in name_difficulties.keys():
        official_pokemon = name_difficulties[pokemon]
    html = urllib.request.urlopen("https://www.pokemon.com/us/pokedex/" + official_pokemon).read()
    soup = BS(html, 'html.parser')

    # access the link and convert it to a json object
    link = "https://pokeapi.co/api/v2/pokemon/" + pokemon
    response = requests.get(link)
    searched_pokemon = json.loads(response.text)

    # traverse paragraphs from soup
    for data in soup.find_all("p"):
        print(data.get_text)
        description = str(data.get_text)
        description = description[51:len(description) - 5]
        print(description)

        if is_caught:
            pokemon += " \u25D3"

        if not is_caught:
            description = "???"

        embed = discord.Embed(
            title=pokemon.upper() + "\n#" + str(searched_pokemon["id"]),
            color=0xa832a4)
        # embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        embed.add_field(name="Description", value=description)
        if not searched_pokemon["game_indices"]:
            embed.set_thumbnail(url=searched_pokemon["sprites"]["front_default"])
        else:
            embed.set_thumbnail(
                url=searched_pokemon["sprites"]["versions"]["generation-v"]["black-white"]["animated"]["front_default"])
        await channel.send(embed=embed)
        return
    return


def get_pokedex_stats():
    obtained_pokemon = 0
    seen_pokemon = 0
    with open("pokedex.json", "r", encoding="utf8") as jsonFile:
        pokedex = json.load(jsonFile)

    for pokemon in pokedex:
        if "?" not in pokedex.get(pokemon):
            if "\u25D3" in pokedex.get(pokemon):
                obtained_pokemon += 1
                seen_pokemon += 1
            else:
                seen_pokemon += 1
    return obtained_pokemon


@client.command()
async def pokedex(ctx, pokemon: str):
    """
    with open("pokedex.json", "r", encoding="utf8") as jsonFile:
        pokedex = json.load(jsonFile)

    text = ""

    i = 1
    while i <= 899:
        if i == 899:
            text += ""
            await ctx.channel.send(text)
            return
        text = text + str(i) + ". " + pokedex[str(i)].capitalize() + "\n"
        i += 1
        if i == 899:
            text += ""
        if len(text + str(i) + ". " + pokedex[str(i)].capitalize() + "\n") > 2000:
            await ctx.channel.send(text)
            text = ""










    print(text)
    # await ctx.channel.send(text)
    """

    if pokemon == "stats":
        obtained_pokemon = 0
        seen_pokemon = 0
        with open("pokedex.json", "r", encoding="utf8") as jsonFile:
            pokedex = json.load(jsonFile)

        for pokemon in pokedex:
            if "?" not in pokedex.get(pokemon):
                if "\u25D3" in pokedex.get(pokemon):
                    obtained_pokemon += 1
                    seen_pokemon += 1
                else:
                    seen_pokemon += 1

        stats = "```\nNumber of Pokemon Caught: " + str(obtained_pokemon) + "\nNumber of Pokemon Seen: " + str(
            seen_pokemon) + "\nYou have obtained " + str(int((obtained_pokemon / 898) * 100)) + "% of the pokemon.```"
        await ctx.channel.send(stats)
        return

    with open("pokedex.json", "r", encoding="utf8") as jsonFile:
        pokedex = json.load(jsonFile)

    if pokemon in pokedex.values():
        is_caught = False
    elif pokemon + " \u25D3" in pokedex.values():
        is_caught = True
    else:
        embed = discord.Embed(
            title="POKEMON NOT DISCOVERED YET!",
            color=0xa832a4)
        await ctx.channel.send(embed=embed)
        return

    name_difficulties = {
        "nidoran-f": "nidoran-female",
        "nidoran-m": "nidoran-male",
        "unown-a": "unown",
        "deoxys-normal": "deoxys",
        "burmy-plant": "burmy",
        "arceus-normal": "arceus",
        "basculin-red-striped": "basculin",
        "spewpa-icy-snow": "spewpa",
        "flabebe-red": "flabebe",
        "floette-red": "floette",
        "pumpkaboo-average": "pumpkaboo",
        "oricorio-baile": "oricorio",
        "silvally-normal": "silvally",
        "minior-red-meteor": "minior",
        "mimikyu-disguised": "mimikyu",
        "sinistea-phony": "sinistea",
        "indeedee-male": "indeedee",
        "morpeko-full-belly": "morpeko",
        "zamazenta-hero": "zamazenta"
    }

    if pokemon == "silvally-normal":
        pokemon = "silvally"
    if pokemon == "arceus-normal":
        pokemon = "arceus"
    if pokemon == "burmy-plant":
        pokemon = "burmy"
    if pokemon == "spewpa-icy-snow":
        pokemon = "spewpa"
    if pokemon == "flabebe-red":
        pokemon = "flabebe"
    if pokemon == "floette-red":
        pokemon = "floette"
    if pokemon == "sinistea-phony":
        pokemon = "sinistea"
    if pokemon == "morpeko-full-belly":
        pokemon = "morpeko"
    if pokemon == "unown-a":
        pokemon = "unown"

    official_pokemon = pokemon
    if pokemon in name_difficulties.keys():
        official_pokemon = name_difficulties[pokemon]
    html = urllib.request.urlopen("https://www.pokemon.com/us/pokedex/" + official_pokemon).read()
    soup = BS(html, 'html.parser')

    # access the link and convert it to a json object
    link = "https://pokeapi.co/api/v2/pokemon/" + pokemon
    response = requests.get(link)
    searched_pokemon = json.loads(response.text)

    # traverse paragraphs from soup
    for data in soup.find_all("p"):
        print(data.get_text)
        description = str(data.get_text)
        description = description[51:len(description) - 5]
        print(description)

        if is_caught:
            pokemon += " \u25D3"

        if not is_caught:
            description = "???"

        embed = discord.Embed(
            title=pokemon.upper() + "\n#" + str(searched_pokemon["id"]),
            color=0xa832a4)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        embed.add_field(name="Description", value=description)
        if not searched_pokemon["game_indices"]:
            embed.set_thumbnail(url=searched_pokemon["sprites"]["front_default"])
        else:
            embed.set_thumbnail(
                url=searched_pokemon["sprites"]["versions"]["generation-v"]["black-white"]["animated"]["front_default"])
        await ctx.channel.send(embed=embed)
        return

    pass


@client.command()
async def swap(ctx, pokemon1: str, pokemon2: str):
    with open("names.json", "r", encoding="utf8") as jsonFile:
        names = json.load(jsonFile)

    p1 = ""
    p2 = ""

    for player in names["players"]:
        if player["name"] == ctx.message.author.nick or player["name"] == ctx.message.author.name:

            for pokemon in player["party"]:
                if pokemon1.lower() == pokemon["name"]:
                    p1 = pokemon
                    print(p1)

            for pokemon in player["party"]:
                if pokemon2.lower() == pokemon["name"]:
                    p2 = pokemon
                    print(p2)

            if p1 == "" or p2 == "":
                await ctx.channel.send("Pokemon not found!")
                return

            i1 = player["party"].index(p1)
            i2 = player["party"].index(p2)

            player["party"][i1], player["party"][i2] = p2, p1
            embed = discord.Embed(title="POKEMON SUCCESSFULLY SWAPPED")
            await ctx.channel.send(embed=embed)

            # save it to the json file
            with open("names.json", "w") as jsonFile:
                json.dump(names, jsonFile)


@client.command()
async def balls(ctx):
    if ctx.channel.id == POKEMON_TEXT_CHANNEL:
        with open("names.json", "r", encoding="utf8") as jsonFile:
            names = json.load(jsonFile)

        for player in names["players"]:
            if player["name"] == ctx.message.author.nick or player["name"] == ctx.message.author.name:
                pokeball_count = player["items"]["pokeball"]
                greatball_count = player["items"]["greatball"]
                ultraball_count = player["items"]["ultraball"]
                masterball_count = player["items"]["masterball"]
                embed = discord.Embed(title="Items:")
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                embed.add_field(name="Pokeballs", value=str(pokeball_count))
                embed.add_field(name="Greatballs", value=str(greatball_count))
                embed.add_field(name="Ultraballs", value=str(ultraball_count))
                embed.add_field(name="Masterballs", value=str(masterball_count))
                embed.set_thumbnail(url="http://pa1.narvii.com/6321/05701fbd1b6f861078e82ff57d17f367b69c5b7a_00.gif")
                await ctx.channel.send(embed=embed)
                return


@client.command()
async def throwrock(ctx):
    # use this to load the json from file
    with open("current_pokemon.json", "r") as jsonFile:
        saved_pokemon = json.load(jsonFile)

    with open("names.json", "r", encoding="utf8") as jsonFile:
        names = json.load(jsonFile)

    if saved_pokemon["pokemon"]["is_caught"] == "no":
        chance = random.randint(1, 3)
        if chance == 3:
            saved_pokemon['pokemon']['is_caught'] = "yes"
            status = "YOU HIT IT! THE WILD " + saved_pokemon["pokemon"]["name"].upper() + " RAN AWAY!"
            current_minute = datetime.now().minute
            next_minute = saved_pokemon["pokemon"]["mins-until-next-pokemon"]
            next_minute -= 15
            if next_minute <= current_minute:
                saved_pokemon["pokemon"]["mins-until-next-pokemon"] = current_minute + 2
                with open("current_pokemon.json", "w") as jsonFile:
                    json.dump(saved_pokemon, jsonFile)
            else:
                if next_minute < 0:
                    saved_pokemon["pokemon"]["mins-until-next-pokemon"] = next_minute + 60
                else:
                    saved_pokemon["pokemon"]["mins-until-next-pokemon"] = next_minute
                with open("current_pokemon.json", "w") as jsonFile:
                    json.dump(saved_pokemon, jsonFile)

            # if current_minute < next_minute:
            #    time_difference = abs(current_minute - next_minute)
            #    if time_difference < 15:
            #        saved_pokemon["pokemon"]["mins-until-next-pokemon"] = current_minute + 2
            #        # save it to the json file
            #        with open("current_pokemon.json", "w") as jsonFile:
            #            json.dump(saved_pokemon, jsonFile)
            #    else:
            #        saved_pokemon["pokemon"]["mins-until-next-pokemon"] -= 15
            #        # save it to the json file
            #        with open("current_pokemon.json", "w") as jsonFile:
            #            json.dump(saved_pokemon, jsonFile)
        else:
            status = "YOU MISS!"
        embed = discord.Embed(
            title="YOU THREW A ROCK AT THE " + saved_pokemon["pokemon"]["name"].upper() + "! " + status)
        embed.set_thumbnail(url=saved_pokemon["pokemon"]["icon"])
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.channel.send(embed=embed)


    else:
        embed = discord.Embed(title="You throw a rock at nothing... Everyone laughs at you...")
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.channel.send(embed=embed)


@client.command(brief="Catch a pokemon with the specified ball.")
async def catch(ctx, ball: str):
    is_new_pokemon = False
    if ctx.channel.id == POKEMON_TEXT_CHANNEL:

        legendary_pokemon = ["mewtwo",
                             "articuno",
                             "zapdos",
                             "moltres",
                             "raikou",
                             "entei",
                             "suicune",
                             "lugia",
                             "ho-oh",
                             "regice",
                             "registeel",
                             "regirock",
                             "latios",
                             "latias",
                             "groudon",
                             "kyogre",
                             "rayquaza",
                             "azelf",
                             "mesprite",
                             "uxie",
                             "dialga",
                             "palkia",
                             "giritina",
                             "cresselia",
                             "heatran",
                             "regigigas",
                             "cobalion",
                             "terrakion",
                             "virizion",
                             "tornadus",
                             "thundurus",
                             "landurus",
                             "zekrom",
                             "reshiram",
                             "kyurem",
                             "xerneas",
                             "yveltal",
                             "zygarde",
                             "type: null",
                             "silvally",
                             "tapu koko",
                             "tapu lele",
                             "tapu bulu",
                             "tapu fini",
                             "cosmog",
                             "cosmoem",
                             "lunala",
                             "solgaleo",
                             "necrozma",
                             "zacian",
                             "zamazenta",
                             "eternatus",
                             "kubfu",
                             "urshifu",
                             "regieleki",
                             "regidrago",
                             "glastrier",
                             "spectrier",
                             "calyrex"]
        mythical_pokemon = ["mew",
                            "celebi",
                            "deoxys",
                            "jirachi",
                            "manaphy",
                            "phione",
                            "darkia",
                            "shaymin",
                            "arceus",
                            "victini",
                            "keldeo",
                            "meloetta",
                            "genesect",
                            "diancie",
                            "hoopa",
                            "volcanian",
                            "magearna",
                            "marshadow",
                            "zeraora",
                            "meltan",
                            "melmetal",
                            "zarude"]

        # use this to load the json from file
        with open("current_pokemon.json", "r") as jsonFile:
            saved_pokemon = json.load(jsonFile)

        with open("names.json", "r", encoding="utf8") as jsonFile:
            names = json.load(jsonFile)

        if saved_pokemon['pokemon']['is_caught'] == 'no':

            # use the specified pokeball
            for player in names["players"]:
                if player["name"] == ctx.message.author.nick or player["name"] == ctx.message.author.name:
                    if ball in player["items"]:
                        if player["items"][ball] > 0:
                            player["items"][ball] -= 1
                        else:
                            embed = discord.Embed(title="You don't have any " + ball.capitalize() + "s!",
                                                  color=0xa832a4)
                            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                            await ctx.channel.send(embed=embed)
                            return
                    else:
                        embed = discord.Embed(title="Ball does not exist", color=0xa832a4)
                        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                        await ctx.channel.send(embed=embed)
                        return

            catch_rate = random.randint(1, 100)

            rate_to_beat = 90
            if saved_pokemon["pokemon"]["name"] in legendary_pokemon:
                rate_to_beat = 95
            if saved_pokemon["pokemon"]["name"] in mythical_pokemon:
                rate_to_beat = 99
            if ball == "masterball":
                catch_rate = 100
            elif ball == "greatball":
                rate_to_beat -= 50
            elif ball == "ultraball":
                rate_to_beat -= 70
            print(catch_rate)
            if catch_rate >= rate_to_beat:

                catch_status = ""
                # save the pokemon to the specified player's party or box
                for player in names["players"]:
                    if player["name"] == ctx.message.author.nick or player["name"] == ctx.message.author.name:
                        if len(player["party"]) == 6:
                            print("Party full, Pokemon sent to PC")
                            catch_status = "YOUR PARTY IS FULL. THE POKEMON HAS BEEN SENT TO YOUR BOX!"
                            player["box"].append(
                                {"name": saved_pokemon["pokemon"]["name"], "icon": saved_pokemon["pokemon"]["icon"]})
                        else:
                            catch_status = "THE POKEMON HAS BEEN ADDED TO YOUR PARTY!"
                            player["party"].append({"name": saved_pokemon["pokemon"]["name"],
                                                    "icon": saved_pokemon["pokemon"]["icon"]})
                    else:
                        print("Player not found!")

                title = "AAAAAAAND IT'S GONE... YOU CAUGHT A " + saved_pokemon["pokemon"][
                    "name"].upper() + "! " + catch_status
                embed = discord.Embed(title=title, color=0xa832a4)
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                embed.set_thumbnail(url=saved_pokemon["pokemon"]["icon"])
                embed.add_field(name="HP", value=saved_pokemon["pokemon"]["hp"])
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                saved_pokemon['pokemon']['is_caught'] = 'yes'

                with open("pokedex.json", "r") as jsonFile:
                    pokedex = json.load(jsonFile)

                if "\u25d3" not in pokedex.get(str(saved_pokemon["pokemon"]["dex-number"])):
                    is_new_pokemon = True

                pokedex[saved_pokemon["pokemon"]["dex-number"]] = saved_pokemon["pokemon"]["name"] + " \u25D3"

                with open("pokedex.json", "w") as jsonFile:
                    json.dump(pokedex, jsonFile)

                # save it to the json file
                with open("current_pokemon.json", "w") as jsonFile:
                    json.dump(saved_pokemon, jsonFile)

                # await updatepokedex(int(saved_pokemon["pokemon"]["dex-number"]), saved_pokemon["pokemon"]["name"])

            else:
                title = "YOU FAILED TO CATCH " + saved_pokemon["pokemon"]["name"].upper() + "!"
                embed = discord.Embed(title=title, color=0xa832a4)
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                embed.set_thumbnail(url=saved_pokemon["pokemon"]["icon"])
                embed.add_field(name="HP", value=saved_pokemon["pokemon"]["hp"])
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        else:
            title = saved_pokemon["pokemon"][
                        "name"].upper() + " IS NO LONGER AVAILABLE, PLEASE WAIT FOR THE NEXT POKEMON! NEXT POKEMON TRAINER IN LINE PLEASE!"
            embed = discord.Embed(title=title, color=0xa832a4)
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            embed.set_thumbnail(url=saved_pokemon["pokemon"]["icon"])
            embed.add_field(name="HP", value=saved_pokemon["pokemon"]["hp"])
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)

    # save it to the json file
    with open("names.json", "w") as jsonFile:
        json.dump(names, jsonFile)

    await ctx.channel.send(embed=embed)
    if is_new_pokemon:
        embed = discord.Embed(title="ADDING " + saved_pokemon["pokemon"]["name"].upper() + "'S DATA TO THE POKEDEX!")
        time.sleep(1)
        await ctx.channel.send(embed=embed)
        time.sleep(1)
        await display_pokedex_entry(saved_pokemon["pokemon"]["name"])


@client.command()
async def release(ctx, pokemon: str):
    with open("names.json", "r", encoding="utf8") as jsonFile:
        names = json.load(jsonFile)

    for player in names["players"]:
        if player["name"] == ctx.message.author.nick or player["name"] == ctx.message.author.name:
            none = 0
            for party_member in player["party"]:
                if party_member["name"] == pokemon.lower():
                    embed = discord.Embed(title=pokemon.upper() + " HAS BEEN RELEASED! BYE BYE, " + pokemon.upper())
                    embed.set_thumbnail(url=party_member["icon"])
                    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                    player["party"].remove(party_member)
                    await ctx.channel.send(embed=embed)
                    # save it to the json file
                    with open("names.json", "w") as jsonFile:
                        json.dump(names, jsonFile)
                    return

                else:
                    none += 1
                    if none == len(player["party"]):
                        embed = discord.Embed(title=pokemon.upper() + " WAS NOT FOUND!")
                        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                        await ctx.channel.send(embed=embed)
        else:
            print("Player not found!")


# join the voice channel
@client.command(brief='Have the bot join the voice channel.')
async def join(ctx):
    time.sleep(.5)
    channel = client.get_channel(438791959444717568)
    connection = await channel.connect()
    connection.play(
        discord.FFmpegPCMAudio(executable='C:/ffmpeg/bin/ffmpeg.exe', source='Diners, Drive Ins And Dives (Intro).mp3'))

    print("I AM JOINING")


# leave the voice channel
@client.command(brief='Make the bot leave the voice channel.')
async def leave(ctx):
    time.sleep(.5)
    server = ctx.message.guild.voice_client
    await server.disconnect(force=True)
    print("I AM LEAVING")


@client.command(brief='Play\'s an audio file from a YouTube video.')
async def play(ctx, url: str):
    # if ctx.author.name == "Freifir":
    #     embed = discord.Embed(title="YOU HAVE BEEN BANNED FROM THE MICKEY MOUSE CLUB FOR INNAPROPRIATE BEHAVIOR.")
    #     await ctx.channel.send(embed=embed)
    #     return
    if url == "https://youtu.be/Jne9t8sHpUc":
        embed = discord.Embed(
            title="JOHN STOP FUCKING POSTING THIS SONG HOLY FUCKING SHIT I SWEAR TO GOD THE ONLY THING IRONIC ABOUT THIS IS THE FACT THAT IT'S A SHITTY SONG. YOU NEED TO LEARN SOME MANNERS.")
        await ctx.channel.send(embed=embed)
        return
    if path.exists("song.mp3"):
        os.remove("song.mp3")

    # this is to make sure to se the audio quality
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'outtmpl': 'song.mp3'
    }

    # download the video
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

        # connect to the channel
        channel = client.get_channel(FLAVOR_TOWN_VOICE)

        # check to see if the bot is already in a voice channel
        if ctx.voice_client is None:
            connection = await channel.connect()
        else:
            connection = ctx.voice_client

        connection.play(discord.FFmpegPCMAudio(executable='C:/ffmpeg/bin/ffmpeg.exe',
                                               source='song.mp3'))


@client.command(brief="Stop the current song or audio clip")
async def stop(ctx):
    connection = discord.utils.get(client.voice_clients, guild=ctx.guild)
    connection.stop()


@client.command(brief="Pause the current song or audio clip")
async def pause(ctx):
    connection = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if connection.is_playing():
        connection.pause()


@client.command(brief="Resume the current song or audio clip")
async def resume(ctx):
    connection = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if connection.is_paused():
        connection.resume()


# why did you call the bot?
@client.command(brief='Call the bot.')
async def bot(ctx):
    time.sleep(.5)
    await ctx.send(f"""You rang, {ctx.message.author.mention}?""")


@client.command(brief='Get the current map rotation in Apex Legends')
async def getmap(ctx):
    time.sleep(.5)

    # access the link and convert it to a json object
    link = "https://api.mozambiquehe.re/maprotation?version=2&auth=mkK7MnR0WXkeUP3TYDkd"
    response = requests.get(link)
    json_object = json.loads(response.text)

    # store the values we want
    current_battle_map = str(json_object["battle_royale"]["current"]["map"])
    current_battle_time = str(json_object["battle_royale"]["current"]["remainingTimer"])
    next_battle_map = str(json_object["battle_royale"]["next"]["map"])

    # convert it into an embed
    embed = discord.Embed(title="CURRENT MAP ROTATION FOR APEX LEGENDS!", color=0xa832a4)
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    embed.add_field(name="Current Map", value=current_battle_map)
    if current_battle_map == "World\'s Edge":
        embed.set_thumbnail(url="https://i.imgur.com/6AnA9ba.png")
    if current_battle_map == "Olympus":
        embed.set_thumbnail(url="https://mp1st.com/wp-content/uploads/2020/11/apex-legends-olmpus-scaled.jpg")
    if current_battle_map == "King\'s Canyon":
        embed.set_thumbnail(
            url="https://static.wikia.nocookie.net/apexlegends_gamepedia_en/images/e/e3/Loadingscreen_Kings_Canyon.png/revision/latest?cb=20190930035209")
    embed.add_field(name="Remaining Time", value=current_battle_time)
    embed.add_field(name="Next Map", value=next_battle_map)
    embed.add_field(name="-------------------------",
                    value="[Here is the arenas map rotation if you're curious](https://apexmap.kuroi.io/arenas)")
    await ctx.channel.send(embed=embed)


@client.command(brief='Have the guy list the server information.')
async def server(ctx):
    time.sleep(.5)
    await ctx.send(
        f"""Server name: {ctx.guild.name}\nTotal members: {ctx.guild.member_count}\nCreated on: {ctx.guild.created_at}\nRegion: {ctx.guild.region}""")


@client.command(brief='Oh egads, my roast is ruined.')
async def steamedhams(ctx):
    time.sleep(.5)
    channel = client.get_channel(FLAVOR_TOWN_VOICE)

    if ctx.voice_client is None:
        connection = await channel.connect()
    else:
        connection = ctx.voice_client

    connection.play(discord.FFmpegPCMAudio(executable='C:/ffmpeg/bin/ffmpeg.exe',
                                           source='Steamed Hams.mp3'))


@client.command(brief='Ba Dum Tss.')
async def joke(ctx):
    time.sleep(.5)
    channel = client.get_channel(438791959444717568)
    connection = await channel.connect()
    connection.play(discord.FFmpegPCMAudio(executable='C:/ffmpeg/bin/ffmpeg.exe', source='Joke-drum-sound.mp3'))


@client.command(brief='Have the guy eat into your ear.')
async def hungry(ctx):
    time.sleep(.5)
    channel = client.get_channel(438791959444717568)
    connection = await channel.connect()
    connection.play(discord.FFmpegPCMAudio(executable='C:/ffmpeg/bin/ffmpeg.exe', source='eating.mp3'))


@client.command(brief='Plays the \'are you a truck?\' sound clip.')
async def areyouatruck(ctx):
    channel = client.get_channel(438791959444717568)
    connection = await channel.connect()
    connection.play(
        discord.FFmpegPCMAudio(executable='C:/ffmpeg/bin/ffmpeg.exe', source='No.mp3'))
    time.sleep(1)
    server = ctx.message.guild.voice_client
    await server.disconnect(force=True)


@client.command(brief='Have the guy tell your fortune.')
async def eightball(ctx):
    time.sleep(.5)
    if len(ctx.message.content) > 10:
        answers = ["Certainly, my dude!",
                   "I have decided it so!",
                   "NO DOUBT!",
                   "Yes - Yes - Yes - Yes - Yes ",
                   "You may rely on it!",
                   "As I see it, hell yea!",
                   "Most likely, hombre!",
                   "Outlook lookin' good here, dude!",
                   "YEA!",
                   "Signs from Flavor Town point to yes!",
                   "The sauce is a little hazy, try again",
                   "Ask again later, I'm tired.",
                   "Better not tell you now. . .",
                   "Cannot predict now, busy eating some slammin' burgers.",
                   "Concentrate on the flavor and ask again.",
                   "Don't count on it, hombre.",
                   "My reply is nuh-uh.",
                   "My inside sources say no.",
                   "Outlook lookin' not so good, dude.",
                   "Doubt."]

        reply = random.choice(answers)
        embed = discord.Embed(title="Question: " + ctx.message.content[11:len(ctx.message.content)].capitalize(),
                              color=0xa832a4)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        embed.add_field(name="Answer: " + reply, value='\u200b')
        await ctx.send(embed=embed)

    else:
        embed = discord.Embed(title="You gotta give me a yes or no question, hombre!")
        await ctx.send(embed=embed)


@tasks.loop()
async def remind_john():
    current_hour = datetime.now().hour
    current_minute = datetime.now().minute
    current_second = datetime.now().second
    current_weekday = datetime.now().weekday()

    if current_weekday == 1 and current_hour == 21 and current_minute == 30 and current_second == 0:
        channel = client.get_channel(438791959444717568)
        connection = await channel.connect()
        connection.play(
            discord.FFmpegPCMAudio(executable='C:/ffmpeg/bin/ffmpeg.exe', source='moist.mp3'))
        time.sleep(11)
        server = channel.message.guild.voice_client
        await server.disconnect(force=True)


@tasks.loop()
async def wild_pokemon():
    # use this to load the json from file

    global pokemon_number
    with open("current_pokemon.json", "r") as jsonFile:
        saved_pokemon = json.load(jsonFile)
    current_minute = datetime.now().minute
    current_second = datetime.now().second

    if current_minute == saved_pokemon["pokemon"]["mins-until-next-pokemon"] and current_second == 5:

        minutes_until_next_pokemon = random.randint(10, 60)
        print(minutes_until_next_pokemon)
        if current_minute + minutes_until_next_pokemon >= 60:
            minutes_until_next_pokemon = minutes_until_next_pokemon + current_minute - 60
        else:
            minutes_until_next_pokemon += current_minute
        saved_pokemon["pokemon"]["mins-until-next-pokemon"] = minutes_until_next_pokemon
        time.sleep(1)
        is_shiny = False
        caught_pokemon = get_pokedex_stats()
        if 449 <= caught_pokemon <= 674:
            new_pokemon_chance = random.randint(1, 2)
            if new_pokemon_chance == 2:
                new_pokemon = False
                while not new_pokemon:
                    with open("pokedex.json", "r") as jsonFile:
                        pokedex = json.load(jsonFile)
                    pokemon_number = random.randint(1, 898)
                    if "\u25D3" not in pokedex.get(str(pokemon_number)):
                        print("WE GOT A NEW POKEMON!!!")
                        new_pokemon = True
            else:
                pokemon_number = random.randint(1, 898)
        elif 675 <= caught_pokemon <= 797:
            new_pokemon_chance = random.randint(1, 4)
            if new_pokemon_chance != 4:
                new_pokemon = False
                while not new_pokemon:
                    with open("pokedex.json", "r") as jsonFile:
                        pokedex = json.load(jsonFile)
                    pokemon_number = random.randint(1, 898)
                    if "\u25D3" not in pokedex.get(str(pokemon_number)):
                        print("WE GOT A NEW POKEMON!!!")
                        new_pokemon = True
            else:
                pokemon_number = random.randint(1, 898)
        elif caught_pokemon >= 798:
            new_pokemon = False
            while not new_pokemon:
                with open("pokedex.json", "r") as jsonFile:
                    pokedex = json.load(jsonFile)
                pokemon_number = random.randint(1, 898)
                if "\u25D3" not in pokedex.get(str(pokemon_number)):
                    print("WE GOT A NEW POKEMON!!!")
                    new_pokemon = True
        else:
            pokemon_number = random.randint(1, 898)
        shiny_odd = random.randint(1, 1000)

        if shiny_odd == 999:
            is_shiny = True

        # access the link and convert it to a json object
        link = "https://pokeapi.co/api/v2/pokemon/" + str(pokemon_number)
        response = requests.get(link)
        pokemon = json.loads(response.text)

        current_pokemon = str(pokemon["forms"][0]["name"])

        channel = client.get_channel(POKEMON_TEXT_CHANNEL)

        # convert it into an embed

        with open("pokedex.json", "r") as jsonFile:
            pokedex = json.load(jsonFile)

        if "\u25D3" not in pokedex[str(pokemon_number)]:
            pokedex[str(pokemon_number)] = current_pokemon

        shiny_text = ""
        caught_symbol = ""
        if is_shiny:
            shiny_text = "*SHINY* "

        if "\u25D3" in pokedex.get(str(pokemon_number)):
            caught_symbol = "\u25D3"

        embed = discord.Embed(title="A WILD " + shiny_text + current_pokemon.upper() + caught_symbol + " APPEARED!",
                              color=0xa832a4)

        with open("pokedex.json", "w") as jsonFile:
            json.dump(pokedex, jsonFile)

        # await updatepokedex(pokemon_number, current_pokemon)

        if pokemon_number > 649:
            if is_shiny:
                embed.set_thumbnail(url=pokemon["sprites"]["front_shiny"])
                saved_pokemon["pokemon"]["icon"] = pokemon["sprites"]["front_shiny"]
            else:
                embed.set_thumbnail(url=pokemon["sprites"]["front_default"])
                saved_pokemon["pokemon"]["icon"] = pokemon["sprites"]["front_default"]
        else:
            if is_shiny:
                embed.set_thumbnail(
                    url=pokemon["sprites"]["versions"]["generation-v"]["black-white"]["animated"]["front_shiny"])
                saved_pokemon["pokemon"]["icon"] = \
                    pokemon["sprites"]["versions"]["generation-v"]["black-white"]["animated"]["front_shiny"]
            else:
                embed.set_thumbnail(
                    url=pokemon["sprites"]["versions"]["generation-v"]["black-white"]["animated"]["front_default"])
                saved_pokemon["pokemon"]["icon"] = \
                    pokemon["sprites"]["versions"]["generation-v"]["black-white"]["animated"]["front_default"]

        calculated_hp = 2 * int(pokemon["stats"][0]["base_stat"]) + 10

        # overwrite the data
        saved_pokemon["pokemon"]["name"] = current_pokemon
        saved_pokemon["pokemon"]["dex-number"] = str(pokemon_number)
        saved_pokemon["pokemon"]["is_caught"] = 'no'
        saved_pokemon["pokemon"]["hp"] = calculated_hp

        # save it to the json file
        with open("current_pokemon.json", "w") as jsonFile:
            json.dump(saved_pokemon, jsonFile)

        await channel.send(embed=embed)


@tasks.loop()
async def replenish_balls():
    current_hour = datetime.now().hour
    current_minute = datetime.now().minute
    current_second = datetime.now().second

    channel = client.get_channel(POKEMON_TEXT_CHANNEL)

    if current_hour == 15 and current_minute == 34 and current_second == 20:
        time.sleep(1)
        with open("names.json", "r", encoding="utf8") as jsonFile:
            names = json.load(jsonFile)

        for player in names["players"]:
            player["items"]["pokeball"] = 10
            player["items"]["greatball"] = 5
            player["items"]["ultraball"] = 2

        # save it to the json file
        with open("names.json", "w") as jsonFile:
            json.dump(names, jsonFile)

        embed = discord.Embed(title="BALLS REPLENISHED!")
        await channel.send(embed=embed)


@client.command(brief='This sound clip is 1 in 100.')
async def sammyhagar(ctx):
    channel = ctx.author.voice.channel
    connection = await channel.connect()
    num = random.randint(1, 100)
    print(num)
    if num % 10 == 0:
        connection.play(
            discord.FFmpegPCMAudio(executable='C:/ffmpeg/bin/ffmpeg.exe', source='sammyhagarooo.mp3'))
        time.sleep(3)
    elif num == 99:
        connection.play(
            discord.FFmpegPCMAudio(executable='C:/ffmpeg/bin/ffmpeg.exe', source='nope.mp3'))
        time.sleep(10)
    else:
        connection.play(
            discord.FFmpegPCMAudio(executable='C:/ffmpeg/bin/ffmpeg.exe', source='sammyhagar.mp3'))
        time.sleep(3)

    server = ctx.message.guild.voice_client
    await server.disconnect(force=True)


@client.command(brief='You\'re a loser if you use this command.')
async def loser(ctx):
    channel = client.get_channel(438791959444717568)
    connection = await channel.connect()
    connection.play(
        discord.FFmpegPCMAudio(executable='C:/ffmpeg/bin/ffmpeg.exe', source='loser.mp3'))
    time.sleep(12)
    server = ctx.message.guild.voice_client
    await server.disconnect(force=True)


@client.command(brief='Plays the pickled sound clip.')
async def pickled(ctx):
    channel = client.get_channel(438791959444717568)
    connection = await channel.connect()
    connection.play(
        discord.FFmpegPCMAudio(executable='C:/ffmpeg/bin/ffmpeg.exe', source='owo.mp3'))
    time.sleep(5)
    server = ctx.message.guild.voice_client
    await server.disconnect(force=True)


@client.command(brief='Get the current weather from any town.')
async def getweather(ctx):
    time.sleep(.5)
    city = str(ctx.message.content)
    city = city[12:len(city)].capitalize()
    print(city)
    if city == "Flavortown":
        embed = discord.Embed(
            title="FLAVORTOWN ONLY HAS ONE WEATHER AND THAT WEATHER IS KICKASS BBQ RIBS SLATHERED ON A FUCKIN' PIZZA STICK DEEP FRIED IN GRAVY SAUSAGE "
                  "AND SERVED WITH A SIDE OF MY FAMOUS CHIPS AND JACKASS HOT SALSA!")
        await ctx.channel.send(embed=embed)
    else:
        complete_url = base_url + "appid=" + api_key + "&q=" + city
        response = requests.get(complete_url)
        print(complete_url)
        x = response.json()
        if x["cod"] != "404":

            # store the value of "main"
            # key in variable y
            y = x["main"]

            # store the value corresponding
            # to the "temp" key of y
            current_temperature = y["temp"]

            # store the value corresponding
            # to the "pressure" key of y
            current_pressure = y["pressure"]

            # store the value corresponding
            # to the "humidity" key of y
            current_humidiy = y["humidity"]

            # store the value of "weather"
            # key in variable z
            z = x["weather"]

            # store the value corresponding
            # to the "description" key at
            # the 0th index of z
            weather_description = z[0]["description"]

            temp_in_f = current_temperature * (9 / 5) - 459.67
            temp_in_f = round(temp_in_f)

            embed = discord.Embed(title="AW MAN! HERE IS THE WEATHER FOR " + city + "!")
            embed.add_field(name="Temperature", value=str(temp_in_f) + ' deg')
            embed.add_field(name="Description", value=weather_description)
            embed.add_field(name="Humidity", value=str(current_humidiy) + "%")
            await ctx.channel.send(embed=embed)

        else:
            embed = discord.Embed(
                title="Sorry Dude. . . that place don't exist in my mind. Make sure if there are multiple "
                      "words you use spaces.")
            await ctx.channel.send(embed=embed)


@client.command(brief='Awaken the masters.')
async def awaken(ctx):
    time.sleep(.5)
    channel = client.get_channel(438791959444717568)
    connection = await channel.connect()
    connection.play(discord.FFmpegPCMAudio(executable='C:/ffmpeg/bin/ffmpeg.exe', source='awaken.mp3'))


@client.command(brief='Play Giorno\'s theme.')
async def jojo(ctx):
    time.sleep(.5)
    channel = client.get_channel(438791959444717568)
    connection = await channel.connect()
    connection.play(discord.FFmpegPCMAudio(executable='C:/ffmpeg/bin/ffmpeg.exe', source='giorno.mp3'))


@client.command(brief='Play \'DejaVu!\'')
async def dejavu(ctx):
    time.sleep(.5)
    channel = client.get_channel(438791959444717568)
    connection = await channel.connect()
    connection.play(discord.FFmpegPCMAudio(executable='C:/ffmpeg/bin/ffmpeg.exe', source='dejavu.mp3'))


@client.command(brief='Have Obama sing the Gay Baby Jail theme song.')
async def gaybabyjail(ctx):
    time.sleep(.5)
    channel = client.get_channel(438791959444717568)
    connection = await channel.connect()
    connection.play(discord.FFmpegPCMAudio(executable='C:/ffmpeg/bin/ffmpeg.exe', source='gaybabyjail.mp3'))


@client.command(brief='NOOO it\'s Sammy Hagar\'s Jager Meister, Hagarmeister!')
async def hagarmeister(ctx):
    channel = client.get_channel(438791959444717568)
    connection = await channel.connect()
    connection.play(
        discord.FFmpegPCMAudio(executable='C:/ffmpeg/bin/ffmpeg.exe', source='hagarmeister.mp3'))
    time.sleep(5)
    server = ctx.message.guild.voice_client
    await server.disconnect(force=True)


@client.command(brief='You got bamboozled.')
async def bamboozle(ctx):
    time.sleep(.5)
    channel = client.get_channel(438791959444717568)
    connection = await channel.connect()
    connection.play(discord.FFmpegPCMAudio(executable='C:/ffmpeg/bin/ffmpeg.exe', source='bamboozled.mp3'))


@client.command(brief='Have the guy roll some dice for you.', description='This is the full description')
async def roll(ctx):
    list_of_dice = {"D2": rollD2(), "D4": rollD4(), "D6": rollD6(), "D8": rollD8(), "D10": rollD10(),
                    "D12": rollD12(), "D20": rollD20(), "D100": rollD100()}
    time.sleep(.5)
    channel = client.get_channel(698323553493188640)
    user_message = str(ctx.message.content)
    current_dice = user_message[6:len(user_message)].capitalize()
    if current_dice in list_of_dice:
        result = list_of_dice[current_dice]
        await channel.send(result)

    else:
        await channel.send("Hey hombre, that dice don't make sense to me. Pick another from my flammin' dice set.")


@client.command()
async def remindme(ctx, reminder_time: str, *message):
    current_epoch_time = int(time.time())

    SECOND = 1
    MINUTE = 60
    HOUR = 3600
    DAY = 86400
    WEEK = 604800
    MONTH = 2592000
    YEAR = 31536000

    num_len = 0
    for letter in reminder_time:
        if letter.isdigit():
            num_len += 1

    num = int(reminder_time[0:num_len])

    string_message = ""
    for word in message:
        string_message = string_message + word + " "

    print(ctx.author.name)

    # check for seconds
    if reminder_time.endswith("second") or reminder_time.endswith("seconds"):
        number_of_seconds = SECOND * num

    # check for minutes
    elif reminder_time.endswith("minute") or reminder_time.endswith("minutes"):
        number_of_seconds = MINUTE * num

    # check for hours
    elif reminder_time.endswith("hour") or reminder_time.endswith("hours"):
        number_of_seconds = HOUR * num

    # check for days
    elif reminder_time.endswith("day") or reminder_time.endswith("days"):
        number_of_seconds = DAY * num

    # check for weeks
    elif reminder_time.endswith("week") or reminder_time.endswith("weeks"):
        number_of_seconds = WEEK * num

    # check for months
    elif reminder_time.endswith("month") or reminder_time.endswith("months"):
        number_of_seconds = MONTH * num

    # check for years
    elif reminder_time.endswith("year") or reminder_time.endswith("years"):
        number_of_seconds = YEAR * num

    # the input must be wrong
    else:
        return

    seconds_until_reminder = number_of_seconds + current_epoch_time

    with open("reminders.json", "r") as jsonFile:
        user_reminders = json.load(jsonFile)

    message_and_reminder = {"message": string_message,
                            "time-until-send": seconds_until_reminder}

    found = False
    for user in user_reminders["users"]:
        if user["name"] == ctx.message.author.name:
            found = True
            user["messages"].append(message_and_reminder)
    if not found:
        user_reminders["users"].append({"name": ctx.message.author.name,
                                        "messages": [message_and_reminder]})

    with open("reminders.json", "w") as jsonFile:
        json.dump(user_reminders, jsonFile)

    datetime_time = datetime.fromtimestamp(seconds_until_reminder - (HOUR * 7))
    embed = discord.Embed(title="REMINDER SET FOR ~ " + str(datetime_time) + " ~")
    await ctx.channel.send(embed=embed)


@tasks.loop()
async def check_reminders():
    current_epoch_time = int(time.time())

    channel = client.get_channel(THE_FIERI_LAIR_TEXT)

    with open("reminders.json", "r") as jsonFile:
        user_reminders = json.load(jsonFile)

    for user in user_reminders["users"]:
        for message in user["messages"]:
            if message["time-until-send"] == current_epoch_time:
                await channel.send("@" + user["name"])
                embed = discord.Embed(title="YOU HAVE A REMINDER!")
                embed.add_field(name="Message", value=message["message"])
                await channel.send(embed=embed)
                user["messages"].remove(message)
                with open("reminders.json", "w") as jsonFile:
                    json.dump(user_reminders, jsonFile)


@client.event
async def on_ready():
    remind_john.start()
    wild_pokemon.start()
    replenish_balls.start()
    check_reminders.start()

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(current_time)


def rollD2():
    return str(random.randint(1, 2))


def rollD4():
    return str(random.randint(1, 4))


def rollD6():
    return str(random.randint(1, 6))


def rollD8():
    return str(random.randint(1, 8))


def rollD10():
    return str(random.randint(1, 10))


def rollD12():
    return str(random.randint(1, 12))


def rollD20():
    return str(random.randint(1, 20))


def rollD100():
    return str(random.randint(1, 100))


# start the bot
client.run(token)

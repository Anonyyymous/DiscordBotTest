import discord
import os
import subprocess
import random
from HungerGamesClasses import Player, GameManager, clean_input_for_games
from TimetableChecker import get_day

# im going to regret this
tokenPath = "/home/oreo/Desktop/DiscordBot/token.txt"
file = open(tokenPath, "r")
token = file.readline()
file.close()

intents = discord.Intents(messages=True, guilds=True, message_content=True)
client = discord.Client(intents=intents)
ids = {"john": 331837038024327182, "lauren": 423146074233110528, "isaac": 386783880637579286}
message_count = 0
playing_hunger_games = False
ash_count = 0
game_manager = None

stored_file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "NamesCount.txt")

@client.event
async def on_ready():
    print("logged in as {0.user}".format(client))
    get_names()
    # await client.user.edit(username="John's assistant")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    global ash_count, message_count, playing_hunger_games, game_manager
    message_count += 1
    print("message sent", message.content)

    if message.content == "-update":
        subprocess.call(["sh", "./update.sh"])
        exit

    rand_num = random.randrange(0, 500)
    if rand_num == 69:
        await message.channel.send("kill yourself - wiktor")

    if message_count == 15:
        message_count = 0
        save_names(["ash", "sofia"], [ash_count, sofia_count])
        print("names saved")
    FuF = ["fucku", "fuckyou"]

    message_contents_full = message.content.lower()
    message_contents = message.content.lower().strip()
    if message_contents in FuF:
        await message.channel.send("not if i fuck you first")
        print("successfully fucked")
    elif message_contents == "kys":
        await message.channel.send("awww keep yourself safe so sweet")

    elif "good morning" in message_contents:
        await message.channel.send("go die")

    elif "-hungergames" == message_contents[:12]:
        if playing_hunger_games:
            # -hungergames|john|isaac|lauren|wiktor|george|kerry|biggie dikkie mikkie|matteo|filip
            output, playing_hunger_games = game_manager.play_round()
            await message.channel.send(output)
        else:
            playing_hunger_games = True
            game_manager = GameManager(clean_input_for_games(message_contents))
            await message.channel.send(game_manager.play_round()[0])
    elif "-timetable" == message_contents[:10]:
        await message.channel.send(get_day())

    elif message.author.id == ids["isaac"] and "ash" in message_contents_full:  # because he could say 'a sheep' for example
        ash_count+=1
    elif message.author.id != ids["lauren"] and message_contents == "-summon isaac":
        print("summoning isaac")
        await message.channel.send("<@386783880637579286> <@386783880637579286> <@386783880637579286> <@386783880637579286> <@386783880637579286>")

    elif message_contents == "-update":
        message_count = 0
        save_names(["ash"], [ash_count])
        print("names saved")
    elif message_contents == "-counters":
        await message.channel.send(f"ash count: {ash_count}")

def get_names():
    if os.path.exists(stored_file_name):
        global sofia_count, ash_count
        with open(stored_file_name, "r") as f:
            lines = f.readlines()
            ash_count = int(lines[0].split("|")[1])
            sofia_count = int(lines[1].split("|")[1])
            print("read file")
            print(f"names = {ash_count}")
    else:
        save_names(["ash"], [38])

def save_names(names, numbers):
    with open(stored_file_name, "w") as f:
        for i in range(len(names)):
            f.write(f"{names[i]}|{numbers[i]}\n")
        print("created file")

client.run(token)

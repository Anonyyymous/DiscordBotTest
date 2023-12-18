import discord
import os
import random
from HungerGamesClasses import Player, GameManager, clean_input_for_games
from TimetableChecker import get_day

# im going to regret this
tokenPath = "/home/oreo/Desktop/DiscordBot/token.txt"  # could at some point replace with an if statement, so this works on my pc as well without replacing the code with the token
# or, could use os.path.dirname, some splits, and store it in the same place relative to those directions on each machine

# reading token
file = open(tokenPath, "r")
token = file.readline()
file.close()

# initialising bot
intents = discord.Intents(messages=True, guilds=True, message_content=True)
client = discord.Client(intents=intents)

# initialising other variables
ids = {"john": 331837038024327182, "lauren": 423146074233110528, "isaac": 386783880637579286}
message_count = 0
playing_hunger_games = False
ash_count = 0
game_manager = None

thisDir = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

responsesFile = open(os.path.join(thisDir, "responses.txt"), "r")
responses = responsesFile.readlines()
responsesFile.close()

namesCountFile = open(os.path.join(thisDir, "NamesCount.txt"), "r")
nameCounters = namesCountFile.readlines()
namesCountFile.close()

stored_file_name = os.path.realpath(os.path.join(thisDir, "NamesCount.txt"))  # i think just "NamesCount.txt" should work, im not sure what prompted this

@client.event
async def on_ready():  # executed on bot setup
    print("logged in as {0.user}".format(client))
    get_names()
    await client.wait_until_ready()
    channel = client.get_channel(1181162678740324392)
    await channel.send(client.user.display_name + " up and running.")
    # await client.user.edit(username="John's assistant")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    global ash_count, message_count, playing_hunger_games, game_manager
    message_count += 1
    message_contents_full = message.content.lower()
    message_contents = message.content.lower().strip()
    
    print(message.author.name + ": " + message.content)

    if message_contents == "-updatebot":
        await message.reply("Restarting...")
        await client.close()
        exit()

    for i in range(len(responses)):
        response = responses[i].split('<>')
        words = response[0].split('//')
        for j in range(len(words)):
            if words[j] in message_contents:
                if str(message.author.id) in response[1].split('//') or response[1] == "all":
                    if random.random() < float(response[2]):
                        answers = response[3].split('//')
                        await message.channel.send(random.choice(answers))

    for i in range(len(nameCounters)):
        if nameCounters[i].split('|')[0].split('-')[1] in message_contents and nameCounters[i].split('|')[0].split('-')[0] == str(message.author.id):
            nameCounters[i] = nameCounters[i].split('|')[0] + int(nameCounters[i].split('|')[1]) + message_contents.count(nameCounters[i].split('|')[0].split('-')[1])

    namesCountText = ""
    for i in range(len(nameCounters)):
        namesCountText += nameCounters[i] + '\n'

    namesCountFile = open(os.path.join(thisDir, "NamesCount.txt"), "w")
    namesCountFile.write(namesCountText)
    namesCountFile.close()
    
    rand_num = random.randrange(0, 500)

    # random responses
    if rand_num == 69:
        await message.channel.send("kill yourself - wiktor")

    #if message_count == 15:  # not necessary now, might remove, or make it random
    #    message_count = 0
    #    save_names(["ash"], [ash_count])
    #    print("names saved")

    # activities
    if "-hungergames" == message_contents[:12]:
        if playing_hunger_games:
            # -hungergames|john|isaac|lauren|wiktor|george|kerry|biggie dikkie mikkie|matteo|filip
            output, playing_hunger_games = game_manager.play_round()
            await message.channel.send(output)
        else:
            playing_hunger_games = True
            game_manager = GameManager(clean_input_for_games(message_contents))
            await message.channel.send(game_manager.play_round()[0])
    elif "-timetable" == message_contents:
        await message.channel.send(get_day())

    # displaying counters
    #elif message_contents == "-update":  # this could be removed
    #    message_count = 0
    #    save_names(["ash"], [ash_count])
    #    print("names saved")
    elif message_contents == "-counters":
        await message.channel.send(f"ash count: {ash_count}")

def get_names():
    if os.path.exists(stored_file_name):
        global ash_count
        with open(stored_file_name, "r") as f:
            lines = f.readlines()
            ash_count = int(lines[0].split("|")[1])
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
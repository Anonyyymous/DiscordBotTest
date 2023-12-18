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
playing_hunger_games = False
game_manager = None

thisDir = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

responsesFile = open(os.path.join(thisDir, "responses.txt"), "r")
responses = responsesFile.readlines()
responsesFile.close()

@client.event
async def on_ready():  # executed on bot setup
    print("logged in as {0.user}".format(client))
    #get_names()
    await client.wait_until_ready()
    channel = client.get_channel(1181162678740324392)
    await channel.send(client.user.display_name + " up and running.")
    # await client.user.edit(username="John's assistant")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    global playing_hunger_games, game_manager
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

    namesCountFile = open(os.path.join(thisDir, "NamesCount.txt"), "r")
    nameCounters = namesCountFile.readlines()
    namesCountFile.close()

    for i in range(len(nameCounters)):
        try:
            currentNameCounter = nameCounters[i].replace('\n', '')
            if currentNameCounter == "":
                continue
            identifier = currentNameCounter.split('|')[0]
            if identifier.split('-')[1] in message_contents and identifier.split('-')[0] == str(message.author.id):
                print(identifier.split('-')[0] + " said " + identifier.split('-')[1])
                nameCounters[i] = nameCounters[i].split('|')[0] + "|" + str(int(nameCounters[i].split('|')[1]) + message_contents.count(identifier.split('-')[1]))
        except:
            print("ERROR IDK")

    namesCountText = ""
    for i in range(len(nameCounters) - 1):
        namesCountText += str(nameCounters[i].replace('\n', '')) + "\n"
    namesCountText += str(nameCounters[-1])

    namesCountFile = open(os.path.join(thisDir, "NamesCount.txt"), "w")
    namesCountFile.write(namesCountText)
    namesCountFile.close()
    
    rand_num = random.randrange(0, 500)

    # random responses
    if rand_num == 69:
        await message.channel.send("kill yourself - wiktor")

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
    elif message_contents == "-counters":
        namesCountFile = open(os.path.join(thisDir, "NamesCount.txt"), "r")
        nameCounters = namesCountFile.readlines()
        namesCountFile.close()
        text = ""
        for i in range(len(nameCounters)):
            text += nameCounters[i]
        await message.channel.send(text)

client.run(token)
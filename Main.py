import discord
import os
import regex
import random
from HungerGamesClasses import Player, GameManager, clean_input_for_games
from TimetableChecker import get_day
import json

thisDir = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

tokenPath = os.path.join(os.getcwd(), "local/token.txt")

# reading token
file = open(tokenPath, "r")
token = file.readline()
file.close()

# initialising bot
intents = discord.Intents(messages=True, guilds=True, message_content=True)
client = discord.Client(intents=intents)

# initialising other variables
ids = {"john": 331837038024327182, "lauren": 423146074233110528, "isaac": 386783880637579286, "kerry": 736925796584915024}
playing_hunger_games = False
game_manager = None

responsesFile = open(os.path.join(thisDir, "responses.txt"), "r")
responses = responsesFile.readlines()
responsesFile.close()

@client.event
async def on_ready():  # executed on bot setup
    print("logged in as {0.user}".format(client))
    #get_names()
    await client.wait_until_ready()
    channel = client.get_channel(1186638026781249606)
    await channel.send(client.user.display_name + " up and running.")
    # await client.user.edit(username="John's assistant")

# @client.command(pass_context=True)  # idk i stole it from online :p
async def send(channel, text):  # might need to @client.event wrapper but dont think so. If this doesnt work, just replace it for now
    if channel.id == 1186331140030746764:  # if channel.id in bot_free_channels
        return
    await channel.send(text)

async def log(text):
    await client.get_channel(1186359268073554071).send(text)

@client.event
async def on_message(message):
    if message.author == client.user:  # for bot-free zone, could be loaded into a json later for bot-free channels
        return
    
    global playing_hunger_games, game_manager, counters
    message_contents_full = message.content.lower()
    message_contents = message.content.lower().strip()
    
    print(message.author.name + ": " + message.content)

    if message_contents == "-updatebot":
        await message.reply("Restarting...")
        await client.close()
        exit()

    await HandleResponses(message)

    await HandleCounters(message)
    
    rand_num = random.randrange(0, 500)

    # random responses
    if rand_num == 69:
        await send(message.channel, "kill yourself - wiktor")

    # activities
    if "-hungergames" == message_contents[:12]:
        if playing_hunger_games:
            # -hungergames|john|isaac|lauren|wiktor|george|kerry|biggie dikkie mikkie|matteo|filip
            output, playing_hunger_games = game_manager.play_round()
            await send(message.channel, output)
        else:
            playing_hunger_games = True
            game_manager = GameManager(clean_input_for_games(message_contents))
            await send(message.channel, game_manager.play_round()[0])
    elif "-timetable" == message_contents:
        await send(message.channel, get_day())
    elif "-roulette" == message_contents:
        member_id = Random.choice(message.guild.members)
        await log(f"{message.guild}")
        st = f"{member_id}"
        str1 = ''.join(f"<{member_id}> " for i in range(10))
        await send(message.channel, st)
        await send(message.channel, str1)  # im being generous
    elif message_contents == "-counters":
        phraseCountFile = open(os.path.join(os.getcwd(),"local/phraseCounters.txt"), "r")
        currentCounts = phraseCountFile.readlines()
        phraseCountFile.close()
        
        text = ""
        
        for phrase in currentCounts:
            text += GetName(phrase.split('|')[0].split('-')[0]) + " " + phrase.split('|')[0].split('-')[1] + " count: " + phrase.split('|')[1]

        await send(message.channel, text)

async def HandleResponses(message):
    for i in range(len(responses)):
        response = responses[i].split('<>')
        words = response[0].split('__')
        for j in range(len(words)):
            if words[j] in message.content.lower():  # using full so it ignores spaces for yu huh, etc
                if str(message.author.id) in response[1].split('__') or response[1] == "all":
                    if random.random() < float(response[2]):
                        answers = response[3].split('__')
                        await send(message.channel, random.choice(answers))

async def HandleCounters(message):
    phraseCounterDefinitions = open(os.path.join(os.getcwd(), "phraseCounterDefinitions.txt"), "r")
    phraseCounters = phraseCounterDefinitions.readlines()
    phraseCounterDefinitions.close()
    
    if os.path.exists(os.path.join(os.getcwd(),"local/phraseCounters.txt")):
        phraseCountFile = open(os.path.join(os.getcwd(),"local/phraseCounters.txt"), "r")
        currentCounts = phraseCountFile.read()
        phraseCountFile.close()
    else:
        currentCounts = ""
    
    text = ""
    
    for phrase in phraseCounters:
        phrase = phrase.strip().replace("\n", "")
        if phrase == "":
            continue
        if phrase.split('-')[1] in message.content.lower() and phrase.split('-')[0] == str(message.author.id):
            #print(phrase.split('-')[0] + " said " + phrase.split('-')[1])
            pattern = phrase + "\|(.+)\n"
            match = regex.search(pattern, currentCounts)
            if bool(match):
                text += phrase + "|" + str(message.content.lower().count(phrase.split('-')[1]) + int(match.group(1))) + "\n"
            else:
                text += phrase + "|" + str(message.content.lower().count(phrase.split('-')[1])) + "\n"
        else:
            try:
                pattern = phrase + "\|(.+)\n"
                match = regex.search(pattern, currentCounts)
                text += match.group(0)
            except:
                text += phrase + "|0\n"
    
    phraseCountFile = open(os.path.join(os.getcwd(),"local/phraseCounters.txt"), "w") 
    phraseCountFile.write(text)
    phraseCountFile.close()

def GetName(id):
    file = open(os.path.join(os.getcwd(), "idNameConversion.txt"))
    text = file.read()
    file.close()
    
    pattern = str(id) + "-(.+)\n"
    #print(pattern)
    #print(text)
    match = regex.search(pattern, text)
    return match.group(1)

client.run(token)

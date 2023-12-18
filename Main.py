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

responsesFile = open(os.path.join(os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))), "responses.txt"), "r")
responses = responsesFile.readlines()
responsesFile.close()

print(responses)

stored_file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "NamesCount.txt")  # i think just "NamesCount.txt" should work, im not sure what prompted this

@client.event
async def on_ready():  # executed on bot setup
    print("logged in as {0.user}".format(client))
    get_names()
    await client.wait_until_ready()
    channel = client.get_channel(1181162678740324392)
    await channel.send("John's Assistant up and running.")
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
        for j in range(len(responses[i].split('<>')[0].split('//'))):
            print("Checking " + responses[i].split('<>')[0].split('//')[j])
            if responses[i].split('<>')[0].split('//')[j] in message_contents:
                print("Found " + responses[i].split('<>')[0].split('//')[j] + " in message.")
                if str(message.author.id) in responses[i].split('<>')[1].split('//'):
                    print("Correct id.")
                    if random.random() < responses[i].split('<>')[2]:
                        answers = responses[i].split('<>')[3].split('//')
                        await message.channel.send(random.choice(answers))

    rand_num = random.randrange(0, 500)

    # random responses
    if rand_num == 69:
        await message.channel.send("kill yourself - wiktor")

    if message_count == 15:  # not necessary now, might remove, or make it random
        message_count = 0
        save_names(["ash"], [ash_count])
        print("names saved")
    
    FuF = ["fucku", "fuckyou"]

    # responses
    if message_contents in FuF:
        await message.channel.send("not if i fuck you first")
        print("successfully fucked")
    elif message_contents == "kys":
        await message.channel.send("awww keep yourself safe so sweet")
    elif "good morning" in message_contents:
        await message.channel.send("go die")

    # activities
    elif "-hungergames" == message_contents[:12]:
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

    # id specific messages
    elif message.author.id == ids["isaac"] and "ash" in message_contents_full:  # using message_contens_full, because he could say 'a sheep' for example
        ash_count+=1
        ashResponses = [
            "such a fucking simp",
            "bUt ShE's So PrEtTy stfu",
            "she don't love you little bro",
            "unbelivably down bad"
        ]
        await message.channel.send(random.choice(ashResponses))
    elif message.author.id != ids["lauren"] and message_contents == "-summon isaac":  # heheheha
        print("summoning isaac")
        await message.channel.send("<@386783880637579286> <@386783880637579286> <@386783880637579286> <@386783880637579286> <@386783880637579286>")

    # displaying counters
    elif message_contents == "-update":  # this could be removed
        message_count = 0
        save_names(["ash"], [ash_count])
        print("names saved")
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

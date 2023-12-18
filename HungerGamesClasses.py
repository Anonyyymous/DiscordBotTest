from dataclasses import dataclass
from HungerGamesData import *
import random

@dataclass
class Player:
    name: str
    damage: int = 1
    kills: int = 0
    environment: str = "planes"
    round_lasted: int = 0

    def __init__(self, name):
        self.name = name


# environments = (0: planes, 1: swamp, 2:volcano)
@dataclass
class GameManager:
    # round 1
    environment_chance: float = 0.3
    round_1_death_chance: float = 0.4

    # extra rounds
    action_chance: float = 0.4  # 
    fight_chance: float = 0.9  # chance the player will die
    suicide_chance: float = 0.2  # chance that the dying player wasnt killed by someone else
    migration_chance: float = 0.5

    # extra stuff
    damage_range: int = 6

    def __init__(self, player_list) -> None:
        self.players = []
        for arg in player_list:
            self.players.append(Player(arg))
        self.environments = {"planes": [], "swamp": [], "volcano": []}  # one nested list for each environment
        self.round = 0
        self.dead_players = []
        print("game set up")

    def rand_from_list(self, list):
        '''
        Returns a random value between 0 and list length
        '''
        return random.randint(0, len(list)-1)
    
    def rand_value_from_list(self, list):
        '''
        Returns a random value from the list
        '''
        return random.choice(list)
        # return list[self.rand_from_list(list)]
    
    def random_chance(self, chance):
        '''
        Takes a decimal chance, generates a random number between 0 and 1, and returns true if the chance is greater than the random value.
        If our chance was 0.4, and we got .3, this would be false, but if we got .6, this would be true.
        '''
        return random.uniform(0, 1) < chance
    
    def get_kill(self, environment, players):
        '''
        Gets a way of death for a player in their environment
        '''
        players -= 1  # so it works with the list
        if players == 0:
            deaths = environments[environment]["deaths"][0]
            return self.rand_value_from_list(deaths)
        
        if self.random_chance(self.environment_chance):
            deaths = environments[environment]["deaths"][players]  # this may not increment the kills, idrk
            return self.rand_value_from_list(deaths)
        return self.rand_value_from_list(pvps)
    
    def remove_player(self, player):
        self.players.remove(player)
        environments[player.environment]["players"].remove(player)
        player.round_lasted = self.round
        self.dead_players.append(player)

    def environmental_kill(self, victim):
        self.remove_player(victim)

        return self.get_kill(victim.environment, 1).replace("(v)", victim.name) + "\n"
    
    def kill_player(self, victim, killer):
        '''
        Returns the method of death of a player to a killer, and removes the victim from the lists, also incrementing the killer's kills
        '''
        if victim == killer:
            return ""
        self.remove_player(victim)
        method = self.get_kill(victim.environment, 2)
        killer.kills += 1
        return method.replace("(k)", killer.name).replace("(v)", victim.name) + "\n"

    def play_round_one(self):  # only kills
        '''
        Simulates round 1 of the games, which has slightly different probabilities.
        '''
        output_string = "Welcome to the hunger games\n"
        environments["planes"]["players"] = [x for x in self.players]  # send them all to the planes, cannot
        # print(environments["planes"]["players"])
        players_killed = random.randint(1, int(len(self.players)/2))  # maybe set a limit, but doing math.min on players killed and a limit?
        for i in range(players_killed):
            player = self.players[self.rand_from_list(self.players)]  # player to be killed
            if self.random_chance(self.round_1_death_chance):
                method = self.environmental_kill(player)
                output_string += method#.replace("(p1)", player.name) + "\n"
            else:
                killer = self.players[self.rand_from_list(self.players)]
                method = self.kill_player(player, killer)
                # print(method + f"|{killer}|{player}")
                output_string += method  # self.kill_player(killer, player)
            

        output_string += self.migrate_players()
        
        self.round += 1
        return output_string, True
    
    def migrate_players(self):
        '''
        Loops through players, if they get lucky, they migrate - changing their current environment
        Then removes player from old environment, adds them to new ones
        '''
        output_string = ""
        for player in self.players:
            if self.random_chance(self.migration_chance):
                prev_env = player.environment
                player.environment = self.rand_value_from_list(possible_environments)

                if prev_env != player.environment:
                    # if player in environments[player.environment]["players"]:  # this wont be the case in the first round
                    environments[prev_env]["players"].remove(player)
                    environments[player.environment]["players"].append(player)
                    output_string += f"\n{player.name} moved to the {player.environment}"
                else:
                    output_string += f"\n{player.name} stayed in the planes"
            else:  # put them in the planes
                # environments[player.environment]["players"].append(player)  # defaults to planes
                output_string += f"\n{player.name} stayed in the {player.environment}"

        return output_string

    def move_to_planes(self):  # a modified version of migrate
        '''
        Moves all players to planes so the last few will actually fight
        '''
        output_string = ""
        for player in self.players:
            if player.environment == "planes":
                output_string += f"\n{player.name} stayed in the planes"
            else:
                output_string += f"\n{player.name} moved to the planes"
                environments[player.environment]["players"].remove(player)
                player.environment = "planes"
                environments["planes"]["players"].append(player)

        return output_string
    
    def fight_players(self, player1, player2):
        '''
        Returns the winner and loser of a battle, in that order
        '''
        player1_score = player1.damage + random.randint(0, self.damage_range)
        player2_score = player2.damage + random.randint(0, self.damage_range)
        if player1_score > player2_score:
            return player1, player2
        return player2, player1

    def declare_winner(self):
        '''
        Returns the winner of a games in a formatted string, to be returned straight away from play_round()
        '''
        output_string = ""
        winner = self.players[0]
        output_string += f"\n\n{winner.name} won the game with {winner.kills} kills"
        for player in self.dead_players:
            output_string += f"\n{player.name} got {player.kills} kills, and died in round {player.round_lasted}"
        return output_string, False

    def play_round(self):
        '''
        Returns a string to print, based on results of one round. Probabilities are slightly different on the first round.
        '''
        if self.round == 0:
            return self.play_round_one()# + self.get_summary()

        if len(self.players) == 1:
            return self.declare_winner()

        output_string = f"round {self.round}\n"

        if len(self.players) == 2:  # 2 players left, so fight them
            player = self.rand_value_from_list(environments["planes"]["players"])  # players should be in the planes
            player2 = [x for x in self.players if x != player][0]  # just gets the other player
            output_string += self.kill_player(player, player2)
        else:
            for envrionment in environments:  # all of this should really go into a function, there is way too much indentation
                env = environments[envrionment]
                if len(env["players"]) <= 0:  # if no one is there
                    pass
                else:  # are 1+ players in the same environment
                    loops = len(env["players"]) - 1
                    for p in range(loops):  # does things once for each player, not per player
                        player = self.rand_value_from_list(env["players"])
                        if self.random_chance(self.action_chance):  # 
                            action = self.rand_value_from_list(actions)
                            player.damage += action[1]
                            output_string += action[0].replace("(v)", player.name) + "\n"
                        # if self.random_chance(self.death_chance):
                        elif self.random_chance(self.fight_chance) and len(env["players"]) > 1:
                            # player1 = self.rand_value_from_list(env["players"])
                            player2 = self.rand_value_from_list(env["players"])
                            if player != player2:
                                loser, winner = self.fight_players(player, player2)
                                output_string += self.kill_player(winner, loser)
                                # env["players"].remove(loser)

                        elif self.random_chance(self.suicide_chance):
                            method = self.environmental_kill(player)
                            output_string += method#.replace("(p1)", player.name) + "\n"
        #if len(self.players) == 1:
            #return self.declare_winner()
        if len(self.players) < 4:
            output_string += self.move_to_planes()
        else:
            output_string += self.migrate_players()
        self.round += 1
        return output_string, True# + self.get_summary()
                    

def clean_input_for_games(inp):
    '''
    Converts input string to list of players to play the game with
    '''
    list = inp.split("|")
    players = list[1:]
    return players
        

# below code is for testing. If not commented out, the rest of the code wont run, due to the input("--") line
'''test_players = ["John", "Beth", "Sofi", "Chris", "Chloe", "Ossian", "Tom"]
gm = GameManager(test_players)
for i in range(10):
    output, continue_playing = gm.play_round()
    print(output)
    if not continue_playing:
        break
    input("-----------------------------------------------")'''
# print(test_players[1:])
        

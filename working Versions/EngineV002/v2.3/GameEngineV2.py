import random
import json

#stopped here

class GameEngine:
    def __init__(self):
        self.activePlayer = False
        self.game_statusID = 1 # Set initial gamestatusID
        self.counter_fight = 0
        self.counter_friendship = 0
        self.counter_hide = 0
        self.counter_run = 0
        self.playerData = {}
        self.turncounter = 0

          
    
    def initialize_game(self):
        num_players = input("Enter the number of players (1 to 5) or enter 'q' to quit: ")
        if num_players == 'q':
            self.game_statusID = 0  # Update the instance variable
            return self.game_statusID
        try:
            num_players = int(num_players)
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 5 or enter 'q' to quit.")
            return None
        if 1 <= num_players <= 5:
            self.playerData = {}  # Use the instance variable
            for playerID in range(1, num_players + 1):
                self.playerData["player " + str(playerID)] = {
                    'playerID': playerID,
                    'actioncards': {},
                    'actioncards_played': 0,
                    'endurance': 15,
                    'activePlayer': False
                }

            if "player 1" in self.playerData:
                self.playerData["player 1"]["activePlayer"] = True
            with open("playerdata.json", "w") as json_file:
                json.dump(self.playerData, json_file, indent=4)
            print("Updated 'activePlayer' status for player 1 to True.")
            print("Player information saved to 'playerdata.json'.")
            
            with open("playerData.json", "r") as json_file:
                playerData = json.load(json_file)
                for key,value in playerData.items():
                    print(key, value)
        else:
            print("Invalid input. Please enter a number between 1 and 5 or enter 'q' to quit.")
            return None


    
    def deal_6_cards_perplayer(self):
        # Load player data from JSON file
        with open("playerData.json", "r") as json_file:
            self.playerData = json.load(json_file)
    
        possible_entries = ["fight", "friendship", "run", "hide", "joker"]
        for player_key, player_attributes in self.playerData.items():
            if player_key in self.playerData:    
                list_actioncards = [random.choice(possible_entries) for _ in range(6)]
                list_actioncards.sort()
                actioncards = {entry: list_actioncards.count(entry) for entry in possible_entries}
            self.playerData[player_key]["actioncards"] = actioncards
            print(f"player {player_key} action cards:", actioncards)
        # Save the updated player data to the JSON file
        with open("playerdata.json", "w") as json_file:
            json.dump(self.playerData, json_file, indent=4)
        with open("playerData.json", "r") as json_file:
            playerData = json.load(json_file)
            for key,value in self.playerData.items():
                print(key, value)       
           
    def update_gamestate(self, gamelevel, turncounter, activePlayer, actioncards_played):
        if self.actioncards_played >= 2:
            self.turncounter += 1
            self.actioncards_played = 0
            print(f"level: {gamelevel} | turn: {turncounter}")
            return(turncounter, actioncards_played)
        
    def get_activePlayer_playerKey(self):
        with open("playerData.json", "r") as json_file:
            playerData = json.load(json_file)
            for playerKey, playerAttributes in playerData.items():
                if playerAttributes["activePlayer"] == True: 
                    print(f"get_activePlayer_playerKey: Active player found. Playerkey: {playerKey}")
                    return(playerKey)              


    def lose_actioncard_fight(self):
        activePlayer_playerKey = self.get_activePlayer_playerKey()
        with open("playerData.json", "r") as json_file:
            playerData_in_json = json.load(json_file)
            if activePlayer_playerKey in playerData_in_json:
                fight_value = playerData_in_json[activePlayer_playerKey]["actioncards"]["fight"]
                print(f"lose_actioncard_fight: This is the number of 'fight' cards for {activePlayer_playerKey}: {fight_value}")
                if fight_value > 0:  # Check if there are "fight" cards to lose
                    fight_value -= 1  # Decrement the count by 1
                    playerData_in_json[activePlayer_playerKey]["actioncards"]["fight"] = fight_value  # Update the JSON data
                    with open("playerData.json", "w") as json_file:
                        json.dump(playerData_in_json, json_file, indent=4)  # Save the updated JSON data
                    print(f"Lose_actioncard_fight: 'fight' card count decreased for {activePlayer_playerKey}.")
                else:
                    print(f"Lose_actioncard_fight: No 'fight' cards left for {activePlayer_playerKey}.")
            else:
                print(f"Lose_actioncard_fight: Player {activePlayer_playerKey} not found in playerData.json.")


                    
    def run_level_loop(self):
        self.activePlayer = self.get_activePlayer_playerKey()
        user_input = input(f"\nPlayer {self.activePlayer}, enter a command (enter 'quit' or 'q' to exit): ")
        if user_input.lower() == "quit" or user_input.lower() == "q":
            print("Exiting the program...")
            self.game_statusID = 0
            return(self.game_statusID)
        elif user_input.lower() == "fight" or user_input.lower() == "f":
            print("executing lose_actioncard_fight")
            self.lose_actioncard_fight()

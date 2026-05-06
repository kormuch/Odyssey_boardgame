import random
import json


class GameEngine:
    def __init__(self):
        self.active_player = 0
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
                    'active_Player': False
                }

            if "player 1" in self.playerData:
                self.playerData["player 1"]["active_Player"] = True
            with open("playerdata.json", "w") as json_file:
                json.dump(self.playerData, json_file, indent=4)
            print("Updated 'active_Player' status for player 1 to True.")
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
           
    def update_gamestate(self, gamelevel, turncounter, active_player, actioncards_played):
        if self.actioncards_played >= 2:
            self.turncounter += 1
            self.actioncards_played = 0
            print(f"level: {gamelevel} | turn: {turncounter}")
            return(turncounter, actioncards_played)
        
    def get_activePlayer_playerID(self):
        with open("playerData.json", "r") as json_file:
            playerData = json.load(json_file)
            for player, playerAttributes in playerData.items():
                if playerAttributes["active_Player"] == True: 
                    print(f"Active player found. PlayerID: {playerAttributes['playerID']}")
                    return(playerAttributes['playerID']) # playerID is an integer
                    
 
    def run_level_loop(self):
        self.active_player = self.get_activePlayer_playerID()
        user_input = input(f"\nPlayer {self.active_player}, enter a command (enter 'quit' or 'q' to exit): ")
        self.game_statusID = 0
        return(self.game_statusID)
        
'''        
    def run_level_loop(self):
        active_player = 0  # Initialize with the first player
        while self.gamestatus != 0:
            user_input = input(f"\nPlayer {active_player + 1}, enter a command (enter 'quit' or 'q' to exit): ")
            if user_input.lower() == "quit" or user_input.lower() == "q":
                print("Exiting the program...")
                self.gamestatus = 0
                return self.gamestatus
            elif user_input.lower() == "joker" or user_input.lower() == "0":
                if self.actioncards["joker"] > 0:
                    user_input_joker = input("\nYou used a Joker. Enter an action (enter 'quit' or 'q' to exit): ")
                    if self.players[f"player_{active_player + 1}"].play_action_card(user_input_joker):
                        self.process_input(user_input_joker)
                else:
                    print('no joker available')
            elif user_input.lower() in ["fight", "1", "friendship", "2", "hide", "3", "run", "4"]:
                if self.players[f"player_{active_player + 1}"].play_action_card(user_input):
                    self.process_input(user_input)
            
            # Move to the next player's turn
            active_player = (active_player + 1) % len(self.players)
'''
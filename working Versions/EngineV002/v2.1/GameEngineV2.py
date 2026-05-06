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
        else:
            print("Invalid input. Please enter a number between 1 and 5 or enter 'q' to quit.")
            return None
    

        
        




    
    def deal_6_cards_perplayer(self):
        # Load player data from JSON file
        with open("playerData.json", "r") as json_file:
            playerData = json.load(json_file)
    
        possible_entries = ["fight", "friendship", "run", "hide", "joker"]
        for player_key, player_attributes in playerData.items():
    
            # Update player's action cards played count if needed
            if player_key in playerData:    
                # Generate new action cards
                list_actioncards = [random.choice(possible_entries) for _ in range(6)]
                list_actioncards.sort()
                actioncards = {entry: list_actioncards.count(entry) for entry in possible_entries}
    
            # Update self.playerData with the new action cards information
            playerData[player_key]["actioncards"] = actioncards
    
            # Print the player's action cards
            print(f"player {player_key} action cards:", actioncards)
    
        # Save the updated player data to the JSON file
        with open("playerdata.json", "w") as json_file:
            json.dump(self.playerData, json_file, indent=4)
    
    
    def load_playerData(self):
        try:
            with open("playerData.json", "r") as json_file:
                playerData = json.load(json_file)
                print("loaded playerData")
        except:
            EOFError
            print("An Error occured. Unable to load playerData.json.")
            pass
        
    def check_gamestate(self, gamelevel, turncounter, actioncards_played):
        if actioncards_played >= 2:
            turncounter += 1
            actioncards_played = 0
            print(f"level: {gamelevel} | turn: {turncounter}")
            return(turncounter, actioncards_played)
        
    def run_level_loop():
        get_activePlayer()
        input(f"\nPlayer {active_player + 1}, enter a command (enter 'quit' or 'q' to exit): ")
        
           
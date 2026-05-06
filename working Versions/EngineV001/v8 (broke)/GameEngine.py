from Player import Player
import random
import json



class GameEngine:
    def __init__(self):
        self.actioncards = {
            "joker": 0,
            "fight": 0,
            "friendship": 0,
            "hide": 0,
            "run": 0
        }
        self.actioncards_played = {}  # Initialize as an empty dictionary

        # Load player data from JSON file to populate the actioncards_played dictionary
        with open("playerdata.json", "r") as json_file:
            player_data = json.load(json_file)
            self.actioncards_played = {
                player_key: player_data[player_key]["actioncards_played"] for player_key in player_data
            }
        
        self.counter_fight = 0
        self.counter_friendship = 0
        self.counter_hide = 0
        self.counter_run = 0
        self.gamestatus = 1  # Set initial gamestatus
        self.players = {}
        self.player_data = {}
        self.turncounter = 0
 

    def check_gamestate(self, gamelevel, turncounter, actioncards_played):
        if actioncards_played >= 2:
            turncounter += 1
            actioncards_played = 0
            print(f"level: {gamelevel} | turn: {turncounter}")
            return(turncounter, actioncards_played)
        
    def initialize_game(self):
        num_players = int(input("Enter the number of players (1 to 5) or enter 'q' to quit: "))
        if 1 <= num_players <= 5:
            players = {f"player_{player_number}": Player(player_number) for player_number in range(1, num_players + 1)}
            player_data = {
                player_key: {
                    "playerNumber": player.playerNumber,
                    "actioncards": player.actioncards,
                    "actioncards_played": player.actioncards_played,
                    "damageSuffered_player": player.damageSuffered_player
                }
                for player_key, player in players.items()
            }
            with open("playerdata.json", "w") as json_file:
                json.dump(player_data, json_file, indent=4)
                self.actioncards_played = {
                player_key: player_data[player_key]["actioncards_played"] for player_key in player_data
            }    
            print("Player information saved to 'playerdata.json'.")
            self.player_data = player_data  # Store player data in the attribute
            return players
        elif num_players == 'q':
            return None
        else:
            print("Invalid input. Please enter a number between 1 and 5 or enter 'q' to quit: ")
            return {}


    





    
    def run_level_loop(self):
        active_player = 0
        actioncards_played_this_turn = 0
        while self.gamestatus != 0:
            user_input = input(f"\nPlayer {active_player + 1}, enter a command (enter 'quit' or 'q' to exit): ")
            
            if user_input.lower() in ["quit", "q"]:  # Add an exit condition here
                print("Exiting the game...")
                self.gamestatus=0

            
            if user_input.lower() in ["fight", "1", "friendship", "2", "hide", "3", "run", "4"]:
                if self.process_input(user_input, active_player):
                    actioncards_played_this_turn += 1
    
                    if actioncards_played_this_turn >= 2:
                        self.actioncards_played[f"player_{active_player + 1}"] += 2
                        active_player = (active_player + 1) % len(self.players)
                        actioncards_played_this_turn = 0
    
        # Save updated actioncards_played to the JSON file after the game loop
        with open("playerdata.json", "w") as json_file:
            json.dump(self.player_data, json_file, indent=4)
    
        with open("actioncards_played.json", "w") as json_file:
            json.dump(self.actioncards_played, json_file, indent=4)


            
    def process_input(self, user_input, active_player):
        action_mapping = {
            "fight": "fight",
            "1": "fight",
            "friendship": "friendship",
            "2": "friendship",
            "hide": "hide",
            "3": "hide",
            "run": "run",
            "4": "run"
        }

        action_type = action_mapping.get(user_input.lower())
        if action_type:
            if action_type == "joker":
                self.actioncards["joker"] -= 1

            # Check if the action type is a valid action card
            if action_type in ["fight", "friendship", "hide", "run"]:
                counter = self.handle_actions(action_type)
                print(f"{action_type.capitalize()} Counter:", counter)
            else:
                print("Invalid input. Please enter a valid action.")
        else:
            print("Invalid input. Please enter a valid action.")


            
    def handle_actions(self, event_type):
        if event_type == "fight":
            self.counter_fight += 1
            return self.counter_fight
        elif event_type == "friendship":
            self.counter_friendship += 1
            return self.counter_friendship
        elif event_type == "hide":
            self.counter_hide += 1
            return self.counter_hide
        elif event_type == "run":
            self.counter_run += 1
            return self.counter_run
        
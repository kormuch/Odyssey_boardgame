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
        self.counter_fight = 0
        self.counter_friendship = 0
        self.counter_hide = 0
        self.counter_run = 0
        self.gamestatus = 1  # Set initial gamestatus
        self.players = {}
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
            
            possible_entries = ["fight", "friendship", "run", "hide", "joker"]
            for player_key, player in players.items():
                list_actioncards = [random.choice(possible_entries) for _ in range(6)]
                list_actioncards.sort()
                player.actioncards = {entry: list_actioncards.count(entry) for entry in possible_entries}
            
            # Save player information to a JSON file
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
            print("Player information saved to 'playerdata.json'.")
            return players
        elif num_players == 'q':
            return None
        else:
            print("Invalid input. Please enter a number between 1 and 5 or enter 'q' to quit: ")
            return {}

    
    def deal_6_cards_perplayer(self):
        # Load player data from JSON file
        with open("playerdata.json", "r") as json_file:
            player_data = json.load(json_file)
    
        possible_entries = ["fight", "friendship", "run", "hide", "joker"]
        for player_key, player_attributes in player_data.items():
            player = Player(player_attributes["playerNumber"])
    
            list_actioncards = [random.choice(possible_entries) for _ in range(6)]
            list_actioncards.sort()
            player.actioncards = {entry: list_actioncards.count(entry) for entry in possible_entries}
    
            # Print the player's action cards
            print(f"{player_key} action cards:", player.actioncards)
            self.players[player_key] = player  # Store player in the dictionary of players


    
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
                    self.process_input(user_input_joker)
                else:
                    print('no joker available')
            elif user_input.lower() in ["fight", "1", "friendship", "2", "hide", "3", "run", "4"]:
                self.process_input(user_input)
            
            # Move to the next player's turn
            active_player = (active_player + 1) % len(self.players)

            
    def process_input(self, user_input):
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
            counter = self.handle_actions(action_type)
            print(f"{action_type.capitalize()} Counter:", counter)
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

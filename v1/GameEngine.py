from PlayerData import Player
import random

class GameEngine:
    def __init__(self, gamestatus, players):
        self.actioncards = {
        "joker": 0,
        "fight": 0,
        "friendship": 0,
        "hide": 0,
        "run": 0
    }
        self.counter_fight_path = 0
        self.counter_friendship_path = 0
        self.counter_hide_path = 0
        self.counter_run_path = 0
        self.gamelevel = 0
        self.gamestatus = gamestatus
        self.players = players
        self.turncounter = 0
 
    def handle_actions(self, event_type):
        if event_type == "fight":
            self.counter_fight_path += 1
            return self.counter_fight_path
        elif event_type == "friendship":
            self.counter_friendship_path += 1
            return self.counter_friendship_path
        elif event_type == "hide":
            self.counter_hide_path += 1
            return self.counter_hide_path
        elif event_type == "run":
            self.counter_run_path += 1
            return self.counter_run_path
    def check_gamestate(self, gamelevel, turncounter, actioncards_played):
        if actioncards_played >= 2:
            turncounter += 1
            actioncards_played = 0
            print(f"level: {gamelevel} | turn: {turncounter}")
            return(turncounter, actioncards_played)
    def setup_lvl_0(self):
        possible_entries = ["fight", "friendship", "run", "hide", "joker"]
        for player in self.players:
            list_actioncards = [random.choice(possible_entries) for _ in range(6)]
            list_actioncards.sort()
            player.actioncards = {entry: list_actioncards.count(entry) for entry in possible_entries}

            # Print the player's action cards
            print(f"Player {player.playerNumber} action cards:", player.actioncards)
    def setup_lvl_1(self):
        return
    
    def run_game_loop(self):
        while self.gamestatus != 0:
            user_input = input("\nEnter a command (enter 'quit' or 'q' to exit): ")
            if user_input.lower() == "quit" or user_input.lower() == "q":
                print("Exiting the program...")
                self.gamestatus = 0
                return(self.gamestatus)
            elif user_input.lower() == "joker" or user_input.lower() == "0":
                if self.actioncards["joker"] > 0:
                    user_input_joker = input("\nYou used a Joker. Enter an action (enter 'quit' or 'q' to exit): ")
                    self.process_action(user_input_joker)
                else:
                    print('no joker available')
            elif user_input.lower() in ["fight", "1", "friendship", "2", "hide", "3", "run", "4"]:
                self.process_action(user_input)

    def process_action(self, user_input):
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
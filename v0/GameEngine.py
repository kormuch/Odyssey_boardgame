from PlayerData import Player
import random

class GameEngine:
    def __init__(self):
        self.counter_fight_path = 0
        self.counter_friendship_path = 0
        self.counter_hide_path = 0
        self.counter_run_path = 0
        self.gamelevel = 0
        self.turncounter = 0
        self.actioncards = {}
 
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
        for player in players:
            list_actioncards = [random.choice(possible_entries) for _ in range(6)]
            list_actioncards.sort()
            player.actioncards = {entry: list_actioncards.count(entry) for entry in possible_entries}

            # Print the player's action cards
            print(f"Player {player.playerNumber} action cards:", player.actioncards)
    def setup_lvl_1(self):
        return
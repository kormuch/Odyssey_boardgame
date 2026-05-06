import random
import json
from itertools import chain

#stopped here

class GameEngine:
    def __init__(self):
        self.actionDictionary = {"artisanship": ["artisanship", "a"],
                                 "battle": ["battle", "b"],
                                 "fellowship": ["fellowship", "f"],
                                 "joker": ["joker"],
                                 "journey":["journey", "j"]}
        self.tuple_possibleActions = tuple(chain.from_iterable(self.actionDictionary.values()))
        self.activePlayer = False
        self.game_statusID = 1 # Set initial gamestatusID
        self.currentActionKey = self.load_current_actionKey_from_gamestateJson()
        self.counter_battle = 0
        self.counter_fellowship = 0
        self.counter_artisanship = 0
        self.counter_journey = 0
        self.playerData = {}
        self.turncounter = 0
 
    
    
    def initialize_game(self):
        print("initialize_game executed")
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
        print("deal_6_cards_perplayer executed")
        with open("playerData.json", "r") as json_file:
            self.playerData = json.load(json_file)
        possible_entries = ["battle", "fellowship", "journey", "artisanship", "joker"]
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
            self.playerData = json.load(json_file)
            for key,value in self.playerData.items():
                print(key, value)       
           
    def update_gamestate(self, game_statusID, turncounter, activePlayer, actioncards_played):
        print("update_gamestate executed")
        if self.actioncards_played >= 2:
            self.turncounter += 1
            self.actioncards_played = 0
            print(f"level: {game_statusID} | turn: {turncounter}")
            return(turncounter, actioncards_played)
        
    def get_activePlayer_playerKey(self):
        print("get_activePlayer_playerKey executed")
        with open("playerData.json", "r") as json_file:
            playerData = json.load(json_file)
            for playerKey, playerAttributes in playerData.items():
                if playerAttributes["activePlayer"] == True: 
                    print(f"get_activePlayer_playerKey: Active player found. Playerkey: {playerKey}")
                    return(playerKey)              


    def get_actionKey_from_userInput(self):
        print("get_actionKey_from_userInput executed")
        print(f"possible actionkeywords: {self.tuple_possibleActions}")
        self.activePlayer = self.get_activePlayer_playerKey()
        user_input = input(f"\nPlayer {self.activePlayer}, enter a command (enter 'quit' or 'q' to exit): ")
        print(user_input)
        
        if user_input.lower() == "quit" or user_input.lower() == "q":
            print("Exiting the program...")
            self.game_statusID = 0
            return self.game_statusID
    
        elif user_input.lower() in self.tuple_possibleActions:
            for actionKey, list_actions in self.actionDictionary.items():
                for action in list_actions:
                    if user_input.lower() in list_actions:
                        print(f"user_input match: '{user_input}' found in '{actionKey}'")
                        print(f"returning actionKey '{actionKey}'")
    
                        # Save actionKey to "gamestate" JSON file
                        gamestate_data = {}
                        gamestate_data["currentActionKey"] = actionKey
    
                        with open("gamestate.json", "w") as file:
                            json.dump(gamestate_data, file, indent=4)
    
                        # Store the entry in a dictionary
                        return actionKey
        else:
            print("User input invalid.")                    

        
    def lose_actioncard(self):
        print("lose_actioncard executed")
        activePlayer_playerKey = self.get_activePlayer_playerKey()
        actionKey = self.get_actionKey_from_userInput()
        with open("playerData.json", "r") as json_file:
            playerData_in_json = json.load(json_file)
            if activePlayer_playerKey in playerData_in_json:
                actioncard_value = playerData_in_json[activePlayer_playerKey]["actioncards"][actionKey]
                if actioncard_value > 0:  # Check if there are action cards to lose
                    actioncard_value-= 1  # Decrement the count by 1
                    playerData_in_json[activePlayer_playerKey]["actioncards"][actionKey] = actioncard_value  # Update the JSON data
                    with open("playerData.json", "w") as json_file:
                        json.dump(playerData_in_json, json_file, indent=4)  # Save the updated JSON data
                    print(f"lose_actioncard: {actionKey} card count decreased for {activePlayer_playerKey}, new {actionKey} card value: {actionKey}.")
                else:
                    print(f"lose_actioncard: No {actionKey} cards left for {activePlayer_playerKey}.")
            else:
                print(f"lose_actioncard: Player {activePlayer_playerKey} not found in playerData.json.")



    def load_current_actionKey_from_gamestateJson(self):
        with open("gamestate.json", "r") as file:
            data = json.load(file)
            current_action_key = data["currentActionKey"]
            return(current_action_key)
            
            
    def run_level_loop(self):
        print("\nrun_level_loop executed")
        self.get_actionKey_from_userInput()
            
            
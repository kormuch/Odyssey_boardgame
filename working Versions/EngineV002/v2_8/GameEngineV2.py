import random
import json
from itertools import chain

#stopped here

class GameEngine:
    def __init__(self, actioncards_played, activePlayerID, currentActionKey, 
                 counter_battle, counter_craftsmanship, counter_fellowship,
                 counter_journey, counter_userinput_execution, game_statusID, playerData,
                 possibleActions_tuple, roundcounter):
        self.actionDictionary = {"battle": ["battle", "b"],
                                 "craftsmanship": ["craftsmanship", "c"],
                                 "fellowship": ["fellowship", "f"],
                                 "joker": ["joker"],
                                 "journey":["journey", "j"]}
        self.actioncards_played = 0
        self.activePlayerID = 0
        self.currentActionKey = ""
        self.counter_battle = 0
        self.counter_craftsmanship = 0
        self.counter_fellowship = 0
        self.counter_journey = 0
        self.counter_userinput_execution = 0
        self.game_statusID = 1 # Set initial gamestatusID
        self.numberOfPlayers = 0
        self.playerData = {}
        self.possibleActions_tuple = tuple(chain.from_iterable(self.actionDictionary.values()))
        self.roundcounter = 0

 
    
    
    def initialize_game(self):
        print("initialize_game executed")
        num_players = input("Enter the number of players (1 to 5) or enter 'q' to quit: ")
        if num_players == 'q':
            self.game_statusID = 0  # Update the instance variable
            return (self.game_statusID)
        try:
            num_players = int(num_players)
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 5 or enter 'q' to quit.")
            return None
        if 1 <= num_players <= 5:
            self.numberOfPlayers = num_players
            self.activePlayerID = 1
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
            return(self.activePlayerID, self.numberOfPlayers, self.playerData)
        else:
            print("Invalid input. Please enter a number between 1 and 5 or enter 'q' to quit.")
            return None


    
    def deal_6_cards_perplayer(self):
        print("deal_6_cards_perplayer executed")
        with open("playerData.json", "r") as json_file:
            self.playerData = json.load(json_file)
        possible_entries = ["battle", "fellowship", "journey", "craftsmanship", "joker"]
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
                   
    def get_activePlayer_playerKey(self):
        print("get_activePlayer_playerKey executed")
        activePlayer_playerKey = "Player " + str(self.activePlayerID)
        return(activePlayer_playerKey)
        
    def nextPlayer(self):
        self.activePlayerID = (self.activePlayerID + 1) % (self.numberOfPlayers + 1)
        if self.activePlayerID == 0:
            self.activePlayerID += 1
        return(self.activePlayerID)



    def get_actionKey_from_userInput(self):
        print("get_actionKey_from_userInput executed")
        print(f"game statusID: {self.game_statusID} | active player: {self.activePlayerID} | actionards played: {self.actioncards_played} | userinputcounter: {self.counter_userinput_execution}")
        print(f"possible actionkeywords: {self.possibleActions_tuple}")
        self.activePlayer = self.get_activePlayer_playerKey()
        user_input = input(f"Player {self.activePlayerID}, enter a command (enter 'quit' or 'q' to exit): ")
        print(user_input)
        
        if user_input.lower() == "quit" or user_input.lower() == "q":
            print("Exiting the program...")
            self.game_statusID = 0
            return (self.game_statusID)
        elif user_input.lower() == "skip" or user_input.lower() == "s":
            self.counter_userinput_execution += 1
            self.actioncards_played = 2
            return(self.actioncards_played, self.counter_userinput_execution)                
        elif user_input.lower() in self.possibleActions_tuple:
            self.counter_userinput_execution += 1
            self.actioncards_played += 1
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
                        return(actionKey)
        else:
            print("User input invalid.")                    

    def trigger_event(self):
        print("trigger_event executed")

        
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
        try:
            with open("gamestate.json", "r") as file:
                data = json.load(file)
                current_action_key = data["currentActionKey"]
                return current_action_key
        except FileNotFoundError:
            # Handle the case when the file "gamestate.json" is not found
            print("File 'gamestate.json' not found")
            return None
        except json.JSONDecodeError:
            # Handle the case when the JSON data is invalid
            print("Invalid JSON data in 'gamestate.json'")
            return None
            
            
    def run_level_loop(self):
        print("\nrun_level_loop executed")
        self.roundcounter += 1
        print(f"round: {self.roundcounter}")
        self.trigger_event()
        while self.actioncards_played < 2:
            self.get_actionKey_from_userInput()
            if self.game_statusID == 0:
                return (self.game_statusID)
        self.nextPlayer()
        self.actioncards_played = 0
        if self.roundcounter == 4:
            self.game_statusID = 0
            return(self.game_statusID)
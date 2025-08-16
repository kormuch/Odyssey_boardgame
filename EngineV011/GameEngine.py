import random
import json
from itertools import chain
import os

class ClassGameEngine:
    def __init__(self):
        self.actionpaths = {"battle": 0,
                            "craftsmanship": 0,
                            "fellowship": 0,
                            "journey": 0}
        self.actionDictionary = {"battle": {"keywords": ["battle", "b"], "effect": {"battle": 1}},
                                 "craftsmanship": {"keywords":["craftsmanship", "c"], "effect": {"craftsmanship": 1}},
                                 "fellowship": {"keywords": ["fellowship", "f"], "effect": {"fellowship": 1}},
                                 "joker": ["joker"],
                                 "journey": {"keywords": ["journey", "j"], "effect": {"journey": 1}},
                                 
                                 "2x battle": {"keywords": ["double battle", "bb"], "effect": {"battle": 2}}, 
                                 "2x craftsmanship": {"keywords": ["double craftsmanship", "cc"], "effect": {"craftsmanship": 2}},
                                 "2x fellowship": {"keywords": ["double fellowship", "ff"], "effect": {"fellowship": 2}},
                                 "2x joker": {"keywords": ["double joker"]},
                                 "2x journey": {"keywords": ["double journey", "jj"], "effect": {"journey": 2}}}
        self.actioncards_played = 0
        self.activePlayerID = 0
        self.currentActionKey = ""
        self.counter_userinput_execution = 0
        self.game_statusID = 1 # Set initial gamestatusID
        self.numberOfPlayers = 0
        self.playerData = {}
        self.possibleActionKeys_tuple = tuple(self.actionDictionary.keys())
        self.possibleActionValues_tuple = tuple(chain.from_iterable(action.get("keywords", []) if isinstance(action, dict) else action for action in self.actionDictionary.values()))
        self.roundcounter = 1
        self.userInput = ""    
    
    def initialize_game(self, num_players=1):
        print("initialize_game executed")
        
        # Use provided number of players instead of asking for input
        try:
            if isinstance(num_players, str):
                if num_players == 'q':
                    self.game_statusID = 0
                    return self.game_statusID
                num_players = int(num_players)
        except ValueError:
            print("Invalid input. Using default 2 players.")
            num_players = 2
            
        if 1 <= num_players <= 5:
            self.numberOfPlayers = num_players
            self.activePlayerID = 1
            
            # Initialize player data
            self.playerData = {}
            for playerID in range(1, num_players + 1):
                self.playerData["player " + str(playerID)] = {
                    'playerID': playerID,
                    'actioncards': {},
                    'actioncards_played': 0,
                    'endurance': 15,
                    'activePlayer': False
                }
            
            # Set first player as active
            self.playerData["player 1"]["activePlayer"] = True
            
            # Save player data safely
            try:
                with open("playerdata.json", "w") as json_file:
                    json.dump(self.playerData, json_file, indent=4)
                print("Player information saved to 'playerdata.json'.")
            except Exception as e:
                print(f"Warning: Could not save to file: {e}")
            
            print("Updated 'activePlayer' status for player 1 to True.")
            return num_players  # Return just the number of players for GUI compatibility
        else:
            print("Invalid input. Using default 2 players.")
            return self.initialize_game(2)  # Recursively call with default

    def deal_6_cards_perplayer(self):
        print("deal_6_cards_perplayer executed")
        
        # Make sure we have players initialized
        if not self.playerData:
            print("Warning: No players initialized. Initializing default game first.")
            self.initialize_game(2)
        
        possible_entries = self.possibleActionKeys_tuple[:5]
        
        for player_key, player_attributes in self.playerData.items():
            if player_key in self.playerData:    
                list_actioncards = [random.choice(possible_entries) for _ in range(6)]
                list_actioncards.sort()
                actioncards = {entry: list_actioncards.count(entry) for entry in possible_entries}
                self.playerData[player_key]["actioncards"] = actioncards
                print(f"player {player_key} action cards:", actioncards)
        
        # Save the updated player data to the JSON file safely
        try:
            with open("playerdata.json", "w") as json_file:
                json.dump(self.playerData, json_file, indent=4)
            
            # Read back the data (if file exists)
            if os.path.exists("playerdata.json"):
                with open("playerdata.json", "r") as json_file:
                    self.playerData = json.load(json_file)
                    for key, value in self.playerData.items():
                        print(key, value)
        except Exception as e:
            print(f"Warning: File operation failed: {e}")
        
        return "Cards dealt successfully"  # Return a result for GUI feedback
                   
    def get_activePlayer_playerKey(self):
        print("get_activePlayer_playerKey executed")
        activePlayer_playerKey = "player " + str(self.activePlayerID)
        return(activePlayer_playerKey)
        
    def nextPlayer(self):
        print("nextPlayer executed")
        self.activePlayerID = (self.activePlayerID + 1) % (self.numberOfPlayers + 1)
        if self.activePlayerID == 0:
            self.activePlayerID += 1
        return(self.activePlayerID)

    def userInput_prompt(self):
        """
        Modified for GUI compatibility - no more input() calls
        GUI will call this to get prompt text, then call process_user_input() with the result
        """
        print("userInput_prompt executed")
        prompt_text = f"game statusID: {self.game_statusID} | active player: {self.activePlayerID} | actioncards played: {self.actioncards_played} | userinputcounter: {self.counter_userinput_execution}\n"
        prompt_text += f"Player {self.activePlayerID}, enter a command (enter 'quit' or 'q' to exit): "
        return prompt_text
    
    def process_user_input(self, user_input):
        """
        New method for GUI to process user input
        """
        self.userInput = user_input
        return self.map_userInput()
        
    def map_userInput(self):
        print(f"map_userInput executed for {self.userInput}")
        if self.userInput == "quit" or self.userInput.lower() == "q":
            print("Exiting the program...")
            self.game_statusID = 0
            return (self.game_statusID)
        elif self.userInput == "skip" or self.userInput == "s":
            self.currentActionKey = "skip"
            self.counter_userinput_execution += 1
            self.actioncards_played = 2
            return(self.actioncards_played, self.counter_userinput_execution, self.currentActionKey) 
        elif self.userInput in self.possibleActionValues_tuple:
            print(f"{self.userInput.lower()} found in {self.possibleActionValues_tuple}")
            user_input = self.userInput.lower()
            if user_input == "b":
                user_input = "battle"
            elif user_input == "c":
                user_input = "craftsmanship"
            elif user_input == "f":
                user_input = "fellowship"
            elif user_input == "j":
                user_input = "journey"
            elif user_input == "bb":
                user_input = "2x battle"
            elif user_input == "cc":
                user_input = "2x craftsmanship"
            elif user_input == "ff":
                user_input = "2x fellowship"
            elif user_input == "jj":
                user_input = "2x journey"
            self.counter_userinput_execution += 1
            self.currentActionKey = user_input
            return(self.currentActionKey)
        else:
            print(f"User input {self.userInput} invalid.")
            return None

    def update_actioncards(self):
        print(f"lose_actioncard executed for player {self.activePlayerID}: lose actioncard '{self.currentActionKey}'")
        activePlayer_playerKey = self.get_activePlayer_playerKey()
        if self.currentActionKey == "skip":
            return(self.currentActionKey)
        elif self.currentActionKey == "joker":
            return(self.currentActionKey)
        elif self.currentActionKey in self.possibleActionKeys_tuple:
            if self.playerData[activePlayer_playerKey]['actioncards'][self.currentActionKey] > 0:
                self.playerData[activePlayer_playerKey]['actioncards'][self.currentActionKey] -= 1
                self.playerData[activePlayer_playerKey]['actioncards_played'] += 1
                self.actioncards_played += 1
                print(self.playerData[activePlayer_playerKey]['actioncards'])
                return(self.actioncards_played, self.playerData)
            elif self.playerData[activePlayer_playerKey]['actioncards']['joker'] > 0:
                print(f"Not enough '{self.currentActionKey}' cards. 'Joker' Played instead.")
                self.playerData[activePlayer_playerKey]['actioncards']['joker'] -= 1
                self.playerData[activePlayer_playerKey]['actioncards_played'] += 1
                self.actioncards_played += 1
                print(self.playerData[activePlayer_playerKey]['actioncards'])
                return(self.actioncards_played, self.playerData)
            else:
                print("not enough actioncards")
                print(self.playerData[activePlayer_playerKey]['actioncards'])
        else:
           print("actioncards error") 
           
    def trigger_cardEffect(self):
        print(f"trigger_cardEffect executed for {self.currentActionKey}")
        if self.currentActionKey == "skip" or self.currentActionKey == "joker" or self.currentActionKey == "2x joker":
            print("no effect triggered")
            return(self.currentActionKey)
        elif self.currentActionKey in self.possibleActionKeys_tuple:
            cardEffectKey = self.actionDictionary[self.currentActionKey]["effect"]
            cardEffectValue = self.actionDictionary[self.currentActionKey]["effect"][self.currentActionKey]
            self.actionpaths[self.currentActionKey] += cardEffectValue
            return(self.actionpaths)
        else:
            print("Error handling currentActionKey effect.")

    def trigger_storyEvent(self):
        print("trigger_event executed")
  
    def run_level_loop(self):
        """
        Modified for GUI compatibility - no more blocking input calls
        """
        print("\nrun_level_loop executed")
        print(f"round: {self.roundcounter}")
        self.trigger_storyEvent()
        
        if self.activePlayerID % self.numberOfPlayers == 0:
            self.roundcounter += 1
        
        # For GUI mode, we'll return early and let GUI handle the input
        # The GUI can call individual methods as needed
        if self.actioncards_played >= 2:
            self.nextPlayer()
            self.actioncards_played = 0
            
        if self.roundcounter >= 3:
            self.game_statusID = 0
            
        return self.game_statusID
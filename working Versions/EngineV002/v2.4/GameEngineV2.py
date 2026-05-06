import random
import json

#stopped here

class GameEngine:
    def __init__(self):
        self.activePlayer = False
        self.game_statusID = 1 # Set initial gamestatusID
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
            playerData = json.load(json_file)
            for key,value in self.playerData.items():
                print(key, value)       
           
    def update_gamestate(self, game_statusID, turncounter, activePlayer, actioncards_played):
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


    def lose_actioncard_artisanship(self):
        print("lose_actioncard_artisanship executed")
        activePlayer_playerKey = self.get_activePlayer_playerKey()
        with open("playerData.json", "r") as json_file:
            playerData_in_json = json.load(json_file)
            if activePlayer_playerKey in playerData_in_json:
                artisanship_value = playerData_in_json[activePlayer_playerKey]["actioncards"]["artisanship"]
                if artisanship_value > 0:  # Check if there are action cards to lose
                    artisanship_value -= 1  # Decrement the count by 1
                    playerData_in_json[activePlayer_playerKey]["actioncards"]["artisanship"] = artisanship_value  # Update the JSON data
                    with open("playerData.json", "w") as json_file:
                        json.dump(playerData_in_json, json_file, indent=4)  # Save the updated JSON data
                    print(f"lose_actioncard_artisanship: 'artisanship' card count decreased for {activePlayer_playerKey}, new artisanship card value: {artisanship_value}.")
                else:
                    print(f"lose_actioncard_artisanship: No 'artisanship' cards left for {activePlayer_playerKey}.")
            else:
                print(f"lose_actioncard_artisanship: Player {activePlayer_playerKey} not found in playerData.json.")


    def lose_actioncard_battle(self):
        print("lose_actioncard_battle executed")
        activePlayer_playerKey = self.get_activePlayer_playerKey()
        with open("playerData.json", "r") as json_file:
            playerData_in_json = json.load(json_file)
            if activePlayer_playerKey in playerData_in_json:
                battle_value = playerData_in_json[activePlayer_playerKey]["actioncards"]["battle"]
                if battle_value > 0:  # Check if there are action cards to lose
                    battle_value -= 1  # Decrement the count by 1
                    playerData_in_json[activePlayer_playerKey]["actioncards"]["battle"] = battle_value  # Update the JSON data
                    with open("playerData.json", "w") as json_file:
                        json.dump(playerData_in_json, json_file, indent=4)  # Save the updated JSON data
                    print(f"lose_actioncard_battle: 'battle' card count decreased for {activePlayer_playerKey}, new battle card value: {battle_value}.")
                else:
                    print(f"Lose_actioncard_battle: No 'battle' cards left for {activePlayer_playerKey}.")
            else:
                print(f"Lose_actioncard_battle: Player {activePlayer_playerKey} not found in playerData.json.")


    def lose_actioncard_fellowship(self):
        print("lose_actioncard_fellowship executed")
        activePlayer_playerKey = self.get_activePlayer_playerKey()
        with open("playerData.json", "r") as json_file:
            playerData_in_json = json.load(json_file)
            if activePlayer_playerKey in playerData_in_json:
                fellowship_value = playerData_in_json[activePlayer_playerKey]["actioncards"]["fellowship"]
                if fellowship_value > 0:  # Check if there are action cards to lose
                    fellowship_value -= 1  # Decrement the count by 1
                    playerData_in_json[activePlayer_playerKey]["actioncards"]["journey"] = fellowship_value  # Update the JSON data
                    with open("playerData.json", "w") as json_file:
                        json.dump(playerData_in_json, json_file, indent=4)  # Save the updated JSON data
                    print(f"lose_actioncard_fellowship: 'fellowship' card count decreased for {activePlayer_playerKey}, new fellowship card value: {fellowship_value}.")
                else:
                    print(f"lose_actioncard_fellowship: No 'felloship' cards left for {activePlayer_playerKey}.")
            else:
                print(f"lose_actioncard_fellowship: Player {activePlayer_playerKey} not found in playerData.json.")
    

    def lose_actioncard_journey(self):
        print("lose_actioncard_journey executed")
        activePlayer_playerKey = self.get_activePlayer_playerKey()
        with open("playerData.json", "r") as json_file:
            playerData_in_json = json.load(json_file)
            if activePlayer_playerKey in playerData_in_json:
                journey_value = playerData_in_json[activePlayer_playerKey]["actioncards"]["journey"]
                if journey_value > 0:  # Check if there are action cards to lose
                    journey_value -= 1  # Decrement the count by 1
                    playerData_in_json[activePlayer_playerKey]["actioncards"]["journey"] = journey_value  # Update the JSON data
                    with open("playerData.json", "w") as json_file:
                        json.dump(playerData_in_json, json_file, indent=4)  # Save the updated JSON data
                    print(f"lose_actioncard_journey: 'journey' card count decreased for {activePlayer_playerKey}, new journey card value: {journey_value}.")
                else:
                    print(f"lose_actioncard_journey: No 'journey' cards left for {activePlayer_playerKey}.")
            else:
                print(f"lose_actioncard_journey: Player {activePlayer_playerKey} not found in playerData.json.")

                    
    def run_level_loop(self):
        print("\nrun_level_loop executed")
        self.activePlayer = self.get_activePlayer_playerKey()
        user_input = input(f"\nPlayer {self.activePlayer}, enter a command (enter 'quit' or 'q' to exit): ")
        if user_input.lower() == "quit" or user_input.lower() == "q":
            print("Exiting the program...")
            self.game_statusID = 0
            return(self.game_statusID)
        elif user_input.lower() == "artisanship" or user_input.lower() == "a":
            self.lose_actioncard_artisanship()        
        elif user_input.lower() == "battle" or user_input.lower() == "b":
            self.lose_actioncard_battle()
        elif user_input.lower() == "fellowship" or user_input.lower() == "f":
            self.lose_actioncard_fellowship()
        elif user_input.lower() == "journey" or user_input.lower() == "j":
            self.lose_actioncard_journey()
            
            
            
            
            
            
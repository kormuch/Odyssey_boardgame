import json
import os
from player import Player
from actioncard import ActionCardManager

class ClassGameEngine:
    def __init__(self):
        # Initialize ActionCard system
        self.card_manager = ActionCardManager()
        
        self.actionpaths = {
            "battle": 0, 
            "fellowship": 0, 
            "craftsmanship": 0, 
            "journey": 0
        }
        
        self.actioncards_played = 0
        self.activePlayerID = 0
        self.currentActionKey = ""
        self.counter_userinput_execution = 0
        self.game_statusID = 1
        self.numberOfPlayers = 0
        self.players = []  # List of Player objects
        self.roundcounter = 1
        self.userInput = ""
        
        # Legacy properties for backward compatibility (derived from card_manager)
        self.actionDictionary = self.card_manager.get_legacy_action_dictionary()
        self.possibleActionKeys_tuple = self.card_manager.get_all_card_names()
        self.possibleActionValues_tuple = self.card_manager.get_all_keywords()
    
    def initialize_game(self, num_players=1):
        print("initialize_game executed")
        
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
            
            # Create Player objects with shared card manager
            self.players = []
            for player_id in range(1, num_players + 1):
                player = Player(player_id, starting_endurance=15, card_manager=self.card_manager)
                self.players.append(player)
            
            # Set first player as active
            self.players[0].set_active(True)
            
            # Save player data
            self.save_player_data()
            
            print("Updated 'activePlayer' status for player 1 to True.")
            return num_players
        else:
            print("Invalid input. Using default 2 players.")
            return self.initialize_game(2)

    def deal_6_cards_perplayer(self):
        print("deal_6_cards_perplayer executed")
        
        if not self.players:
            print("Warning: No players initialized. Initializing default game first.")
            self.initialize_game(2)
        
        # Deal cards to each player using ActionCardManager
        for player in self.players:
            player.deal_cards(num_cards=6)
        
        # Save the updated player data
        self.save_player_data()
        self.load_and_display_player_data()
        
        return "Cards dealt successfully"
    
    def get_active_player(self):
        """Get the active Player object"""
        for player in self.players:
            if player.is_active:
                return player
        return None
    
    def get_player_by_id(self, player_id):
        """Get player by ID"""
        for player in self.players:
            if player.player_id == player_id:
                return player
        return None
        
    def nextPlayer(self):
        print("nextPlayer executed")
        
        # Deactivate current player
        current_player = self.get_active_player()
        if current_player:
            current_player.set_active(False)
        
        # Calculate next player ID
        self.activePlayerID = (self.activePlayerID + 1) % (self.numberOfPlayers + 1)
        if self.activePlayerID == 0:
            self.activePlayerID += 1
        
        # Activate next player
        next_player = self.get_player_by_id(self.activePlayerID)
        if next_player:
            next_player.set_active(True)
        
        return self.activePlayerID

    def userInput_prompt(self):
        """Get prompt text for GUI"""
        print("userInput_prompt executed")
        prompt_text = f"game statusID: {self.game_statusID} | active player: {self.activePlayerID} | actioncards played: {self.actioncards_played} | userinputcounter: {self.counter_userinput_execution}\n"
        prompt_text += f"Player {self.activePlayerID}, enter a command (enter 'quit' or 'q' to exit): "
        return prompt_text
    
    def process_user_input(self, user_input):
        """Process user input from GUI"""
        self.userInput = user_input
        return self.map_userInput()
        
    def map_userInput(self):
        print(f"map_userInput executed for {self.userInput}")
        if self.userInput == "quit" or self.userInput.lower() == "q":
            print("Exiting the program...")
            self.game_statusID = 0
            return self.game_statusID
        elif self.userInput == "skip" or self.userInput == "s":
            self.currentActionKey = "skip"
            self.counter_userinput_execution += 1
            self.actioncards_played = 2
            return (self.actioncards_played, self.counter_userinput_execution, self.currentActionKey) 
        elif self.card_manager.validate_input(self.userInput):
            print(f"{self.userInput.lower()} found in valid keywords")
            
            # Use ActionCardManager to resolve input to card name
            resolved_card_name = self.card_manager.resolve_input_to_card_name(self.userInput)
            
            if resolved_card_name:
                self.counter_userinput_execution += 1
                self.currentActionKey = resolved_card_name
                return self.currentActionKey
            else:
                print(f"Could not resolve input: {self.userInput}")
                return None
        else:
            print(f"User input {self.userInput} invalid.")
            return None

    def update_actioncards(self):
        print(f"update_actioncards executed for player {self.activePlayerID}: play actioncard '{self.currentActionKey}'")
        
        if self.currentActionKey == "skip":
            return self.currentActionKey
        elif self.currentActionKey == "joker":
            return self.currentActionKey
        elif self.currentActionKey in self.card_manager:
            # Use Player class methods
            active_player = self.get_active_player()
            if active_player:
                if active_player.play_card(self.currentActionKey):
                    self.actioncards_played += 1
                    return (self.actioncards_played, self.get_player_data())
                else:
                    print("not enough actioncards")
                    return None
        else:
           print("actioncards error")
           return None
           
    def trigger_cardEffect(self):
        print(f"trigger_cardEffect executed for {self.currentActionKey}")
        
        # Use ActionCardManager to handle effects
        if self.currentActionKey == "skip":
            print("no effect triggered")
            return self.currentActionKey
        else:
            return self.card_manager.trigger_card_effect(self.currentActionKey, self.actionpaths)

    def trigger_storyEvent(self):
        print("trigger_event executed")
  
    def run_level_loop(self):
        """Main game loop for GUI compatibility"""
        print("\nrun_level_loop executed")
        print(f"round: {self.roundcounter}")
        self.trigger_storyEvent()
        
        if self.activePlayerID % self.numberOfPlayers == 0:
            self.roundcounter += 1
        
        if self.actioncards_played >= 2:
            self.nextPlayer()
            self.actioncards_played = 0
            
        if self.roundcounter >= 3:
            self.game_statusID = 0
            
        return self.game_statusID
    
    def save_player_data(self):
        """Save player data to JSON file"""
        try:
            player_data = self.get_player_data()
            with open("playerdata.json", "w") as json_file:
                json.dump(player_data, json_file, indent=4)
            print("Player information saved to 'playerdata.json'.")
        except Exception as e:
            print(f"Warning: Could not save to file: {e}")
    
    def get_player_data(self):
        """Get player data in dictionary format"""
        player_data = {}
        for player in self.players:
            key = f"player {player.player_id}"
            player_data[key] = player.to_dict()
        return player_data
    
    def get_activePlayer_playerKey(self):
        """Legacy method for GUI compatibility"""
        return f"player {self.activePlayerID}"
    
    @property
    def playerData(self):
        """Legacy property for GUI compatibility - returns current player data"""
        return self.get_player_data()
    
    def load_and_display_player_data(self):
        """Load and display player data"""
        try:
            if os.path.exists("playerdata.json"):
                with open("playerdata.json", "r") as json_file:
                    data = json.load(json_file)
                    for key, value in data.items():
                        print(key, value)
        except Exception as e:
            print(f"Warning: File operation failed: {e}")
    
    def load_player_data_from_file(self):
        """Load player data from JSON file and recreate Player objects"""
        try:
            if os.path.exists("playerdata.json"):
                with open("playerdata.json", "r") as json_file:
                    data = json.load(json_file)
                    
                    # Recreate players from saved data
                    self.players = []
                    for key, player_data in data.items():
                        player = Player.from_dict(player_data, self.card_manager)
                        self.players.append(player)
                        if player.is_active:
                            self.activePlayerID = player.player_id
                    
                    self.numberOfPlayers = len(self.players)
                    print("Player data loaded successfully from file.")
                    return True
        except Exception as e:
            print(f"Warning: Could not load player data: {e}")
            return False
    
    def get_card_manager(self):
        """Get the ActionCardManager instance"""
        return self.card_manager
    
    def add_custom_card(self, name, keywords, effect=None, category="custom"):
        """Add a custom card to the game"""
        self.card_manager.add_card(name, keywords, effect, category)
        # Update legacy properties
        self.actionDictionary = self.card_manager.get_legacy_action_dictionary()
        self.possibleActionKeys_tuple = self.card_manager.get_all_card_names()
        self.possibleActionValues_tuple = self.card_manager.get_all_keywords()
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

    # =============================================================================
    # GAME INITIALIZATION MODULE
    # =============================================================================
    
    def initialize_game(self, num_players=1, deal_cards=True, starting_endurance=15):
        """
        Complete game initialization with players and optional card dealing.
        
        Args:
            num_players: Number of players (1-5) or 'q' to quit
            deal_cards: Whether to deal initial cards (default: True)
            starting_endurance: Starting endurance for players (default: 15)
            
        Returns:
            int: Number of players created, or 0 if quitting
        """
        print("initialize_game executed")
        
        # Handle quit command
        if isinstance(num_players, str) and num_players == 'q':
            self.game_statusID = 0
            return 0
        
        # Validate and convert num_players
        validated_players = self._validate_player_count(num_players)
        if validated_players == 0:
            return 0
            
        # Create players and set up game state
        self._setup_players(validated_players, starting_endurance)
        
        # Deal initial cards if requested
        if deal_cards:
            self._deal_initial_cards()
        
        # Save and display game state
        self._save_and_display_state()
        
        return validated_players
    
    def _validate_player_count(self, num_players):
        """Validate and normalize player count input."""
        try:
            if isinstance(num_players, str):
                num_players = int(num_players)
        except ValueError:
            print("Invalid input. Using default 2 players.")
            return 2
            
        if 1 <= num_players <= 5:
            return num_players
        else:
            print("Invalid input. Using default 2 players.")
            return 2
    
    def _setup_players(self, num_players, starting_endurance):
        """Create and configure player objects."""
        self.numberOfPlayers = num_players
        self.activePlayerID = 1
        
        # Create Player objects with shared card manager
        self.players = []
        for player_id in range(1, num_players + 1):
            player = Player(player_id, starting_endurance=starting_endurance, 
                          card_manager=self.card_manager)
            self.players.append(player)
        
        # Set first player as active
        self.players[0].set_active(True)
        print(f"Created {num_players} players. Player 1 is active.")
    
    def _deal_initial_cards(self, cards_per_player=6):
        """Deal initial cards to all players."""
        print(f"Dealing {cards_per_player} cards to each player...")
        
        for player in self.players:
            player.deal_cards(num_cards=cards_per_player)
        
        print("Cards dealt successfully")
    
    def _save_and_display_state(self):
        """Save player data and display current state."""
        self.save_player_data()
        self.load_and_display_player_data()
    
    # =============================================================================
    # LEGACY METHODS - CAN BE REMOVED
    # =============================================================================
    
    # No legacy methods needed anymore - all functionality integrated into main methods

    # =============================================================================
    # GAME STATUS SYSTEM
    # =============================================================================
    
    @staticmethod
    def get_status_meaning(status_id):
        """
        Get human-readable meaning of game status ID
        
        Returns:
            str: Status description
        """
        status_meanings = {
            0: "Game not started",
            1: "Game initialized but not running",
            1000: "Game running", 
            -1: "Game completed"
        }
        return status_meanings.get(status_id, f"Unknown status: {status_id}")
    
    def get_current_game_status(self):
        """Get detailed current game status for GUI"""
        return {
            'game_statusID': self.game_statusID,
            'status_meaning': self.get_status_meaning(self.game_statusID),
            'activePlayerID': self.activePlayerID,
            'actioncards_played': self.actioncards_played,
            'roundcounter': self.roundcounter,
            'numberOfPlayers': self.numberOfPlayers
        }

    # =============================================================================
    # PLAYER MANAGEMENT
    # =============================================================================
    
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
        """Switch to the next player in turn order."""
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

    # =============================================================================
    # INPUT PROCESSING
    # =============================================================================

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
        """Map user input to valid game actions."""
        print(f"map_userInput executed for {self.userInput}")
        
        if self.userInput in ["quit", "q"]:
            print("Exiting the program...")
            self.game_statusID = -1
            return self.game_statusID
            
        elif self.userInput in ["skip", "s"]:
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

    # =============================================================================
    # GAME ACTION PROCESSING
    # =============================================================================

    def update_actioncards(self):
        """Process action card play for the current player."""
        print(f"update_actioncards executed for player {self.activePlayerID}: play actioncard '{self.currentActionKey}'")
        
        if self.currentActionKey in ["skip", "joker"]:
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
        """Trigger the effect of the current action card."""
        print(f"trigger_cardEffect executed for {self.currentActionKey}")
        
        if self.currentActionKey == "skip":
            print("no effect triggered")
            return self.currentActionKey
        else:
            return self.card_manager.trigger_card_effect(self.currentActionKey, self.actionpaths)

    def trigger_storyEvent(self):
        """Trigger story events (placeholder for future implementation)."""
        print("trigger_event executed")

    # =============================================================================
    # GAME LOOP
    # =============================================================================
  
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

        return self.game_statusID

    # =============================================================================
    # DATA PERSISTENCE
    # =============================================================================
    
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

    # =============================================================================
    # LEGACY PROPERTIES & METHODS (for backward compatibility)
    # =============================================================================
    
    def get_activePlayer_playerKey(self):
        """Legacy method for GUI compatibility"""
        return f"player {self.activePlayerID}"
    
    @property
    def playerData(self):
        """Legacy property for GUI compatibility - returns current player data"""
        return self.get_player_data()
    
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
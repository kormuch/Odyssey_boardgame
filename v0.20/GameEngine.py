import json
import os
from player import Player
from actioncard import ActionCardManager
from gamestate import GameState, GameStatus
from commands import CommandManager, Command, QuitCommand, SkipTurnCommand, PlayCardCommand

class ClassGameEngine:
    def __init__(self):
        # Initialize ActionCard system
        self.card_manager = ActionCardManager()
        
        # Initialize centralized game state
        self.state = GameState()
        
        # Initialize command manager
        self.command_manager = CommandManager(self.card_manager)
        
        # Player management (kept separate from state)
        self.players = []  # List of Player objects
        
        # Legacy properties for backward compatibility (derived from card_manager)
        self.actionDictionary = self.card_manager.get_legacy_action_dictionary()
        self.possibleActionKeys_tuple = self.card_manager.get_all_card_names()
        self.possibleActionValues_tuple = self.card_manager.get_all_keywords()

    # =============================================================================
    # LEGACY PROPERTY MAPPINGS (for backward compatibility)
    # =============================================================================
    
    @property
    def actionpaths(self):
        """Legacy property mapping to state.action_paths"""
        return self.state.action_paths
    
    @property
    def actioncards_played(self):
        """Legacy property mapping"""
        return self.state.action_cards_played
    
    @actioncards_played.setter
    def actioncards_played(self, value):
        """Legacy property setter"""
        self.state.action_cards_played = value
    
    @property
    def activePlayerID(self):
        """Legacy property mapping"""
        return self.state.active_player_id
    
    @activePlayerID.setter
    def activePlayerID(self, value):
        """Legacy property setter"""
        self.state.active_player_id = value
    
    @property
    def currentActionKey(self):
        """Legacy property mapping"""
        return self.state.current_action_key
    
    @currentActionKey.setter
    def currentActionKey(self, value):
        """Legacy property setter"""
        self.state.current_action_key = value
    
    @property
    def counter_userinput_execution(self):
        """Legacy property mapping"""
        return self.state.user_input_counter
    
    @counter_userinput_execution.setter
    def counter_userinput_execution(self, value):
        """Legacy property setter"""
        self.state.user_input_counter = value
    
    @property
    def game_statusID(self):
        """Legacy property mapping"""
        return self.state.status.value
    
    @game_statusID.setter
    def game_statusID(self, value):
        """Legacy property setter"""
        # Convert integer to GameStatus enum
        if value == 0:
            self.state.status = GameStatus.NOT_STARTED
        elif value == 1:
            self.state.status = GameStatus.INITIALIZED
        elif value == 1000:
            self.state.status = GameStatus.RUNNING
        elif value == -1:
            self.state.status = GameStatus.COMPLETED
    
    @property
    def numberOfPlayers(self):
        """Legacy property mapping"""
        return self.state.number_of_players
    
    @numberOfPlayers.setter
    def numberOfPlayers(self, value):
        """Legacy property setter"""
        self.state.number_of_players = value
    
    @property
    def roundcounter(self):
        """Legacy property mapping"""
        return self.state.round_counter
    
    @roundcounter.setter
    def roundcounter(self, value):
        """Legacy property setter"""
        self.state.round_counter = value
    
    @property
    def userInput(self):
        """Legacy property - kept local as it's temporary"""
        return self._userInput if hasattr(self, '_userInput') else ""
    
    @userInput.setter
    def userInput(self, value):
        """Legacy property setter"""
        self._userInput = value

    # =============================================================================
    # COMMAND CONTEXT BUILDER
    # =============================================================================
    
    def _build_command_context(self):
        """Build context dictionary for command execution"""
        return {
            'game_state': self.state,
            'active_player': self.get_active_player(),
            'players': self.players,
            'card_manager': self.card_manager,
            'game_engine': self  # Some commands might need the full engine
        }

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
            self.state.status = GameStatus.NOT_STARTED
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
        self.state.number_of_players = num_players
        self.state.active_player_id = 1
        
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
    # GAME STATUS SYSTEM
    # =============================================================================
    
    @staticmethod
    def get_status_meaning(status_id):
        """
        Get human-readable meaning of game status ID
        
        Returns:
            str: Status description
        """
        # Convert to GameStatus enum and get description
        try:
            if status_id == 0:
                return GameStatus.NOT_STARTED.description
            elif status_id == 1:
                return GameStatus.INITIALIZED.description
            elif status_id == 1000:
                return GameStatus.RUNNING.description
            elif status_id == -1:
                return GameStatus.COMPLETED.description
            else:
                return f"Unknown status: {status_id}"
        except:
            return f"Unknown status: {status_id}"
    
    def get_current_game_status(self):
        """Get detailed current game status for GUI"""
        return {
            'game_statusID': self.state.status.value,
            'status_meaning': self.state.status.description,
            'activePlayerID': self.state.active_player_id,
            'actioncards_played': self.state.action_cards_played,
            'roundcounter': self.state.round_counter,
            'numberOfPlayers': self.state.number_of_players
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
        
        # Use GameState's next_player method
        new_player_id = self.state.next_player(self.state.number_of_players)
        
        # Activate next player
        next_player = self.get_player_by_id(new_player_id)
        if next_player:
            next_player.set_active(True)
        
        return new_player_id

    # =============================================================================
    # INPUT PROCESSING - NOW WITH COMMAND PATTERN
    # =============================================================================

    def userInput_prompt(self):
        """Get prompt text for GUI"""
        print("userInput_prompt executed")
        prompt_text = f"game statusID: {self.state.status.value} | active player: {self.state.active_player_id} | actioncards played: {self.state.action_cards_played} | userinputcounter: {self.state.user_input_counter}\n"
        prompt_text += f"Player {self.state.active_player_id}, enter a command (enter 'quit' or 'q' to exit): "
        return prompt_text
    
    def process_user_input(self, user_input):
        """Process user input from GUI"""
        self.userInput = user_input
        return self.map_userInput()
    
    def map_userInput(self):
        """
        Map user input to valid game actions.
        Now uses Command Pattern internally while maintaining legacy behavior.
        """
        print(f"map_userInput executed for {self.userInput}")
        
        # Try to parse input as a command
        command = self.command_manager.parse_input(self.userInput)
        
        if command:
            # Build context for command execution
            context = self._build_command_context()
            
            # Check if command can be executed
            if not command.can_execute(context):
                print(f"Command cannot be executed in current context")
                return None
            
            # Execute command and handle result based on command type
            if isinstance(command, QuitCommand):
                # Execute quit command
                command.execute(context)
                print("Exiting the program...")
                return self.state.status.value
                
            elif isinstance(command, SkipTurnCommand):
                # Execute skip command
                command.execute(context)
                return (self.state.action_cards_played, self.state.user_input_counter, self.state.current_action_key)
                
            elif isinstance(command, PlayCardCommand):
                # For play card commands, we need to maintain legacy behavior
                # The command validates but we still use the legacy update flow
                self.state.user_input_counter += 1
                self.state.current_action_key = command.card_name
                return self.state.current_action_key
            else:
                # Unknown command type, try to handle generically
                result = command.execute(context)
                return result
        else:
            # No valid command found - maintain legacy behavior
            print(f"User input {self.userInput} invalid.")
            return None

    def map_userInput_legacy(self):
        """
        LEGACY METHOD - Keep for reference/fallback
        Original map_userInput implementation
        """
        print(f"map_userInput_legacy executed for {self.userInput}")
        
        if self.userInput in ["quit", "q"]:
            print("Exiting the program...")
            self.state.status = GameStatus.COMPLETED
            return self.state.status.value
            
        elif self.userInput in ["skip", "s"]:
            self.state.current_action_key = "skip"
            self.state.user_input_counter += 1
            self.state.action_cards_played = 2
            return (self.state.action_cards_played, self.state.user_input_counter, self.state.current_action_key)
            
        elif self.card_manager.validate_input(self.userInput):
            print(f"{self.userInput.lower()} found in valid keywords")
            
            # Use ActionCardManager to resolve input to card name
            resolved_card_name = self.card_manager.resolve_input_to_card_name(self.userInput)
            
            if resolved_card_name:
                self.state.user_input_counter += 1
                self.state.current_action_key = resolved_card_name
                return self.state.current_action_key
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
        print(f"update_actioncards executed for player {self.state.active_player_id}: play actioncard '{self.state.current_action_key}'")
        
        if self.state.current_action_key in ["skip", "joker"]:
            return self.state.current_action_key
            
        elif self.state.current_action_key in self.card_manager:
            # Use Player class methods
            active_player = self.get_active_player()
            if active_player:
                if active_player.play_card(self.state.current_action_key):
                    self.state.action_cards_played += 1
                    return (self.state.action_cards_played, self.get_player_data())
                else:
                    print("not enough actioncards")
                    return None
        else:
           print("actioncards error")
           return None
           
    def trigger_cardEffect(self):
        """Trigger the effect of the current action card."""
        print(f"trigger_cardEffect executed for {self.state.current_action_key}")
        
        if self.state.current_action_key == "skip":
            print("no effect triggered")
            return self.state.current_action_key
        else:
            return self.card_manager.trigger_card_effect(
                self.state.current_action_key, 
                self.state.action_paths
            )

    def trigger_storyEvent(self):
        """Trigger story events (placeholder for future implementation)."""
        print("trigger_event executed")

    # =============================================================================
    # GAME LOOP
    # =============================================================================
  
    def run_level_loop(self):
        """Main game loop for GUI compatibility"""
        print("\nrun_level_loop executed")
        print(f"round: {self.state.round_counter}")
        self.trigger_storyEvent()
        
        if self.state.active_player_id % self.state.number_of_players == 0:
            self.state.increment_round()
        
        if self.state.action_cards_played >= 2:
            self.nextPlayer()
            self.state.reset_turn()

        return self.state.status.value

    # =============================================================================
    # COMMAND PATTERN HELPERS
    # =============================================================================
    
    def get_available_commands(self):
        """Get list of currently available commands"""
        context = self._build_command_context()
        return self.command_manager.get_available_commands(context)
    
    def execute_command_directly(self, command_name, **kwargs):
        """
        Execute a command directly by name (useful for GUI buttons)
        
        Args:
            command_name: Name of the command ('quit', 'skip', etc.)
            **kwargs: Additional arguments for the command
            
        Returns:
            Command execution result or None if command not found
        """
        command = self.command_manager.parse_input(command_name)
        if command:
            context = self._build_command_context()
            context.update(kwargs)  # Add any additional kwargs to context
            return self.command_manager.execute_command(command, context)
        return None

    # =============================================================================
    # DATA PERSISTENCE
    # =============================================================================
    
    def save_player_data(self):
        """Save player data to JSON file"""
        try:
            # Include game state in the save
            save_data = {
                'game_state': self.state.to_dict(),
                'players': self.get_player_data()
            }
            
            with open("playerdata.json", "w") as json_file:
                json.dump(save_data, json_file, indent=4)
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
                    
                    # Display game state if present
                    if 'game_state' in data:
                        print("Game State:", data['game_state'])
                    
                    # Display player data
                    if 'players' in data:
                        for key, value in data['players'].items():
                            print(key, value)
                    else:
                        # Legacy format support
                        for key, value in data.items():
                            if key != 'game_state':
                                print(key, value)
        except Exception as e:
            print(f"Warning: File operation failed: {e}")
    
    def load_player_data_from_file(self):
        """Load player data from JSON file and recreate Player objects"""
        try:
            if os.path.exists("playerdata.json"):
                with open("playerdata.json", "r") as json_file:
                    data = json.load(json_file)
                    
                    # Load game state if present
                    if 'game_state' in data:
                        self.state = GameState.from_dict(data['game_state'])
                    
                    # Determine where player data is stored
                    player_data = data.get('players', data)
                    
                    # Recreate players from saved data
                    self.players = []
                    for key, player_dict in player_data.items():
                        if key != 'game_state':  # Skip non-player entries
                            player = Player.from_dict(player_dict, self.card_manager)
                            self.players.append(player)
                            if player.is_active:
                                self.state.active_player_id = player.player_id
                    
                    self.state.number_of_players = len(self.players)
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
        return f"player {self.state.active_player_id}"
    
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
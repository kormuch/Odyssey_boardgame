import json
import os
from player import Player
from actioncard import ActionCardManager
from gamestate import GameState, GameStatus
from commands import CommandManager, Command, QuitCommand, SkipTurnCommand, PlayCardCommand
from persistence import PersistenceManager, SaveManager  # Import the new classes

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
        
        # NEW: Initialize persistence system
        self.persistence_manager = PersistenceManager()
        self.save_manager = SaveManager(self.persistence_manager)
        
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
        
        # Save and display game state - NOW USES NEW PERSISTENCE SYSTEM
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
        """Save player data and display current state using new persistence system."""
        self.save_game()  # Use new save method
        self.display_current_state()  # New method for displaying state

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
    # GAME LOOP - NOW WITH AUTOSAVE INTEGRATION
    # =============================================================================
  
    def run_level_loop(self):
        """Main game loop for GUI compatibility - now with autosave integration"""
        print("\nrun_level_loop executed")
        print(f"round: {self.state.round_counter}")
        self.trigger_storyEvent()
        
        if self.state.active_player_id % self.state.number_of_players == 0:
            self.state.increment_round()
            # NEW: Check for autosave after round increment
            self.save_manager.check_autosave(self)
        
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
    # NEW PERSISTENCE SYSTEM - REPLACES OLD DATA PERSISTENCE
    # =============================================================================
    
    def save_game(self, filename=None):
        """Save game using the new persistence system"""
        return self.save_manager.save_game(self)
    
    def load_game(self, filename=None):
        """Load game using the new persistence system"""
        return self.save_manager.load_game(self, filename)
    
    def create_autosave(self):
        """Create an autosave"""
        game_data = {
            'game_state': self.state.to_dict(),
            'players': self.get_player_data(),
            'settings': {
                'autosave_enabled': self.save_manager.autosave_enabled,
                'autosave_interval': self.save_manager.autosave_interval
            }
        }
        return self.persistence_manager.create_autosave(game_data)
    
    def list_saves(self):
        """List available save files"""
        return self.persistence_manager.list_save_files()
    
    def delete_save(self, filename):
        """Delete a save file"""
        return self.persistence_manager.delete_save(filename)
    
    def export_game(self, export_path):
        """Export game to external location"""
        game_data = {
            'game_state': self.state.to_dict(),
            'players': self.get_player_data(),
        }
        return self.persistence_manager.export_game_data(game_data, export_path)
    
    def import_game(self, import_path):
        """Import game from external location"""
        data = self.persistence_manager.import_game_data(import_path)
        if data:
            # Reconstruct game state
            self.state = GameState.from_dict(data['game_state'])
            
            # Reconstruct players
            self.players = []
            for key, player_data in data['players'].items():
                player = Player.from_dict(player_data, self.card_manager)
                self.players.append(player)
            
            return True
        return False
    
    def display_current_state(self):
        """Display current game state"""
        print("=== Current Game State ===")
        print(f"Status: {self.state.status.description}")
        print(f"Round: {self.state.round_counter}")
        print(f"Active Player: {self.state.active_player_id}")
        print(f"Action Cards Played: {self.state.action_cards_played}")
        print(f"Number of Players: {self.state.number_of_players}")
        
        print("\n=== Players ===")
        for player in self.players:
            status = " (ACTIVE)" if player.is_active else ""
            # Get player info safely without assuming attribute names
            player_dict = player.to_dict()
            
            # Build info string dynamically based on what's available
            info_parts = []
            
            # Common attributes to display if they exist
            if 'endurance' in player_dict:
                info_parts.append(f"Endurance: {player_dict['endurance']}")
            
            # Try different possible card attributes
            cards_count = None
            for card_attr in ['cards', 'hand', 'actioncards', 'deck']:
                if card_attr in player_dict and isinstance(player_dict[card_attr], (list, dict)):
                    cards_count = len(player_dict[card_attr])
                    break
            
            if cards_count is not None:
                info_parts.append(f"Cards: {cards_count}")
            
            # Add any other relevant info from player_dict
            for key, value in player_dict.items():
                if key not in ['player_id', 'is_active', 'endurance', 'cards', 'hand', 'actioncards', 'deck']:
                    if isinstance(value, (int, float, str, bool)):
                        info_parts.append(f"{key.title()}: {value}")
            
            info_str = ", ".join(info_parts) if info_parts else "No additional info"
            print(f"Player {player.player_id}{status}: {info_str}")

    # =============================================================================
    # PERSISTENCE SETTINGS
    # =============================================================================
    
    def configure_autosave(self, enabled=True, interval=5):
        """Configure autosave settings"""
        self.save_manager.autosave_enabled = enabled
        self.save_manager.autosave_interval = interval
        print(f"Autosave {'enabled' if enabled else 'disabled'}, interval: {interval} rounds")
    
    def get_persistence_info(self):
        """Get information about persistence system"""
        return {
            'autosave_enabled': self.save_manager.autosave_enabled,
            'autosave_interval': self.save_manager.autosave_interval,
            'save_directory': str(self.persistence_manager.save_directory),
            'current_save_file': self.persistence_manager.current_save_file,
            'available_saves': len(self.persistence_manager.list_save_files())
        }

    # =============================================================================
    # LEGACY COMPATIBILITY LAYER
    # =============================================================================
    
    def save_player_data(self):
        """LEGACY: Redirect to new save system"""
        print("Warning: save_player_data() is deprecated. Use save_game() instead.")
        return self.save_game()
    
    def load_and_display_player_data(self):
        """LEGACY: Redirect to new display method"""
        print("Warning: load_and_display_player_data() is deprecated.")
        self.display_current_state()
    
    def load_player_data_from_file(self):
        """LEGACY: Redirect to new load system"""
        print("Warning: load_player_data_from_file() is deprecated. Use load_game() instead.")
        return self.load_game()
    
    def get_player_data(self):
        """Get player data in dictionary format - KEPT FOR COMPATIBILITY"""
        player_data = {}
        for player in self.players:
            key = f"player {player.player_id}"
            player_data[key] = player.to_dict()
        return player_data

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
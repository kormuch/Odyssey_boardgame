class GameStateManager:
    """Manages game state and engine interactions"""
    
    def __init__(self, engine=None):
        self.engine = engine  # Use provided engine or create one
        self.current_message = "Welcome! Click START to begin."
        self.awaiting_input = False
        self.input_prompt = ""
        
        if self.engine is None:
            self._initialize_engine()
    
    def _initialize_engine(self):
        """Initialize the game engine"""
        try:
            # Import your actual GameEngine
            from GameEngine import ClassGameEngine
            self.engine = ClassGameEngine()
            print("✓ Real GameEngine loaded successfully!")
            print(f"Engine initialized with game_statusID: {self.engine.game_statusID}")
        except ImportError as e:
            print(f"❌ GameEngine import failed: {e}")
            print("Make sure GameEngine.py is in the same directory as your GUI")

    
    def get_status_text(self):
        """Generate status text based on current game state"""
        if not self.engine:
            return "No game engine loaded"
        
        status_lines = [
            f"Game Status: {getattr(self.engine, 'game_statusID', 'Unknown')}",
            f"Players: {getattr(self.engine, 'numberOfPlayers', 0)}",
            f"Active Player: {getattr(self.engine, 'activePlayerID', 0)}",
            f"Round: {getattr(self.engine, 'roundcounter', 0)}",
            f"Total Cards Played: {getattr(self.engine, 'actioncards_played', 0)}",
            "",
            f"Action Paths Progress:",
            f"Battle: {self.engine.actionpaths.get('battle', 0)}",
            f"Craftsmanship: {self.engine.actionpaths.get('craftsmanship', 0)}",
            f"Fellowship: {self.engine.actionpaths.get('fellowship', 0)}",
            f"Journey: {self.engine.actionpaths.get('journey', 0)}",
            "",
            self.current_message
        ]
        
        return "\n".join(status_lines)
    
    def get_total_progress(self):
        """Get total progress from action paths"""
        return sum(self.engine.actionpaths.values()) if hasattr(self.engine, 'actionpaths') else 0
    
    def get_actionpaths(self):
        """Get action paths dictionary"""
        return getattr(self.engine, 'actionpaths', {})
    
    def get_player_card_count(self, card_name):
        """Get card count for active player"""
        if (hasattr(self.engine, 'playerData') and self.engine.playerData and 
            hasattr(self.engine, 'activePlayerID') and self.engine.activePlayerID > 0):
            
            player_key = f"player {self.engine.activePlayerID}"
            if (player_key in self.engine.playerData and 
                'actioncards' in self.engine.playerData[player_key]):
                return self.engine.playerData[player_key]['actioncards'].get(card_name.lower(), 0)
        
        return 0
    
    def set_message(self, message):
        """Set the current status message"""
        self.current_message = message
    
    def append_message(self, message):
        """Append to the current status message"""
        self.current_message += f"\n{message}"
    
    def get_current_player_info(self):
        """Get detailed information about the current player"""
        if not hasattr(self.engine, 'playerData') or not self.engine.playerData:
            return None
            
        player_key = f"player {self.engine.activePlayerID}"
        if player_key in self.engine.playerData:
            return self.engine.playerData[player_key]
        
        return None
    
    def is_game_initialized(self):
        """Check if the game is properly initialized"""
        return (hasattr(self.engine, 'game_statusID') and 
                self.engine.game_statusID >= 1000 and
                hasattr(self.engine, 'numberOfPlayers') and
                self.engine.numberOfPlayers > 0)
    
    def is_game_active(self):
        """Check if the game is currently active"""
        return (self.is_game_initialized() and 
                hasattr(self.engine, 'game_statusID') and 
                self.engine.game_statusID > 0)
    
    def reset_game_state(self):
        """Reset the game state"""
        if self.engine:
            self.engine.game_statusID = 1
            self.engine.numberOfPlayers = 0
            self.engine.activePlayerID = 1
            self.engine.actioncards_played = 0
            self.engine.roundcounter = 1
            self.engine.actionpaths = {"battle": 0, "craftsmanship": 0, "fellowship": 0, "journey": 0}
            self.engine.playerData = {}
        self.current_message = "Game reset. Click START to begin."
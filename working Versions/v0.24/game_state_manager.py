# game_state_manager.py
from gamelog import logger

class GameStateManager:
    """Manages game state and engine interactions"""
    
    def __init__(self, engine=None):
        self.engine = engine
        self.current_message = "Welcome! Click START to begin."
        self.awaiting_input = False
        self.input_prompt = ""
        
        if self.engine is None:
            self._initialize_engine()
        else:
            logger.info("GameStateManager initialized with provided engine")
    
    def _initialize_engine(self):
        """Initialize the game engine"""
        try:
            from GameEngine import ClassGameEngine
            self.engine = ClassGameEngine()
            logger.info(f"GameEngine loaded successfully (status: {self.engine.game_statusID})")
        except ImportError as e:
            logger.error(f"Failed to import GameEngine: {e}")
            logger.error("Make sure GameEngine.py is in the same directory")
        except Exception as e:
            logger.error(f"Error initializing GameEngine: {e}")
            logger.exception("Full traceback:")
    
    def get_status_text(self):
        """Generate status text based on current game state"""
        if not self.engine:
            logger.warning("get_status_text called but no engine loaded")
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
            f"Wits: {self.engine.actionpaths.get('wits', 0)}",
            f"Fellowship: {self.engine.actionpaths.get('fellowship', 0)}",
            f"Journey: {self.engine.actionpaths.get('journey', 0)}",
            "",
            self.current_message
        ]
        return "\n".join(status_lines)
    
    def get_collision_track_data(self):
        """Get collision track data for rendering the danger track"""
        if hasattr(self.engine, 'state'):
            return self.engine.state.get_collision_track_status()
        
        # Fallback if state not available
        return {
            'left_position': 0,
            'right_position': 20,
            'distance': 20,
            'collision': False,
            'track_length': 20,
            'right_marker_progress_pct': 0
        }
    
    def get_actionpaths(self):
        """Get action paths dictionary (quest progress)"""
        return getattr(self.engine, 'actionpaths', {})
    
    def get_player_card_count(self, card_name):
        """Get card count for active player"""
        count = 0
        if (hasattr(self.engine, 'playerData') and self.engine.playerData and 
            hasattr(self.engine, 'activePlayerID') and self.engine.activePlayerID > 0):
            
            player_key = f"player {self.engine.activePlayerID}"
            if (player_key in self.engine.playerData and 
                'actioncards' in self.engine.playerData[player_key]):
                count = self.engine.playerData[player_key]['actioncards'].get(card_name.lower(), 0)
        
        return count
    
    def set_message(self, message):
        """Set the current status message"""
        self.current_message = message
        logger.game_debug(f"Status message set: {message[:50]}...")
    
    def append_message(self, message):
        """Append to the current status message"""
        self.current_message += f"\n{message}"
        logger.game_debug(f"Status message appended: {message[:50]}...")
    
    def get_current_player_info(self):
        """Get detailed information about the current player"""
        if not hasattr(self.engine, 'playerData') or not self.engine.playerData:
            return None
        
        player_key = f"player {self.engine.activePlayerID}"
        info = self.engine.playerData.get(player_key, None)
        return info
    
    def is_game_initialized(self):
        """Check if the game is properly initialized"""
        initialized = (hasattr(self.engine, 'game_statusID') and 
                       self.engine.game_statusID >= 1000 and
                       hasattr(self.engine, 'numberOfPlayers') and
                       self.engine.numberOfPlayers > 0)
        return initialized
    
    def is_game_active(self):
        """Check if the game is currently active"""
        active = self.is_game_initialized() and hasattr(self.engine, 'game_statusID') and self.engine.game_statusID > 0
        return active
    
    def reset_game_state(self):
        """Reset the game state"""
        if self.engine:
            old_status = self.engine.game_statusID
            
            self.engine.game_statusID = 1
            self.engine.numberOfPlayers = 0
            self.engine.activePlayerID = 1
            self.engine.actioncards_played = 0
            self.engine.roundcounter = 1
            self.engine.actionpaths = {"battle": 0, "wits": 0, "fellowship": 0, "journey": 0}
            self.engine.playerData = {}
            
            # Reset collision track if state exists
            if hasattr(self.engine, 'state'):
                self.engine.state.left_marker = 0
                self.engine.state.right_marker = 20
            
            self.current_message = "Game reset. Click START to begin."
            logger.state_change("game_state", old_status, 1, action="full_reset")
# game_state_manager.py
import logging
logger = logging.getLogger(__name__)

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
            from GameEngine import ClassGameEngine
            self.engine = ClassGameEngine()
            logger.info("✓ Real GameEngine loaded successfully!")
            logger.info(f"Engine initialized with game_statusID: {self.engine.game_statusID}")
        except ImportError as e:
            logger.error(f"❌ GameEngine import failed: {e}")
            logger.error("Make sure GameEngine.py is in the same directory as your GUI")
    
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
            f"Wits: {self.engine.actionpaths.get('Wits', 0)}",
            f"Fellowship: {self.engine.actionpaths.get('fellowship', 0)}",
            f"Journey: {self.engine.actionpaths.get('journey', 0)}",
            "",
            self.current_message
        ]
        logger.debug("get_status_text executed")
        return "\n".join(status_lines)
    
    def get_total_progress(self):
        """Get total progress from action paths"""
        total = sum(self.engine.actionpaths.values()) if hasattr(self.engine, 'actionpaths') else 0
        logger.debug(f"get_total_progress executed -> {total}")
        return total
    
    def get_actionpaths(self):
        """Get action paths dictionary"""
        paths = getattr(self.engine, 'actionpaths', {})
        logger.debug(f"get_actionpaths executed -> {paths}")
        return paths
    
    def get_player_card_count(self, card_name):
        """Get card count for active player"""
        count = 0
        if (hasattr(self.engine, 'playerData') and self.engine.playerData and 
            hasattr(self.engine, 'activePlayerID') and self.engine.activePlayerID > 0):
            
            player_key = f"player {self.engine.activePlayerID}"
            if (player_key in self.engine.playerData and 
                'actioncards' in self.engine.playerData[player_key]):
                count = self.engine.playerData[player_key]['actioncards'].get(card_name.lower(), 0)
        
        logger.debug(f"get_player_card_count executed for '{card_name}' -> {count}")
        return count
    
    def set_message(self, message):
        """Set the current status message"""
        self.current_message = message
        logger.info(f"set_message executed -> {message}")
    
    def append_message(self, message):
        """Append to the current status message"""
        self.current_message += f"\n{message}"
        logger.info(f"append_message executed -> {message}")
    
    def get_current_player_info(self):
        """Get detailed information about the current player"""
        if not hasattr(self.engine, 'playerData') or not self.engine.playerData:
            logger.debug("get_current_player_info -> no player data")
            return None
        
        player_key = f"player {self.engine.activePlayerID}"
        info = self.engine.playerData.get(player_key, None)
        logger.debug(f"get_current_player_info -> {info}")
        return info
    
    def is_game_initialized(self):
        """Check if the game is properly initialized"""
        initialized = (hasattr(self.engine, 'game_statusID') and 
                       self.engine.game_statusID >= 1000 and
                       hasattr(self.engine, 'numberOfPlayers') and
                       self.engine.numberOfPlayers > 0)
        logger.debug(f"is_game_initialized -> {initialized}")
        return initialized
    
    def is_game_active(self):
        """Check if the game is currently active"""
        active = self.is_game_initialized() and hasattr(self.engine, 'game_statusID') and self.engine.game_statusID > 0
        logger.debug(f"is_game_active -> {active}")
        return active
    
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
        logger.info("reset_game_state executed -> game state reset")

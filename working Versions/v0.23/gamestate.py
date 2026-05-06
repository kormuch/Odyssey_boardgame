# gamestate.py - Enhanced with generic threat system
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict
from gamelog import logger


class GameStatus(Enum):
    """Enumeration for game status values"""
    NOT_STARTED = 0
    INITIALIZED = 1
    RUNNING = 1000
    COMPLETED = -1
    
    @property
    def description(self):
        descriptions = {
            GameStatus.NOT_STARTED: "Game not started",
            GameStatus.INITIALIZED: "Game initialized but not running",
            GameStatus.RUNNING: "Game running",
            GameStatus.COMPLETED: "Game completed"
        }
        return descriptions.get(self, f"Unknown status: {self.value}")


@dataclass
class GameState:
    """Centralized game state management"""
    
    # Core game state
    status: GameStatus = GameStatus.INITIALIZED
    active_player_id: int = 1
    number_of_players: int = 0
    round_counter: int = 1
    
    # Action tracking
    action_cards_played: int = 0
    current_action_key: str = ""
    user_input_counter: int = 0
    
    # Action paths (quest progress)
    action_paths: Dict[str, int] = field(default_factory=lambda: {
        "battle": 0,
        "fellowship": 0,
        "wits": 0,
        "journey": 0
    })
    
    # NEW: Collision Track System
    # This represents a symmetric track where two markers approach each other
    # When they meet/cross, the game ends (loss condition)
    # 
    # Example themes:
    # - Odyssey: Left = Odysseus' hope, Right = Suitors closing in on Penelope
    # - LOTR: Left = Fellowship progress, Right = Sauron's corruption
    # - Pandemic: Left = Cure progress, Right = Disease spread
    # 
    # Left marker typically moves right (progress/damage)
    # Right marker typically moves left (countdown/threat advancing)
    track_length: int = 20              # Total positions on the track (0 to track_length)
    left_marker: int = 0                # Starts at position 0 (far left)
    right_marker: int = 20              # Starts at position track_length (far right)
    right_marker_advance_interval: int = 3  # Right marker advances every X rounds
    
    def __post_init__(self):
        logger.game_debug("GameState initialized with default values")
    
    def reset(self):
        """Reset game state to initial values"""
        old_status = self.status
        
        self.status = GameStatus.INITIALIZED
        self.active_player_id = 1
        self.round_counter = 1
        self.action_cards_played = 0
        self.current_action_key = ""
        self.user_input_counter = 0
        self.action_paths = {k: 0 for k in self.action_paths}
        
        # Reset collision track
        self.left_marker = 0
        self.right_marker = self.track_length
        
        logger.state_change("game_state", "full_reset", "initialized", old_status=old_status.description)
    
    def increment_round(self):
        """Increment round counter"""
        old_round = self.round_counter
        self.round_counter += 1
        logger.state_change("round", old_round, self.round_counter)
    
    def next_player(self, max_players: int) -> int:
        """Calculate and set next player ID"""
        old_player = self.active_player_id
        self.active_player_id = (self.active_player_id % max_players) + 1
        logger.state_change(
            "active_player",
            old_player,
            self.active_player_id,
            max_players=max_players
        )
        return self.active_player_id
    
    def record_action(self, action_key: str):
        """Record an action being played"""
        self.current_action_key = action_key
        self.action_cards_played += 1
        self.user_input_counter += 1
        
        logger.player_action(
            self.active_player_id,
            f"Action recorded: {action_key}",
            cards_played=self.action_cards_played,
            input_counter=self.user_input_counter
        )
    
    def reset_turn(self):
        """Reset turn-specific counters"""
        old_cards = self.action_cards_played
        self.action_cards_played = 0
        self.current_action_key = ""
        
        logger.game_debug(f"Turn reset: {old_cards} cards were played")
    
    # =============================================================================
    # COLLISION TRACK SYSTEM
    # =============================================================================
    
    def advance_right_marker(self, steps: int = 1):
        """Move right marker toward left (approaching collision)"""
        old_pos = self.right_marker
        self.right_marker = max(0, self.right_marker - steps)
        
        logger.state_change(
            "right_marker",
            old_pos,
            self.right_marker,
            steps=steps,
            distance=self.get_marker_distance()
        )
        
        if self.check_marker_collision():
            logger.warning("⚠️ MARKERS COLLIDED - GAME OVER CONDITION!")
        
        return self.right_marker
    
    def advance_left_marker(self, steps: int = 1):
        """Move left marker toward right (progress/damage)"""
        old_pos = self.left_marker
        self.left_marker = min(self.track_length, self.left_marker + steps)
        
        logger.state_change(
            "left_marker",
            old_pos,
            self.left_marker,
            steps=steps,
            distance=self.get_marker_distance()
        )
        
        if self.check_marker_collision():
            logger.warning("⚠️ MARKERS COLLIDED - GAME OVER CONDITION!")
        
        return self.left_marker
    
    def retreat_left_marker(self, steps: int = 1):
        """Move left marker back toward start (healing/recovery)"""
        old_pos = self.left_marker
        self.left_marker = max(0, self.left_marker - steps)
        
        logger.state_change(
            "left_marker",
            old_pos,
            self.left_marker,
            steps=steps,
            reason="healing/recovery"
        )
        
        return self.left_marker
    
    def get_marker_distance(self) -> int:
        """Get distance between left and right markers"""
        return self.right_marker - self.left_marker
    
    def check_marker_collision(self) -> bool:
        """Check if markers have collided (left >= right)"""
        return self.left_marker >= self.right_marker
    
    def should_right_marker_advance(self) -> bool:
        """Check if right marker should advance this round"""
        return self.round_counter % self.right_marker_advance_interval == 0
    
    def get_collision_track_status(self) -> dict:
        """Get current collision track status"""
        distance = self.get_marker_distance()
        collision = self.check_marker_collision()
        
        return {
            'left_position': self.left_marker,
            'right_position': self.right_marker,
            'distance': distance,
            'collision': collision,
            'track_length': self.track_length,
            'right_marker_progress_pct': int((1 - self.right_marker / self.track_length) * 100)
        }
    
    # =============================================================================
    # SERIALIZATION
    # =============================================================================
    
    def to_dict(self) -> dict:
        """Convert state to dictionary for serialization"""
        data = {
            'status': self.status.value,
            'status_meaning': self.status.description,
            'active_player_id': self.active_player_id,
            'number_of_players': self.number_of_players,
            'round_counter': self.round_counter,
            'action_cards_played': self.action_cards_played,
            'current_action_key': self.current_action_key,
            'user_input_counter': self.user_input_counter,
            'action_paths': self.action_paths.copy(),
            # Collision track data
            'track_length': self.track_length,
            'left_marker': self.left_marker,
            'right_marker': self.right_marker,
            'right_marker_advance_interval': self.right_marker_advance_interval
        }
        logger.game_debug(f"GameState serialized to dict (round={self.round_counter}, player={self.active_player_id})")
        return data
    
    @classmethod
    def from_dict(cls, data: dict) -> 'GameState':
        """Create GameState from dictionary"""
        state = cls()
        state.status = GameStatus(data.get('status', 1))
        state.active_player_id = data.get('active_player_id', 1)
        state.number_of_players = data.get('number_of_players', 0)
        state.round_counter = data.get('round_counter', 1)
        state.action_cards_played = data.get('action_cards_played', 0)
        state.current_action_key = data.get('current_action_key', "")
        state.user_input_counter = data.get('user_input_counter', 0)
        state.action_paths = data.get('action_paths', state.action_paths)
        
        # Load collision track data
        state.track_length = data.get('track_length', 20)
        state.left_marker = data.get('left_marker', 0)
        state.right_marker = data.get('right_marker', 20)
        state.right_marker_advance_interval = data.get('right_marker_advance_interval', 3)
        
        logger.info(f"GameState loaded: round {state.round_counter}, player {state.active_player_id}, status={state.status.description}")
        logger.info(f"Collision track: Left@{state.left_marker}, Right@{state.right_marker}, Distance={state.get_marker_distance()}")
        return state
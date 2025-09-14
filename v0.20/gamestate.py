from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, Optional

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
    
    # Action paths
    action_paths: Dict[str, int] = field(default_factory=lambda: {
        "battle": 0,
        "fellowship": 0,
        "wits": 0,
        "journey": 0
    })
    
    def reset(self):
        """Reset game state to initial values"""
        self.status = GameStatus.INITIALIZED
        self.active_player_id = 1
        self.round_counter = 1
        self.action_cards_played = 0
        self.current_action_key = ""
        self.user_input_counter = 0
        self.action_paths = {
            "battle": 0,
            "fellowship": 0,
            "wits": 0,
            "journey": 0
        }
    
    def increment_round(self):
        """Increment round counter"""
        self.round_counter += 1
    
    def next_player(self, max_players: int) -> int:
        """Calculate and set next player ID"""
        self.active_player_id = (self.active_player_id % max_players) + 1
        return self.active_player_id
    
    def record_action(self, action_key: str):
        """Record an action being played"""
        self.current_action_key = action_key
        self.action_cards_played += 1
        self.user_input_counter += 1
    
    def reset_turn(self):
        """Reset turn-specific counters"""
        self.action_cards_played = 0
        self.current_action_key = ""
    
    def to_dict(self) -> dict:
        """Convert state to dictionary for serialization"""
        return {
            'status': self.status.value,
            'status_meaning': self.status.description,
            'active_player_id': self.active_player_id,
            'number_of_players': self.number_of_players,
            'round_counter': self.round_counter,
            'action_cards_played': self.action_cards_played,
            'current_action_key': self.current_action_key,
            'user_input_counter': self.user_input_counter,
            'action_paths': self.action_paths.copy()
        }
    
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
        return state
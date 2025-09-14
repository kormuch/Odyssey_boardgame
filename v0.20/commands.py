# commands.py - Simplified version for smooth integration
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

class Command(ABC):
    """Abstract base class for all game commands"""
    
    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> Any:
        """Execute the command with given context"""
        pass
    
    @abstractmethod
    def can_execute(self, context: Dict[str, Any]) -> bool:
        """Check if command can be executed in current context"""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Get command description"""
        pass

class QuitCommand(Command):
    """Command to quit the game"""
    
    def execute(self, context: Dict[str, Any]) -> Any:
        from gamestate import GameStatus
        game_state = context['game_state']
        game_state.status = GameStatus.COMPLETED
        return "Game ended by user"
    
    def can_execute(self, context: Dict[str, Any]) -> bool:
        return True
    
    @property
    def description(self) -> str:
        return "Quit the game"

class SkipTurnCommand(Command):
    """Command to skip current turn"""
    
    def execute(self, context: Dict[str, Any]) -> Any:
        game_state = context['game_state']
        game_state.current_action_key = "skip"
        game_state.user_input_counter += 1
        game_state.action_cards_played = 2  # Force turn end
        return "Turn skipped"
    
    def can_execute(self, context: Dict[str, Any]) -> bool:
        from gamestate import GameStatus
        game_state = context['game_state']
        # Can skip if game is running or initialized
        return game_state.status in [GameStatus.RUNNING, GameStatus.INITIALIZED]
    
    @property
    def description(self) -> str:
        return "Skip current turn"

class PlayCardCommand(Command):
    """Command to play an action card"""
    
    def __init__(self, card_name: str):
        self.card_name = card_name
    
    def execute(self, context: Dict[str, Any]) -> Any:
        # Note: The actual card playing is still handled by update_actioncards
        # This command just validates and prepares the action
        return {
            'success': True,
            'card_name': self.card_name,
            'action': 'play_card'
        }
    
    def can_execute(self, context: Dict[str, Any]) -> bool:
        from gamestate import GameStatus
        game_state = context['game_state']
        active_player = context.get('active_player')
        
        # Can play cards if game is running/initialized and we have an active player
        return (game_state.status in [GameStatus.RUNNING, GameStatus.INITIALIZED] and 
                active_player is not None and
                game_state.action_cards_played < 2)
    
    @property
    def description(self) -> str:
        return f"Play action card: {self.card_name}"

class CommandManager:
    """Manages and executes game commands"""
    
    def __init__(self, card_manager):
        self.card_manager = card_manager
        self.commands: Dict[str, Command] = {}
        self._register_default_commands()
    
    def _register_default_commands(self):
        """Register default game commands"""
        # Register quit command
        quit_cmd = QuitCommand()
        self.commands['quit'] = quit_cmd
        self.commands['q'] = quit_cmd
        
        # Register skip command
        skip_cmd = SkipTurnCommand()
        self.commands['skip'] = skip_cmd
        self.commands['s'] = skip_cmd
    
    def parse_input(self, user_input: str) -> Optional[Command]:
        """Parse user input and return appropriate command"""
        if not user_input:
            return None
            
        input_lower = user_input.lower().strip()
        
        # Check for registered commands first
        if input_lower in self.commands:
            return self.commands[input_lower]
        
        # Check if it's a card play command
        if self.card_manager.validate_input(user_input):
            card_name = self.card_manager.resolve_input_to_card_name(user_input)
            if card_name:
                return PlayCardCommand(card_name)
        
        return None
    
    def execute_command(self, command: Command, context: Dict[str, Any]) -> Any:
        """Execute a command with validation"""
        if command.can_execute(context):
            return command.execute(context)
        else:
            return {'success': False, 'reason': 'Command cannot be executed in current context'}
    
    def get_available_commands(self, context: Dict[str, Any]) -> Dict[str, str]:
        """Get list of currently available commands"""
        available = {}
        for alias, command in self.commands.items():
            if command.can_execute(context):
                # Only show primary aliases (skip 'q' and 's')
                if alias in ['quit', 'skip']:
                    available[alias] = command.description
        return available
    
    def register_command(self, aliases: list, command: Command):
        """Register a custom command with given aliases"""
        for alias in aliases:
            self.commands[alias.lower()] = command
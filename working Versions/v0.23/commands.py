#commands.py
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from gamelog import logger

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
        logger.info("QuitCommand executed - game ending")
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
        player_id = game_state.active_player_id
        
        game_state.current_action_key = "skip"
        game_state.user_input_counter += 1
        game_state.action_cards_played = 2  # Force turn end
        
        logger.player_action(
            player_id,
            "Turn skipped",
            user_input_counter=game_state.user_input_counter
        )
        return "Turn skipped"

    def can_execute(self, context: Dict[str, Any]) -> bool:
        from gamestate import GameStatus
        game_state = context['game_state']
        return game_state.status in [GameStatus.RUNNING, GameStatus.INITIALIZED]

    @property
    def description(self) -> str:
        return "Skip current turn"

class PlayCardCommand(Command):
    """Command to play an action card"""

    def __init__(self, card_name: str):
        self.card_name = card_name

    def execute(self, context: Dict[str, Any]) -> Any:
        logger.game_debug(f"PlayCardCommand.execute for '{self.card_name}'")
        return {
            'success': True,
            'card_name': self.card_name,
            'action': 'play_card'
        }

    def can_execute(self, context: Dict[str, Any]) -> bool:
        from gamestate import GameStatus
        game_state = context['game_state']
        active_player = context.get('active_player')
        
        can_execute = (
            game_state.status in [GameStatus.RUNNING, GameStatus.INITIALIZED] and
            active_player is not None and
            game_state.action_cards_played < 2
        )
        
        if not can_execute:
            logger.game_debug(f"PlayCardCommand for '{self.card_name}' cannot execute - conditions not met")
        
        return can_execute

    @property
    def description(self) -> str:
        return f"Play action card: {self.card_name}"

class CommandManager:
    """Manages and executes game commands"""

    def __init__(self, card_manager):
        self.card_manager = card_manager
        self.commands: Dict[str, Command] = {}
        self._register_default_commands()
        logger.info(f"CommandManager initialized with {len(self.commands)} command aliases")

    def _register_default_commands(self):
        """Register default game commands"""
        quit_cmd = QuitCommand()
        self.commands['quit'] = quit_cmd
        self.commands['q'] = quit_cmd

        skip_cmd = SkipTurnCommand()
        self.commands['skip'] = skip_cmd
        self.commands['s'] = skip_cmd

    def parse_input(self, user_input: str) -> Optional[Command]:
        """Parse user input and return appropriate command"""
        if not user_input:
            return None

        input_lower = user_input.lower().strip()

        # Check for system commands first
        if input_lower in self.commands:
            logger.game_debug(f"Input '{user_input}' matched command: {self.commands[input_lower].description}")
            return self.commands[input_lower]

        # Check for card play commands
        if self.card_manager.validate_input(user_input):
            card_name = self.card_manager.resolve_input_to_card_name(user_input)
            if card_name:
                logger.game_debug(f"Input '{user_input}' resolved to PlayCardCommand: '{card_name}'")
                return PlayCardCommand(card_name)

        logger.game_debug(f"No command matched for input: '{user_input}'")
        return None

    def execute_command(self, command: Command, context: Dict[str, Any]) -> Any:
        """Execute a command with validation"""
        if command.can_execute(context):
            result = command.execute(context)
            logger.info(f"Command executed: {command.description}")
            return result
        else:
            logger.warning(f"Command blocked: {command.description} (cannot execute in current context)")
            return {'success': False, 'reason': 'Command cannot be executed in current context'}

    def get_available_commands(self, context: Dict[str, Any]) -> Dict[str, str]:
        """Get list of currently available commands"""
        available = {}
        for alias, command in self.commands.items():
            if command.can_execute(context) and alias in ['quit', 'skip']:
                available[alias] = command.description
        return available

    def register_command(self, aliases: list, command: Command):
        """Register a custom command with given aliases"""
        for alias in aliases:
            self.commands[alias.lower()] = command
        logger.info(f"Custom command registered: '{command.description}' with aliases {aliases}")
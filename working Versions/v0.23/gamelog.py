# gamelog.py
import logging
import sys
import os
from datetime import datetime, timedelta
from pathlib import Path


class GameLogger:
    """Enhanced game logger with structured logging and cleanup capabilities"""
    
    def __init__(self, debug_ui=False, debug_game=True, keep_logs_days=7):
        self.debug_ui = debug_ui
        self.debug_game = debug_game
        self.keep_logs_days = keep_logs_days
        self.logger = self._setup_logger()
        self._cleanup_old_logs()
    
    def _setup_logger(self):
        """Configure a unique logger for each session"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_filename = log_dir / f"game_{timestamp}.log"

        logger = logging.getLogger("game_logger")
        logger.setLevel(logging.DEBUG)

        if logger.hasHandlers():
            logger.handlers.clear()

        # File handler (everything goes here)
        fh = logging.FileHandler(log_filename, mode='w', encoding='utf-8')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%H:%M:%S"
        ))

        # Console handler (INFO+)
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.INFO)
        ch.setFormatter(logging.Formatter(
            "%(asctime)s [%(levelname)s]: %(message)s",
            datefmt="%H:%M:%S"
        ))

        logger.addHandler(fh)
        logger.addHandler(ch)

        # Redirect print() to logger at INFO level
        import builtins
        original_print = builtins.print
        
        def logging_print(*args, **kwargs):
            message = " ".join(map(str, args))
            logger.info(message)
        
        builtins.print = logging_print
        builtins._original_print = original_print  # Keep reference to original

        logger.info(f"=== Logging started - file: {log_filename} ===")
        logger.info(f"Debug UI: {self.debug_ui}, Debug Game: {self.debug_game}")
        return logger
    
    def _cleanup_old_logs(self):
        """Remove log files older than keep_logs_days"""
        if self.keep_logs_days <= 0:
            return
        
        log_dir = Path("logs")
        if not log_dir.exists():
            return
        
        cutoff = datetime.now() - timedelta(days=self.keep_logs_days)
        removed_count = 0
        
        for logfile in log_dir.glob("game_*.log"):
            try:
                file_time = datetime.fromtimestamp(logfile.stat().st_mtime)
                if file_time < cutoff:
                    logfile.unlink()
                    removed_count += 1
            except Exception as e:
                self.logger.warning(f"Could not remove old log {logfile}: {e}")
        
        if removed_count > 0:
            self.logger.info(f"Cleaned up {removed_count} old log file(s)")
    
    def game_event(self, event_type, **kwargs):
        """Structured logging for game events"""
        details = " | ".join(f"{k}={v}" for k, v in kwargs.items())
        msg = f"[GAME_EVENT: {event_type}] {details}"
        self.logger.info(msg)
    
    def player_action(self, player_id, action, **kwargs):
        """Log player actions with context"""
        details = " | ".join(f"{k}={v}" for k, v in kwargs.items())
        msg = f"[PLAYER_{player_id}] {action}"
        if details:
            msg += f" | {details}"
        self.logger.info(msg)
    
    def state_change(self, component, old_value, new_value, **kwargs):
        """Log state changes"""
        msg = f"[STATE_CHANGE: {component}] {old_value} → {new_value}"
        if kwargs:
            details = " | ".join(f"{k}={v}" for k, v in kwargs.items())
            msg += f" | {details}"
        self.logger.info(msg)
    
    def ui_debug(self, message):
        """Log UI debug info only if debug_ui is enabled"""
        if self.debug_ui:
            self.logger.debug(f"[UI] {message}")
    
    def game_debug(self, message):
        """Log game debug info only if debug_game is enabled"""
        if self.debug_game:
            self.logger.debug(f"[GAME] {message}")
    
    # Convenience methods that match standard logger interface
    def debug(self, message):
        self.logger.debug(message)
    
    def info(self, message):
        self.logger.info(message)
    
    def warning(self, message):
        self.logger.warning(message)
    
    def error(self, message):
        self.logger.error(message)
    
    def exception(self, message):
        self.logger.exception(message)


def setup_logger(debug_ui=False, debug_game=True, keep_logs_days=7):
    """
    Configure a unique logger for each session.
    
    Args:
        debug_ui (bool): If True, logs detailed UI info (button rects, hover states, etc.)
        debug_game (bool): If True, logs detailed game logic info
        keep_logs_days (int): Number of days to keep old logs (0 = keep all)
    
    Returns:
        GameLogger instance
    """
    return GameLogger(debug_ui=debug_ui, debug_game=debug_game, keep_logs_days=keep_logs_days)


# Create logger instance with sensible defaults for development
logger = setup_logger(debug_ui=False, debug_game=True, keep_logs_days=7)
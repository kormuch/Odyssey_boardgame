# persistance.py
import json
import os
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path
import logging
logger = logging.getLogger(__name__)


class PersistenceManager:
    """Handles all game data persistence operations"""
    
    def __init__(self, save_directory: str = "saves"):
        self.save_directory = Path(save_directory)
        self.save_directory.mkdir(exist_ok=True)
        self.current_save_file = "playerdata.json"
        logger.info(f"PersistenceManager initialized at {self.save_directory}")
    
    def save_game_state(self, game_data: Dict[str, Any], filename: Optional[str] = None) -> bool:
        if filename is None:
            filename = self.current_save_file
        
        filepath = self.save_directory / filename
        
        try:
            save_data = {
                'metadata': {
                    'version': '1.0.0',
                    'timestamp': datetime.now().isoformat(),
                    'save_type': 'full_game_state'
                },
                'game_state': game_data.get('game_state', {}),
                'players': game_data.get('players', {}),
                'settings': game_data.get('settings', {})
            }
            
            with open(filepath, 'w') as f:
                json.dump(save_data, f, indent=4)
            
            logger.info(f"Game state saved to '{filepath}'")
            return True
        except Exception as e:
            logger.error(f"Error saving game state to '{filepath}': {e}")
            return False
    
    def load_game_state(self, filename: Optional[str] = None) -> Optional[Dict[str, Any]]:
        if filename is None:
            filename = self.current_save_file
        
        filepath = self.save_directory / filename
        
        try:
            if not filepath.exists():
                logger.warning(f"Save file '{filepath}' not found")
                return None
            
            with open(filepath, 'r') as f:
                save_data = json.load(f)
            
            if not self._validate_save_data(save_data):
                logger.error(f"Invalid save file format: {filepath}")
                return None
            
            logger.info(f"Game state loaded from '{filepath}'")
            return save_data
        except Exception as e:
            logger.error(f"Error loading game state from '{filepath}': {e}")
            return None
    
    def _validate_save_data(self, save_data: Dict) -> bool:
        required_keys = ['metadata', 'game_state', 'players']
        valid = all(key in save_data for key in required_keys)
        if not valid:
            logger.warning("Save data missing required keys")
        return valid
    
    def create_autosave(self, game_data: Dict[str, Any]) -> bool:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"autosave_{timestamp}.json"
        success = self.save_game_state(game_data, filename)
        if success:
            logger.info(f"Autosave created: {filename}")
        return success
    
    def list_save_files(self) -> List[Dict[str, Any]]:
        saves = []
        for filepath in self.save_directory.glob("*.json"):
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    
                saves.append({
                    'filename': filepath.name,
                    'timestamp': data.get('metadata', {}).get('timestamp', 'Unknown'),
                    'version': data.get('metadata', {}).get('version', 'Unknown'),
                    'players': len(data.get('players', {}))
                })
            except Exception:
                logger.warning(f"Skipping invalid save file: {filepath}")
                continue
        
        return sorted(saves, key=lambda x: x['timestamp'], reverse=True)
    
    def delete_save(self, filename: str) -> bool:
        filepath = self.save_directory / filename
        
        try:
            if filepath.exists():
                filepath.unlink()
                logger.info(f"Save file '{filename}' deleted")
                return True
            else:
                logger.warning(f"Save file '{filename}' not found")
                return False
        except Exception as e:
            logger.error(f"Error deleting save file '{filename}': {e}")
            return False
    
    def export_game_data(self, game_data: Dict[str, Any], export_path: str) -> bool:
        try:
            with open(export_path, 'w') as f:
                json.dump(game_data, f, indent=4)
            logger.info(f"Game data exported to '{export_path}'")
            return True
        except Exception as e:
            logger.error(f"Error exporting game data to '{export_path}': {e}")
            return False
    
    def import_game_data(self, import_path: str) -> Optional[Dict[str, Any]]:
        try:
            with open(import_path, 'r') as f:
                data = json.load(f)
            
            if self._validate_save_data(data):
                logger.info(f"Game data imported from '{import_path}'")
                return data
            else:
                logger.error(f"Invalid import file format: {import_path}")
                return None
        except Exception as e:
            logger.error(f"Error importing game data from '{import_path}': {e}")
            return None


class SaveManager:
    """High-level save management interface"""
    
    def __init__(self, persistence_manager: PersistenceManager):
        self.persistence = persistence_manager
        self.autosave_enabled = True
        self.autosave_interval = 5  # rounds
        logger.info("SaveManager initialized")
    
    def save_game(self, game_engine) -> bool:
        game_data = {
            'game_state': game_engine.state.to_dict(),
            'players': game_engine.get_player_data(),
            'settings': {
                'autosave_enabled': self.autosave_enabled,
                'autosave_interval': self.autosave_interval
            }
        }
        return self.persistence.save_game_state(game_data)
    
    def load_game(self, game_engine, filename: Optional[str] = None) -> bool:
        save_data = self.persistence.load_game_state(filename)
        if save_data:
            from gamestate import GameState
            game_engine.state = GameState.from_dict(save_data['game_state'])
            
            from player import Player
            game_engine.players = []
            for key, player_data in save_data['players'].items():
                player = Player.from_dict(player_data, game_engine.card_manager)
                game_engine.players.append(player)
            
            settings = save_data.get('settings', {})
            self.autosave_enabled = settings.get('autosave_enabled', True)
            self.autosave_interval = settings.get('autosave_interval', 5)
            
            logger.info(f"Game loaded successfully from '{filename or self.persistence.current_save_file}'")
            return True
        
        logger.warning(f"Failed to load game from '{filename or self.persistence.current_save_file}'")
        return False
    
    def check_autosave(self, game_engine) -> None:
        if self.autosave_enabled:
            if game_engine.state.round_counter % self.autosave_interval == 0:
                self.persistence.create_autosave({
                    'game_state': game_engine.state.to_dict(),
                    'players': game_engine.get_player_data(),
                    'settings': {
                        'autosave_enabled': self.autosave_enabled,
                        'autosave_interval': self.autosave_interval
                    }
                })

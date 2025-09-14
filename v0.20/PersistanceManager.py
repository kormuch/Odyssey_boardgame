import json
import os
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path

class PersistenceManager:
    """Handles all game data persistence operations"""
    
    def __init__(self, save_directory: str = "saves"):
        self.save_directory = Path(save_directory)
        self.save_directory.mkdir(exist_ok=True)
        self.current_save_file = "playerdata.json"
    
    def save_game_state(self, game_data: Dict[str, Any], filename: Optional[str] = None) -> bool:
        """
        Save complete game state to file
        
        Args:
            game_data: Dictionary containing all game data
            filename: Optional custom filename
            
        Returns:
            bool: Success status
        """
        if filename is None:
            filename = self.current_save_file
        
        filepath = self.save_directory / filename
        
        try:
            # Add metadata
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
            
            print(f"Game state saved to '{filepath}'")
            return True
            
        except Exception as e:
            print(f"Error saving game state: {e}")
            return False
    
    def load_game_state(self, filename: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Load game state from file
        
        Args:
            filename: Optional custom filename
            
        Returns:
            Dict or None: Loaded game data or None if failed
        """
        if filename is None:
            filename = self.current_save_file
        
        filepath = self.save_directory / filename
        
        try:
            if not filepath.exists():
                print(f"Save file '{filepath}' not found")
                return None
            
            with open(filepath, 'r') as f:
                save_data = json.load(f)
            
            # Validate save data structure
            if not self._validate_save_data(save_data):
                print("Invalid save file format")
                return None
            
            print(f"Game state loaded from '{filepath}'")
            return save_data
            
        except Exception as e:
            print(f"Error loading game state: {e}")
            return None
    
    def _validate_save_data(self, save_data: Dict) -> bool:
        """Validate loaded save data structure"""
        required_keys = ['metadata', 'game_state', 'players']
        return all(key in save_data for key in required_keys)
    
    def create_autosave(self, game_data: Dict[str, Any]) -> bool:
        """Create an autosave with timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"autosave_{timestamp}.json"
        return self.save_game_state(game_data, filename)
    
    def list_save_files(self) -> List[Dict[str, Any]]:
        """
        List all available save files with metadata
        
        Returns:
            List of save file information
        """
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
            except:
                # Skip invalid files
                continue
        
        return sorted(saves, key=lambda x: x['timestamp'], reverse=True)
    
    def delete_save(self, filename: str) -> bool:
        """Delete a save file"""
        filepath = self.save_directory / filename
        
        try:
            if filepath.exists():
                filepath.unlink()
                print(f"Save file '{filename}' deleted")
                return True
            else:
                print(f"Save file '{filename}' not found")
                return False
        except Exception as e:
            print(f"Error deleting save file: {e}")
            return False
    
    def export_game_data(self, game_data: Dict[str, Any], export_path: str) -> bool:
        """Export game data to external location"""
        try:
            with open(export_path, 'w') as f:
                json.dump(game_data, f, indent=4)
            print(f"Game data exported to '{export_path}'")
            return True
        except Exception as e:
            print(f"Error exporting game data: {e}")
            return False
    
    def import_game_data(self, import_path: str) -> Optional[Dict[str, Any]]:
        """Import game data from external location"""
        try:
            with open(import_path, 'r') as f:
                data = json.load(f)
            
            if self._validate_save_data(data):
                print(f"Game data imported from '{import_path}'")
                return data
            else:
                print("Invalid import file format")
                return None
        except Exception as e:
            print(f"Error importing game data: {e}")
            return None

class SaveManager:
    """High-level save management interface"""
    
    def __init__(self, persistence_manager: PersistenceManager):
        self.persistence = persistence_manager
        self.autosave_enabled = True
        self.autosave_interval = 5  # rounds
    
    def save_game(self, game_engine) -> bool:
        """Save complete game state from engine"""
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
        """Load game state into engine"""
        save_data = self.persistence.load_game_state(filename)
        
        if save_data:
            # Reconstruct game state
            from gamestate import GameState
            game_engine.state = GameState.from_dict(save_data['game_state'])
            
            # Reconstruct players
            from player import Player
            game_engine.players = []
            for key, player_data in save_data['players'].items():
                player = Player.from_dict(player_data, game_engine.card_manager)
                game_engine.players.append(player)
            
            # Apply settings
            settings = save_data.get('settings', {})
            self.autosave_enabled = settings.get('autosave_enabled', True)
            self.autosave_interval = settings.get('autosave_interval', 5)
            
            return True
        return False
    
    def check_autosave(self, game_engine) -> None:
        """Check if autosave should be triggered"""
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
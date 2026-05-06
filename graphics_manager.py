# graphics_manager.py
import pygame
import os
from gamelog import logger


class GraphicsManager:
    """Handles loading and managing game graphics"""
    
    def __init__(self):
        self.images = {}
        logger.info("GraphicsManager initializing...")
        self.load_graphics()
        logger.info(f"GraphicsManager ready with {len(self.images)} images loaded")
    
    def load_graphics(self):
        """Load game graphics with error handling"""
        graphics_files = {
            "odysseus": os.path.join("gamegraphics", "odysseus_01.png"),
            "background_01": os.path.join("gamegraphics", "background_01.png"),
            "actioncard battle 01": os.path.join("gamegraphics", "actioncard battle 01.png"),
            "actioncard fellowship 01": os.path.join("gamegraphics", "actioncard fellowship 01.png"),
            "actioncard journey 01": os.path.join("gamegraphics", "actioncard journey 01.png"),
            "actioncard wits 01": os.path.join("gamegraphics", "actioncard wits 01.png"),
        }
        
        loaded_count = 0
        placeholder_count = 0
        
        for name, filepath in graphics_files.items():
            try:
                if os.path.exists(filepath):
                    image = pygame.image.load(filepath)
                    # convert to display format (preserve alpha when present)
                    try:
                        image = image.convert_alpha()
                    except Exception:
                        image = image.convert()
                    self.images[name] = image
                    loaded_count += 1
                    logger.game_debug(f"Loaded image: {name} from {filepath}")
                else:
                    logger.warning(f"Image file not found: {filepath}")
                    self.images[name] = self._create_placeholder((100, 100), (255, 0, 255))
                    placeholder_count += 1
                    logger.game_debug(f"Created placeholder for: {name}")
            except pygame.error as e:
                logger.error(f"Failed to load {filepath}: {e}")
                self.images[name] = self._create_placeholder((100, 100), (255, 0, 0))
                placeholder_count += 1
        
        logger.info(f"Graphics loaded: {loaded_count} actual, {placeholder_count} placeholders")
    
    def _create_placeholder(self, size, color):
        """Create a colored placeholder surface"""
        placeholder = pygame.Surface(size)
        placeholder.fill(color)
        try:
            return placeholder.convert_alpha()
        except Exception:
            return placeholder.convert()
    
    def get_image(self, name):
        """Get an image by name"""
        img = self.images.get(name)
        if not img:
            logger.warning(f"Requested image not found: {name}")
        return img
    
    def add_image(self, name, filepath):
        """Add a new image to the manager"""
        try:
            if os.path.exists(filepath):
                image = pygame.image.load(filepath)
                try:
                    image = image.convert_alpha()
                except Exception:
                    image = image.convert()
                self.images[name] = image
                logger.info(f"Image added: {name} from {filepath}")
                return True
            else:
                logger.warning(f"Cannot add image - file not found: {filepath}")
                return False
        except pygame.error as e:
            logger.error(f"Failed to add image {filepath}: {e}")
            return False
    
    def list_loaded_images(self):
        """Return list of loaded image names"""
        return list(self.images.keys())
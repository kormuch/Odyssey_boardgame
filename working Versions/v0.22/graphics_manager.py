# graphics_manager.py
import pygame
import os
import logging
logger = logging.getLogger(__name__)


class GraphicsManager:
    """Handles loading and managing game graphics"""
    
    def __init__(self):
        self.images = {}
        self.load_graphics()
    
    def load_graphics(self):
        """Load game graphics with error handling"""
        graphics_files = {
            "odysseus": os.path.join("gamegraphics", "odysseus_01.png"),
            # Add more images here as needed
        }
        
        for name, filepath in graphics_files.items():
            try:
                if os.path.exists(filepath):
                    image = pygame.image.load(filepath)
                    self.images[name] = image
                    logger.info(f"✓ Loaded {name}: {filepath}")
                else:
                    logger.warning(f"❌ File not found: {filepath}")
                    self.images[name] = self._create_placeholder((100, 100), (255, 0, 255))
                    logger.info(f"  Created placeholder for {name}")
            except pygame.error as e:
                logger.error(f"❌ Error loading {filepath}: {e}")
                self.images[name] = self._create_placeholder((100, 100), (255, 0, 0))
    
    def _create_placeholder(self, size, color):
        """Create a colored placeholder surface"""
        placeholder = pygame.Surface(size)
        placeholder.fill(color)
        logger.debug(f"Created placeholder surface of size {size} with color {color}")
        return placeholder
    
    def get_image(self, name):
        """Get an image by name"""
        img = self.images.get(name)
        if img:
            logger.debug(f"Retrieved image: {name}")
        else:
            logger.warning(f"Image not found: {name}")
        return img
    
    def add_image(self, name, filepath):
        """Add a new image to the manager"""
        try:
            if os.path.exists(filepath):
                image = pygame.image.load(filepath)
                self.images[name] = image
                logger.info(f"✓ Added {name}: {filepath}")
                return True
            else:
                logger.warning(f"❌ File not found: {filepath}")
                return False
        except pygame.error as e:
            logger.error(f"❌ Error loading {filepath}: {e}")
            return False
    
    def list_loaded_images(self):
        """Return list of loaded image names"""
        image_list = list(self.images.keys())
        logger.debug(f"Loaded images: {image_list}")
        return image_list

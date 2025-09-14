import pygame
import os

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
                    print(f"✓ Loaded {name}: {filepath}")
                else:
                    print(f"❌ File not found: {filepath}")
                    self.images[name] = self._create_placeholder((100, 100), (255, 0, 255))
                    print(f"  Created placeholder for {name}")
            except pygame.error as e:
                print(f"❌ Error loading {filepath}: {e}")
                self.images[name] = self._create_placeholder((100, 100), (255, 0, 0))
    
    def _create_placeholder(self, size, color):
        """Create a colored placeholder surface"""
        placeholder = pygame.Surface(size)
        placeholder.fill(color)
        return placeholder
    
    def get_image(self, name):
        """Get an image by name"""
        return self.images.get(name)
    
    def add_image(self, name, filepath):
        """Add a new image to the manager"""
        try:
            if os.path.exists(filepath):
                image = pygame.image.load(filepath)
                self.images[name] = image
                print(f"✓ Added {name}: {filepath}")
                return True
            else:
                print(f"❌ File not found: {filepath}")
                return False
        except pygame.error as e:
            print(f"❌ Error loading {filepath}: {e}")
            return False
    
    def list_loaded_images(self):
        """Return list of loaded image names"""
        return list(self.images.keys())
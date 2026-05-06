# ui_renderer.py
import pygame
from gamelog import logger

class UIRenderer:
    """Handles all UI rendering operations"""
    
    def __init__(self, screen, graphics_manager):
        self.screen = screen
        self.graphics = graphics_manager
        self.WIDTH, self.HEIGHT = screen.get_size()
        
        # Colors
        self.BACKGROUND_COLOR = (152, 251, 152)
        self.PROGRESS_BAR_COLOR = (255, 255, 255)
        self.PATH_COLOR = (255, 255, 255)
        self.BUTTON_COLOR = (255, 255, 255)
        self.BUTTON_HOVER_COLOR = (200, 200, 200)
        
        # Fonts
        self.button_font = pygame.font.Font(None, 24)
        self.textbox_font = pygame.font.Font(None, 18)
        self.small_font = pygame.font.Font(None, 18)
        self.large_font = pygame.font.Font(None, 36)

        # Track last states to avoid redundant logs
        self.last_progress = -1
        self.last_paths = {}
        
        logger.info(f"UIRenderer initialized: {self.WIDTH}x{self.HEIGHT}")
    
    # ==============================
    # IMAGE DRAWING
    # ==============================
    
    def draw_image_space(self):
        """Draws the image space with loaded graphics"""
        image_space_height = self.HEIGHT // 3
        image_space_rect = pygame.Rect(self.WIDTH // 4, 0, self.WIDTH // 2, image_space_height)
        pygame.draw.rect(self.screen, (0, 0, 0), image_space_rect)
        
        odysseus_image = self.graphics.get_image("odysseus")
        if odysseus_image:
            self._draw_scaled_image(odysseus_image, image_space_rect)
    
    def _draw_scaled_image(self, image, container_rect):
        """Draw image scaled to fit container while maintaining aspect ratio"""
        image_rect = image.get_rect()
        scale_x = (container_rect.width - 20) / image_rect.width
        scale_y = (container_rect.height - 20) / image_rect.height
        scale = min(scale_x, scale_y, 1.0)
        
        if scale < 1.0:
            new_width = int(image_rect.width * scale)
            new_height = int(image_rect.height * scale)
            scaled_image = pygame.transform.scale(image, (new_width, new_height))
        else:
            scaled_image = image
        
        scaled_rect = scaled_image.get_rect(center=container_rect.center)
        self.screen.blit(scaled_image, scaled_rect)
    
    # ==============================
    # TEXTBOXES
    # ==============================
    
    def draw_textbox(self, text, position=None):
        """Draws a textbox with the given text"""
        lines = text.split('\n')
        line_height = 20
        total_height = len(lines) * line_height + 10
        max_width = max(self.textbox_font.size(line)[0] for line in lines)
        textbox_width = max_width + 10
        
        if position is None:
            # Default bottom-right position
            textbox_x = self.WIDTH - textbox_width - self.WIDTH * 0.1
            textbox_y = self.HEIGHT - total_height - self.HEIGHT * 3/5 - 10
        else:
            textbox_x, textbox_y = position
        
        textbox_rect = pygame.Rect(textbox_x, textbox_y, textbox_width, total_height)
        pygame.draw.rect(self.screen, (255, 255, 255), textbox_rect)
        pygame.draw.rect(self.screen, (0, 0, 0), textbox_rect, 2)
        
        for i, line in enumerate(lines):
            text_surface = self.textbox_font.render(line, True, (0, 0, 0))
            self.screen.blit(text_surface, (textbox_x + 5, textbox_y + 5 + i * line_height))
    
    # ==============================
    # PROGRESS & PATHS
    # ==============================
    
    def draw_progress_bar(self, total_progress):
        """Draws the progress bar with highlighting"""
        # Only log when progress actually changes
        if total_progress != self.last_progress:
            logger.info(f"Progress updated: {self.last_progress} → {total_progress}")
            self.last_progress = total_progress

        progress_bar_y = (self.HEIGHT // 3) + 50
        for step in range(1, 21):
            fill_color = (0, 255, 0) if step <= total_progress else self.PROGRESS_BAR_COLOR
            rect = pygame.Rect(step * (self.WIDTH // 22), progress_bar_y, self.WIDTH // 20, 20)
            pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)
            inner_rect = pygame.Rect(rect.x + 1, rect.y + 1, rect.width - 2, rect.height - 2)
            pygame.draw.rect(self.screen, fill_color, inner_rect)
    
    def draw_paths(self, actionpaths):
        """Draws four paths with progress indicators"""
        # Only log when paths actually change
        if actionpaths != self.last_paths:
            changes = []
            for path_name in ["battle", "wits", "fellowship", "journey"]:
                old_val = self.last_paths.get(path_name, 0)
                new_val = actionpaths.get(path_name, 0)
                if old_val != new_val:
                    changes.append(f"{path_name}: {old_val}→{new_val}")
            
            if changes:
                logger.info(f"Paths updated: {', '.join(changes)}")
            self.last_paths = actionpaths.copy()
        
        path_start_y = (self.HEIGHT // 3) + 140
        path_spacing = 60
        path_offset_x = 50
        path_names = ["battle", "wits", "fellowship", "journey"]
        colors = [(255, 100, 100), (100, 255, 100), (100, 100, 255), (255, 255, 100)]
        
        for path in range(4):
            path_name = path_names[path]
            path_progress = actionpaths.get(path_name, 0)
            label = self.button_font.render(path_name.capitalize(), True, (0, 0, 0))
            label_y = path_start_y + path * path_spacing - 35
            self.screen.blit(label, (path_offset_x, label_y))
            
            for step in range(1, 11):
                circle_x = step * (self.WIDTH // 25) + path_offset_x
                circle_y = path_start_y + path * path_spacing
                color = colors[path] if step <= path_progress else self.PATH_COLOR
                pygame.draw.circle(self.screen, color, (circle_x, circle_y), 15)
                pygame.draw.circle(self.screen, (0, 0, 0), (circle_x, circle_y), 15, 2)
    
    # ==============================
    # BUTTONS
    # ==============================
    
    def draw_button(self, rect, text, hover=False, text_color=(0, 0, 0), font=None):
        """Draw a button with optional hover effect"""
        # Only log hover on state change, not every frame
        logger.ui_debug(f"Drawing button '{text}' (hover={hover})")
        
        font = font or self.button_font
        color = self.BUTTON_HOVER_COLOR if hover else self.BUTTON_COLOR
        pygame.draw.rect(self.screen, color, rect)
        pygame.draw.rect(self.screen, (0, 0, 0), rect, 2)
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)
    
    def draw_card_count(self, rect, count):
        """Draw a small card count indicator on top of button"""
        count_text = self.small_font.render(str(count), True, (255, 0, 0))
        self.screen.blit(count_text, (rect.right - 20, rect.top + 5))
    
    # ==============================
    # UTILITIES
    # ==============================
    
    def set_background_color(self, color):
        old_color = self.BACKGROUND_COLOR
        self.BACKGROUND_COLOR = color
        logger.info(f"Background color changed: {old_color} → {color}")
    
    def get_screen_dimensions(self):
        return self.WIDTH, self.HEIGHT
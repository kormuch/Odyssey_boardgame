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
        self.PATH_COLOR = (255, 255, 255)
        self.BUTTON_COLOR = (255, 255, 255)
        self.BUTTON_HOVER_COLOR = (200, 200, 200)
        
        # Background image (from graphics manager)
        self.background_image = graphics_manager.get_image("background_01")
        self._bg_cache = None
        self._bg_cache_size = (0, 0)
        
        # Fonts
        self.button_font = pygame.font.Font(None, 24)
        self.textbox_font = pygame.font.Font(None, 18)
        self.small_font = pygame.font.Font(None, 18)
        self.large_font = pygame.font.Font(None, 36)

        # Track last states to avoid redundant logs
        self.last_left_marker = -1
        self.last_right_marker = -1
        self.last_paths = {}
        
        
        logger.info(f"UIRenderer initialized: {self.WIDTH}x{self.HEIGHT}")
    
    # ==============================
    # BACKGROUND
    # ==============================
    def _invalidate_bg_cache(self):
        self._bg_cache = None
        self._bg_cache_size = (0, 0)

    def _build_bg_cache(self):
        """Scale the background image once to screen size and cache it."""
        if not self.background_image:
            return None
        if self._bg_cache and self._bg_cache_size == (self.WIDTH, self.HEIGHT):
            return self._bg_cache

        try:
            scaled = pygame.transform.smoothscale(self.background_image, (self.WIDTH, self.HEIGHT))
        except Exception:
            scaled = pygame.transform.scale(self.background_image, (self.WIDTH, self.HEIGHT))
        # Keep convert/convert_alpha state (already done in GraphicsManager)
        self._bg_cache = scaled
        self._bg_cache_size = (self.WIDTH, self.HEIGHT)
        return self._bg_cache

    def draw_background(self, dim_overlay_alpha=0):
        """
        Draw the background. If no background image is loaded, fill with color.
        dim_overlay_alpha: optional 0..255 to darken background for readability.
        """
        bg = self._build_bg_cache()
        if bg:
            self.screen.blit(bg, (0, 0))
        else:
            self.screen.fill(self.BACKGROUND_COLOR)

        if dim_overlay_alpha:
            overlay = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, max(0, min(255, int(dim_overlay_alpha)))))
            self.screen.blit(overlay, (0, 0))

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
    # COLLISION TRACK (DANGER TRACK)
    # ==============================
    
    def draw_collision_track(self, track_data):
        """
        Draws the collision track with left and right markers.
        Left marker = Player damage position (starts at 0, moves right)
        Right marker = Suitors/antagonist position (starts at track_length, moves left)
        When they meet = Game Over
        """
        left_pos = track_data.get('left_position', 0)
        right_pos = track_data.get('right_position', 20)
        track_length = track_data.get('track_length', 20)
        collision = track_data.get('collision', False)
        
        # Only log when markers actually change
        if left_pos != self.last_left_marker or right_pos != self.last_right_marker:
            distance = right_pos - left_pos
            logger.info(f"[UI_RENDER] Collision track: Left@{left_pos}, Right@{right_pos}, Distance={distance}")
            
            if collision:
                logger.warning(f"[UI_RENDER] ⚠️ COLLISION DETECTED - GAME OVER!")
            elif distance <= 3:
                logger.warning(f"[UI_RENDER] ⚠️ Distance critical: {distance}")
            
            logger.game_debug(f"draw_collision_track called with track_data={track_data}")
            self.last_left_marker = left_pos
            self.last_right_marker = right_pos
        
        track_y = (self.HEIGHT // 3) + 50
        step_width = self.WIDTH // (track_length + 2)
        
        # Draw each position on the track
        for step in range(track_length + 1):
            x_pos = step * step_width + 10
            
            # Determine color based on position
            if step == left_pos and step == right_pos:
                # Collision!
                fill_color = (255, 0, 255)  # Magenta - collision
            elif step == left_pos:
                # Player marker (blue)
                fill_color = (50, 150, 255)  # Blue - player damage position
            elif step == right_pos:
                # Suitor marker (red)
                fill_color = (255, 50, 50)  # Red - antagonist position
            elif left_pos < step < right_pos:
                # Safe zone between markers
                fill_color = (200, 200, 200)  # Light gray - safe zone
            elif step < left_pos:
                # Behind player (damage already taken)
                fill_color = (100, 100, 150)  # Dark blue - past damage
            else:  # step > right_pos
                # Behind suitors (they've passed)
                fill_color = (150, 100, 100)  # Dark red - past threat
            
            # Draw the position
            rect = pygame.Rect(x_pos, track_y, step_width - 2, 20)
            pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)
            inner_rect = pygame.Rect(rect.x + 1, rect.y + 1, rect.width - 2, rect.height - 2)
            pygame.draw.rect(self.screen, fill_color, inner_rect)
            
            # Draw position number
            if step % 2 == 0:  # Only show every other number to avoid clutter
                num_text = self.small_font.render(str(step), True, (0, 0, 0))
                num_rect = num_text.get_rect(center=(x_pos + step_width // 2, track_y - 10))
                self.screen.blit(num_text, num_rect)
        
        # Draw labels
        label_y = track_y + 30
        
        # Left marker label
        left_label = self.small_font.render(f"Players: {left_pos}", True, (50, 150, 255))
        self.screen.blit(left_label, (10, label_y))
        
        # Right marker label
        right_label = self.small_font.render(f"Threat: {right_pos}", True, (255, 50, 50))
        right_label_rect = right_label.get_rect(right=self.WIDTH - 10, top=label_y)
        self.screen.blit(right_label, right_label_rect)
        
        # Distance label (center)
        distance = right_pos - left_pos
        distance_text = f"Distance: {distance}"
        if collision:
            distance_text = "COLLISION!"
        distance_label = self.button_font.render(distance_text, True, (0, 0, 0))
        distance_rect = distance_label.get_rect(center=(self.WIDTH // 2, label_y))
        self.screen.blit(distance_label, distance_rect)
    
    # ==============================
    # ACTION PATHS (QUEST PROGRESS)
    # ==============================
    
    def draw_paths(self, actionpaths):
        """Draws four paths with progress indicators (quest progress)"""
        # Only log when paths actually change
        if actionpaths != self.last_paths:
            changes = []
            for path_name in ["battle", "wits", "fellowship", "journey"]:
                old_val = self.last_paths.get(path_name, 0)
                new_val = actionpaths.get(path_name, 0)
                if old_val != new_val:
                    changes.append(f"{path_name}: {old_val}→{new_val}")
            
            if changes:
                logger.info(f"[UI_RENDER] Action paths updated: {', '.join(changes)}")
                logger.game_debug(f"draw_paths called with actionpaths={actionpaths}")
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
        logger.ui_debug(f"Drawing button '{text}' (hover={hover})")
        
        font = font or self.button_font
        color = self.BUTTON_HOVER_COLOR if hover else self.BUTTON_COLOR
        pygame.draw.rect(self.screen, color, rect)
        pygame.draw.rect(self.screen, (0, 0, 0), rect, 2)
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)
    
    def draw_image_button(self, rect, image_key, hover=False, text=None, text_color=(0, 0, 0), font=None, padding=6):
        """
        Draw a button filled with an image (image_key looked up via graphics manager).
        Falls back to draw_button() if image missing.
        - rect: pygame.Rect for button area
        - image_key: key used with graphics.get_image(...)
        - text: optional label drawn over the image (center-bottom)
        """
        logger.ui_debug(f"Drawing image-button '{text or image_key}' (hover={hover})")
        font = font or self.button_font
    
        img = self.graphics.get_image(image_key)
        if img is None:
            # fallback when image not available
            return self.draw_button(rect, text or image_key, hover=hover, text_color=text_color, font=font)
    
        # create temp surface for the button (supports alpha)
        btn_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    
        # compute target area (leave a small padding)
        target_w = max(1, rect.width - padding * 2)
        target_h = max(1, rect.height - padding * 2)
    
        img_w, img_h = img.get_size()
        # fit the image inside the target area (contain) to avoid cropping
        scale = min(target_w / img_w, target_h / img_h)
        new_w = max(1, int(img_w * scale))
        new_h = max(1, int(img_h * scale))
    
        try:
            scaled = pygame.transform.smoothscale(img, (new_w, new_h))
        except Exception:
            scaled = pygame.transform.scale(img, (new_w, new_h))
    
        blit_x = (rect.width - new_w) // 2
        blit_y = (rect.height - new_h) // 2
        btn_surf.blit(scaled, (blit_x, blit_y))
    
        # hover overlay to indicate hover state (subtle)
        if hover:
            hover_overlay = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            hover_overlay.fill((255, 255, 255, 60))  # lightening overlay; change alpha or color if you prefer darkening
            btn_surf.blit(hover_overlay, (0, 0))
    
        # border
        pygame.draw.rect(btn_surf, (0, 0, 0), pygame.Rect(0, 0, rect.width, rect.height), 2)
    
        # optional label over the image (bottom-centered with small translucent bg for readability)
        if text:
            text_surf = font.render(text, True, text_color)
            text_rect = text_surf.get_rect(midbottom=(rect.width // 2, rect.height - 6))
            bg_rect = text_rect.inflate(8, 4)
            bg_surf = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
            bg_surf.fill((255, 255, 255, 200))  # mostly opaque white background behind text; adjust alpha/color to taste
            btn_surf.blit(bg_surf, (bg_rect.x, bg_rect.y))
            btn_surf.blit(text_surf, (text_rect.x, text_rect.y))
    
        # blit the final button surface to the main screen
        self.screen.blit(btn_surf, rect.topleft)
    
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
        # If switching to color-only background, invalidate the cached image
        self.background_image = None
        self._invalidate_bg_cache()
        logger.info(f"Background color changed: {old_color} → {color}")
    
    def get_screen_dimensions(self):
        return self.WIDTH, self.HEIGHT
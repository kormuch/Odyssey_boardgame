import pygame
import sys


class ClassBoardGameGUI:
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        
        # Try to import and initialize the real GameEngine
        self.engine = None
        try:
            from GameEngine import ClassGameEngine
            self.engine = ClassGameEngine()
            print("Real GameEngine loaded successfully!")
        except ImportError:
            print("GameEngine not found, using mock engine for testing")
            # Use mock engine for testing
            self.engine = self._create_mock_engine()
        except Exception as e:
            print(f"Error loading GameEngine: {e}")
            print("Using mock engine for testing")
            self.engine = self._create_mock_engine()
        
        # Constants
        self.WIDTH, self.HEIGHT = 800, 700
        self.BACKGROUND_COLOR = (152, 251, 152)  # Shades of green
        self.SCREEN_COLOR = (152, 251, 152)  # Shades of green
        self.PROGRESS_BAR_COLOR = (255, 255, 255)
        self.PATH_COLOR = (255, 255, 255)
        self.BUTTON_COLOR = (255, 255, 255)
        self.BUTTON_ENGINE_posX, self.BUTTON_ENGINE_posY = 600, 400
        
        # initialize game
        self.init_game_button = pygame.Rect(510, 100, 100, 50)
        self.init_game_text_box = pygame.Rect(100, 100, 400, 50)
        self.init_game_active = False
        self.init_game_text = ''
        
        # menu
        self.button_quit_pos_x, self.button_quit_pos_y = 600, 100

        # Initialize the screen
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Board Game Interface")

        # Buttons
        self.buttons_menu = ["Quit"]
        self.buttons_actioncards = ["Battle", "Craftsmanship", "Fellowship", "Journey"]
        self.button_clicked = None
        self.button_height = 50
        self.button_margin_bottom = 10
        self.button_start_y = self.HEIGHT - self.button_height - self.button_margin_bottom
        self.button_width = self.WIDTH // 4

    def _create_mock_engine(self):
        """Create a mock engine for testing when real engine is not available"""
        class MockGameEngine:
            def __init__(self):
                self.game_statusID = 1
                self.players = 0
            
            def initialize_game(self):
                self.players = 2
                self.game_statusID = 1
                return self.players
            
            def deal_6_cards_perplayer(self):
                return f"Mock: Dealt {6 * self.players} cards"
            
            def run_level_loop(self):
                return "Mock: Level completed"
        
        return MockGameEngine()

    def draw_image_space(self):
        """Draws the black rectangle for the image space."""
        image_space_height = self.HEIGHT // 3
        image_space = pygame.Rect(self.WIDTH // 4, 0, self.WIDTH // 2, image_space_height)
        pygame.draw.rect(self.screen, (0, 0, 0), image_space)

    def draw_textbox(self, text):
        """Draws the textbox with the given text."""
        textbox_font = pygame.font.Font(None, 24)
        text_surface = textbox_font.render(text, True, (0, 0, 0))
        text_width, text_height = text_surface.get_size()
        textbox_x = self.WIDTH // 4
        textbox_y = (self.HEIGHT // 3) + 10
        textbox_rect = pygame.Rect(textbox_x, textbox_y, text_width + 10, text_height + 10)
        pygame.draw.rect(self.screen, (255, 255, 255), textbox_rect)
        self.screen.blit(text_surface, (textbox_x + 5, textbox_y + 5))

    def draw_progress_bar(self):
        """Draws the progress bar with 20 squares."""
        progress_bar_offset_x = 0
        progress_bar_y = (self.HEIGHT // 3) + 35
        border_thickness = 1
        for step in range(1, 21):
            border_color = (0, 0, 0)
            pygame.draw.rect(self.screen, border_color, (step * (self.WIDTH // 22) + progress_bar_offset_x,
                                                         progress_bar_y, self.WIDTH // 20, 20), border_thickness)
            pygame.draw.rect(self.screen, self.PROGRESS_BAR_COLOR, (step * (self.WIDTH // 22) + progress_bar_offset_x + border_thickness,
                                                                    progress_bar_y + border_thickness,
                                                                    self.WIDTH // 20 - 2 * border_thickness, 20 - 2 * border_thickness))

    def draw_paths(self):
        """Draws four paths with 10 circles each."""
        path_start_y = (self.HEIGHT // 3) + 95
        path_spacing = 48
        path_offset_x = 0
        for path in range(4):
            for step in range(1, 11):
                circle_radius = 15
                circle_x = step * (self.WIDTH // 25) + path_offset_x
                circle_y = path_start_y + path * path_spacing
                pygame.draw.circle(self.screen, self.PATH_COLOR, (circle_x, circle_y), circle_radius)

    def draw_buttons_actioncards(self):
        button_font = pygame.font.Font(None, 36)
        for i, button_text in enumerate(self.buttons_actioncards):
            button_rect = pygame.Rect(i * self.button_width, self.button_start_y, self.button_width, self.button_height)
            pygame.draw.rect(self.screen, self.BUTTON_COLOR, button_rect)
            text_surface = button_font.render(button_text, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=button_rect.center)
            self.screen.blit(text_surface, text_rect)
    
    def handle_button_click(self, pos):
        # Check action card buttons
        for i, button_text in enumerate(self.buttons_actioncards):
            button_rect = pygame.Rect(i * self.button_width, self.button_start_y, self.button_width, self.button_height)
            if button_rect.collidepoint(pos):
                self.button_clicked = button_text 
                print(f"Button clicked: {self.button_clicked}")
                # Add logic here to perform an action based on the clicked button
                return
        
        # Check for the QUIT button
        quit_button_rect = pygame.Rect(600, 100, self.button_width, self.button_height)
        if quit_button_rect.collidepoint(pos):
            self.button_clicked = "QUIT" 
            print(f"Button clicked: {self.button_clicked}")
            pygame.quit()
            sys.exit()
                
    def handle_button_START(self, pos):
        print("handle_button_START executed")
        button_engine_rect = pygame.Rect(self.BUTTON_ENGINE_posX, self.BUTTON_ENGINE_posY, self.button_width, self.button_height)
        if button_engine_rect.collidepoint(pos):
            print("START button clicked!")
            try:
                self.button_clicked = self.engine.deal_6_cards_perplayer()
                # Update game status to move to next phase
                self.engine.game_statusID = 1000
                print(f"Engine result: {self.button_clicked}")
                print(f"Game status changed to: {self.engine.game_statusID}")
            except Exception as e:
                print(f"Error calling engine method: {e}")

    def draw_button_quit(self):
        """exits the game"""
        button_font = pygame.font.Font(None, 36)
        button_rect = pygame.Rect(600, 100, self.button_width, self.button_height)
        pygame.draw.rect(self.screen, self.BUTTON_COLOR, button_rect)
        text_surface = button_font.render("QUIT", True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=button_rect.center)
        self.screen.blit(text_surface, text_rect)
        
    def draw_button_START(self):
        button_font = pygame.font.Font(None, 36)
        button_rect = pygame.Rect(self.BUTTON_ENGINE_posX, self.BUTTON_ENGINE_posY, self.button_width, self.button_height)
        pygame.draw.rect(self.screen, self.BUTTON_COLOR, button_rect)
        text_surface = button_font.render("START", True, (255, 0, 0))
        text_rect = text_surface.get_rect(center=button_rect.center)
        self.screen.blit(text_surface, text_rect)

    def runGUI_initialize_game(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button click
                        self.handle_button_click(event.pos)  # Pass the mouse position
                        self.handle_button_START(event.pos)
                        
                        # Check if we should exit this loop
                        if self.engine and hasattr(self.engine, 'game_statusID'):
                            if self.engine.game_statusID == 1000:
                                running = False
                                
            self.screen.fill(self.BACKGROUND_COLOR)
            self.draw_button_quit()
            self.draw_button_START()
            pygame.display.flip()
            clock.tick(60)

    def runGUI_game(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button click
                        self.handle_button_click(event.pos)  # Pass the mouse position
                        self.handle_button_START(event.pos)
                        
            self.screen.fill(self.BACKGROUND_COLOR)
            self.draw_image_space()
            self.draw_textbox("This is a sample text.")
            self.draw_progress_bar()
            self.draw_paths()
            self.draw_buttons_actioncards()
            self.draw_button_quit()
            self.draw_button_START()
            pygame.display.flip()
            clock.tick(60)
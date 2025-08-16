import pygame
import sys
import os

class ClassBoardGameGUI:
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        
        # Initialize the GameEngine FIRST
        self.engine = None
        try:
            from GameEngine import ClassGameEngine
            self.engine = ClassGameEngine()
            print("✓ Real GameEngine loaded successfully!")
        except ImportError:
            print("❌ GameEngine not found, using mock engine for testing")
            self.engine = self._create_mock_engine()
        except Exception as e:
            print(f"❌ Error loading GameEngine: {e}")
            print("Using mock engine for testing")
            self.engine = self._create_mock_engine()
        
        # Constants
        self.WIDTH, self.HEIGHT = 1500, 800
        self.BACKGROUND_COLOR = (152, 251, 152)  # Shades of green
        self.SCREEN_COLOR = (152, 251, 152)  # Shades of green
        self.PROGRESS_BAR_COLOR = (255, 255, 255)
        self.PATH_COLOR = (255, 255, 255)
        self.BUTTON_COLOR = (255, 255, 255)
        self.BUTTON_HOVER_COLOR = (200, 200, 200)
        self.BUTTON_ENGINE_posX, self.BUTTON_ENGINE_posY = 600, 400
        
        # Game state tracking
        self.current_message = "Welcome! Click START to begin."
        self.awaiting_input = False
        self.input_prompt = ""
        
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
        self.buttons_game_control = ["Next Player", "Skip Turn", "Show Cards", "New Level"]
        self.button_clicked = None
        self.button_height = 50
        self.button_margin_bottom = 10
        self.button_start_y = self.HEIGHT - self.button_height - self.button_margin_bottom
        self.button_width = self.WIDTH // 4
        self.small_button_width = 120
        
        # Mouse state for hover effects
        self.mouse_pos = (0, 0)
        
        # Load graphics
        self.load_graphics()

    def _create_mock_engine(self):
        """Create a mock engine for testing when real engine is not available"""
        class MockGameEngine:
            def __init__(self):
                self.game_statusID = 1
                self.numberOfPlayers = 0
                self.activePlayerID = 1
                self.actioncards_played = 0
                self.roundcounter = 1
                self.actionpaths = {"battle": 0, "craftsmanship": 0, "fellowship": 0, "journey": 0}
                self.playerData = {}
            
            def initialize_game(self, num_players=2):
                self.numberOfPlayers = num_players
                self.game_statusID = 1
                return num_players
            
            def deal_6_cards_perplayer(self):
                return f"Mock: Dealt {6 * self.numberOfPlayers} cards"
            
            def run_level_loop(self):
                return "Mock: Level completed"
            
            def process_user_input(self, user_input):
                return f"Mock: Processed {user_input}"
            
            def nextPlayer(self):
                self.activePlayerID = (self.activePlayerID % self.numberOfPlayers) + 1
                return self.activePlayerID
            
            def userInput_prompt(self):
                return f"Mock prompt for player {self.activePlayerID}"
        
        return MockGameEngine()

    def load_graphics(self):
        """Load game graphics with error handling"""
        self.images = {}
        
        # Define your graphics files
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
                    # Create a placeholder colored rectangle
                    placeholder = pygame.Surface((100, 100))
                    placeholder.fill((255, 0, 255))  # Magenta placeholder
                    self.images[name] = placeholder
                    print(f"  Created placeholder for {name}")
            except pygame.error as e:
                print(f"❌ Error loading {filepath}: {e}")
                # Create placeholder
                placeholder = pygame.Surface((100, 100))
                placeholder.fill((255, 0, 0))  # Red placeholder
                self.images[name] = placeholder

    def draw_image_space(self):
        """Draws the image space with loaded graphics"""
        image_space_height = self.HEIGHT // 3
        image_space_rect = pygame.Rect(self.WIDTH // 4, 0, self.WIDTH // 2, image_space_height)
        
        # Draw black background
        pygame.draw.rect(self.screen, (0, 0, 0), image_space_rect)
        
        # Draw the odysseus image if loaded
        if "odysseus" in self.images:
            image = self.images["odysseus"]
            # Scale image to fit in the space
            image_rect = image.get_rect()
            
            # Scale to fit while maintaining aspect ratio
            scale_x = (image_space_rect.width - 20) / image_rect.width
            scale_y = (image_space_rect.height - 20) / image_rect.height
            scale = min(scale_x, scale_y, 1.0)  # Don't upscale
            
            if scale < 1.0:
                new_width = int(image_rect.width * scale)
                new_height = int(image_rect.height * scale)
                scaled_image = pygame.transform.scale(image, (new_width, new_height))
            else:
                scaled_image = image
            
            # Center the image in the space
            scaled_rect = scaled_image.get_rect()
            scaled_rect.center = image_space_rect.center
            
            self.screen.blit(scaled_image, scaled_rect)

    def draw_textbox(self, text):
        """Draws the textbox with the given text."""
        textbox_font = pygame.font.Font(None, 20)
        
        # Handle multi-line text
        lines = text.split('\n')
        line_height = 22
        total_height = len(lines) * line_height + 10
        
        # Calculate max width needed
        max_width = 0
        for line in lines:
            text_surface = textbox_font.render(line, True, (0, 0, 0))
            max_width = max(max_width, text_surface.get_width())
        
        textbox_x = self.WIDTH // 4
        textbox_y = (self.HEIGHT // 3) + 10
        textbox_rect = pygame.Rect(textbox_x, textbox_y, max_width + 10, total_height)
        pygame.draw.rect(self.screen, (255, 255, 255), textbox_rect)
        pygame.draw.rect(self.screen, (0, 0, 0), textbox_rect, 2)  # Border
        
        # Draw each line
        for i, line in enumerate(lines):
            text_surface = textbox_font.render(line, True, (0, 0, 0))
            self.screen.blit(text_surface, (textbox_x + 5, textbox_y + 5 + i * line_height))

    def draw_progress_bar(self):
        """Draws the progress bar with 20 squares, highlighting current progress."""
        progress_bar_offset_x = 0
        progress_bar_y = (self.HEIGHT // 3) + 80
        border_thickness = 1
        
        # Calculate total progress from action paths
        total_progress = sum(self.engine.actionpaths.values()) if hasattr(self.engine, 'actionpaths') else 0
        
        for step in range(1, 21):
            border_color = (0, 0, 0)
            fill_color = (0, 255, 0) if step <= total_progress else self.PROGRESS_BAR_COLOR
            
            pygame.draw.rect(self.screen, border_color, (step * (self.WIDTH // 22) + progress_bar_offset_x,
                                                         progress_bar_y, self.WIDTH // 20, 20), border_thickness)
            pygame.draw.rect(self.screen, fill_color, (step * (self.WIDTH // 22) + progress_bar_offset_x + border_thickness,
                                                      progress_bar_y + border_thickness,
                                                      self.WIDTH // 20 - 2 * border_thickness, 20 - 2 * border_thickness))

    def draw_paths(self):
        """Draws four paths with 10 circles each, showing current progress."""
        path_start_y = (self.HEIGHT // 3) + 120
        path_spacing = 48
        path_offset_x = 0
        path_names = ["battle", "craftsmanship", "fellowship", "journey"]
        colors = [(255, 100, 100), (100, 255, 100), (100, 100, 255), (255, 255, 100)]
        
        for path in range(4):
            path_name = path_names[path]
            path_progress = self.engine.actionpaths.get(path_name, 0) if hasattr(self.engine, 'actionpaths') else 0
            
            # Draw path label
            font = pygame.font.Font(None, 24)
            label = font.render(path_name.capitalize(), True, (0, 0, 0))
            self.screen.blit(label, (10, path_start_y + path * path_spacing - 10))
            
            for step in range(1, 11):
                circle_radius = 15
                circle_x = step * (self.WIDTH // 25) + path_offset_x
                circle_y = path_start_y + path * path_spacing
                
                # Fill circles based on progress
                if step <= path_progress:
                    color = colors[path]
                else:
                    color = self.PATH_COLOR
                    
                pygame.draw.circle(self.screen, color, (circle_x, circle_y), circle_radius)
                pygame.draw.circle(self.screen, (0, 0, 0), (circle_x, circle_y), circle_radius, 2)

    def draw_button(self, rect, text, color=None, hover=False):
        """Helper method to draw a button with hover effects"""
        if color is None:
            color = self.BUTTON_HOVER_COLOR if hover else self.BUTTON_COLOR
            
        pygame.draw.rect(self.screen, color, rect)
        pygame.draw.rect(self.screen, (0, 0, 0), rect, 2)  # Border
        
        button_font = pygame.font.Font(None, 24)
        text_surface = button_font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)

    def draw_buttons_actioncards(self):
        """Draw action card buttons with hover effects and card counts"""
        button_font = pygame.font.Font(None, 24)
        small_font = pygame.font.Font(None, 18)
        
        for i, button_text in enumerate(self.buttons_actioncards):
            button_rect = pygame.Rect(i * self.button_width, self.button_start_y, self.button_width, self.button_height)
            hover = button_rect.collidepoint(self.mouse_pos)
            
            self.draw_button(button_rect, button_text, hover=hover)
            
            # Show card count if we have player data
            if (hasattr(self.engine, 'playerData') and self.engine.playerData and 
                hasattr(self.engine, 'activePlayerID') and self.engine.activePlayerID > 0):
                
                player_key = f"player {self.engine.activePlayerID}"
                if (player_key in self.engine.playerData and 
                    'actioncards' in self.engine.playerData[player_key]):
                    
                    card_name = button_text.lower()
                    card_count = self.engine.playerData[player_key]['actioncards'].get(card_name, 0)
                    
                    # Draw card count in corner
                    count_text = small_font.render(str(card_count), True, (255, 0, 0))
                    count_pos = (button_rect.right - 20, button_rect.top + 5)
                    self.screen.blit(count_text, count_pos)

    def draw_game_control_buttons(self):
        """Draw game control buttons"""
        start_x = 20
        start_y = 450
        button_spacing = 10
        
        for i, button_text in enumerate(self.buttons_game_control):
            button_rect = pygame.Rect(start_x, start_y + i * (self.button_height + button_spacing), 
                                    self.small_button_width, self.button_height)
            hover = button_rect.collidepoint(self.mouse_pos)
            self.draw_button(button_rect, button_text, hover=hover)

    def get_game_status_text(self):
        """Generate status text based on current game state"""
        if not self.engine:
            return "No game engine loaded"
        
        status_lines = []
        status_lines.append(f"Game Status: {getattr(self.engine, 'game_statusID', 'Unknown')}")
        status_lines.append(f"Players: {getattr(self.engine, 'numberOfPlayers', 0)}")
        status_lines.append(f"Active Player: {getattr(self.engine, 'activePlayerID', 0)}")
        status_lines.append(f"Round: {getattr(self.engine, 'roundcounter', 0)}")
        status_lines.append(f"Cards Played: {getattr(self.engine, 'actioncards_played', 0)}")
        status_lines.append("")
        status_lines.append(self.current_message)
        
        return "\n".join(status_lines)

    def handle_action_card_click(self, card_name):
        """Handle action card button clicks"""
        try:
            # Convert button text to engine format
            action_input = card_name.lower()
            
            # Process the action through the engine
            result = self.engine.process_user_input(action_input)
            
            if result:
                # Update action cards
                self.engine.update_actioncards()
                # Trigger card effects
                self.engine.trigger_cardEffect()
                
                self.current_message = f"Played {card_name} card!"
                print(f"Action result: {result}")
            else:
                self.current_message = f"Cannot play {card_name} - invalid action"
                
        except Exception as e:
            print(f"Error handling action card: {e}")
            self.current_message = f"Error playing {card_name}"

    def handle_game_control_click(self, control_name):
        """Handle game control button clicks"""
        try:
            if control_name == "Next Player":
                old_player = getattr(self.engine, 'activePlayerID', 0)
                new_player = self.engine.nextPlayer()
                self.current_message = f"Switched from Player {old_player} to Player {new_player}"
                
            elif control_name == "Skip Turn":
                result = self.engine.process_user_input("skip")
                self.current_message = "Turn skipped!"
                
            elif control_name == "Show Cards":
                if (hasattr(self.engine, 'playerData') and self.engine.playerData and 
                    hasattr(self.engine, 'activePlayerID') and self.engine.activePlayerID > 0):
                    
                    player_key = f"player {self.engine.activePlayerID}"
                    if player_key in self.engine.playerData:
                        cards = self.engine.playerData[player_key].get('actioncards', {})
                        card_text = ", ".join([f"{k}: {v}" for k, v in cards.items() if v > 0])
                        self.current_message = f"Player {self.engine.activePlayerID} cards: {card_text}"
                    else:
                        self.current_message = "No card data available"
                else:
                    self.current_message = "No active player data"
                    
            elif control_name == "New Level":
                result = self.engine.run_level_loop()
                self.current_message = f"Level loop result: {result}"
                
        except Exception as e:
            print(f"Error handling game control: {e}")
            self.current_message = f"Error with {control_name}: {str(e)}"

    def handle_button_click(self, pos):
        # Check action card buttons
        for i, button_text in enumerate(self.buttons_actioncards):
            button_rect = pygame.Rect(i * self.button_width, self.button_start_y, self.button_width, self.button_height)
            if button_rect.collidepoint(pos):
                self.handle_action_card_click(button_text)
                return
        
        # Check game control buttons
        start_x = 20
        start_y = 450
        button_spacing = 10
        
        for i, button_text in enumerate(self.buttons_game_control):
            button_rect = pygame.Rect(start_x, start_y + i * (self.button_height + button_spacing), 
                                    self.small_button_width, self.button_height)
            if button_rect.collidepoint(pos):
                self.handle_game_control_click(button_text)
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
                # Initialize game with default 2 players
                players = self.engine.initialize_game(2)
                self.current_message = f"Game initialized with {players} players"
                
                # Deal cards
                result = self.engine.deal_6_cards_perplayer()
                self.current_message += f"\n{result}"
                
                # Update game status to move to next phase
                self.engine.game_statusID = 1000
                print(f"Engine result: {result}")
                print(f"Game status changed to: {self.engine.game_statusID}")
                
            except Exception as e:
                print(f"Error calling engine method: {e}")
                self.current_message = f"Error starting game: {str(e)}"

    def draw_button_quit(self):
        """Draw quit button with hover effect"""
        button_rect = pygame.Rect(600, 100, self.button_width, self.button_height)
        hover = button_rect.collidepoint(self.mouse_pos)
        self.draw_button(button_rect, "QUIT", hover=hover)
        
    def draw_button_START(self):
        """Draw start button with hover effect"""
        button_rect = pygame.Rect(self.BUTTON_ENGINE_posX, self.BUTTON_ENGINE_posY, self.button_width, self.button_height)
        hover = button_rect.collidepoint(self.mouse_pos)
        color = self.BUTTON_HOVER_COLOR if hover else self.BUTTON_COLOR
        
        pygame.draw.rect(self.screen, color, button_rect)
        pygame.draw.rect(self.screen, (0, 0, 0), button_rect, 2)
        
        button_font = pygame.font.Font(None, 36)
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
                elif event.type == pygame.MOUSEMOTION:
                    self.mouse_pos = event.pos
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button click
                        self.handle_button_click(event.pos)
                        self.handle_button_START(event.pos)
                        
                        # Check if we should exit this loop
                        if self.engine and hasattr(self.engine, 'game_statusID'):
                            if self.engine.game_statusID == 1000:
                                running = False
                                
            self.screen.fill(self.BACKGROUND_COLOR)
            self.draw_textbox("Click START to initialize the game\nwith 2 players and deal cards.")
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
                elif event.type == pygame.MOUSEMOTION:
                    self.mouse_pos = event.pos
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button click
                        self.handle_button_click(event.pos)
                        self.handle_button_START(event.pos)
                        
            self.screen.fill(self.BACKGROUND_COLOR)
            self.draw_image_space()
            self.draw_textbox(self.get_game_status_text())
            self.draw_progress_bar()
            self.draw_paths()
            self.draw_buttons_actioncards()
            self.draw_game_control_buttons()
            self.draw_button_quit()
            
            # Only show START button if game isn't fully initialized
            if getattr(self.engine, 'game_statusID', 0) < 1000:
                self.draw_button_START()
                
            pygame.display.flip()
            clock.tick(60)
import pygame
import sys
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
        
        scaled_rect = scaled_image.get_rect()
        scaled_rect.center = container_rect.center
        self.screen.blit(scaled_image, scaled_rect)
    
    def draw_textbox(self, text, position=None):
        """Draws a textbox with the given text"""
        lines = text.split('\n')
        line_height = 20
        total_height = len(lines) * line_height + 10
        
        max_width = max(self.textbox_font.size(line)[0] for line in lines)
        textbox_width = max_width + 10
        
        if position is None:
            # Default position (bottom right)
            textbox_x = self.WIDTH - textbox_width - 20
            textbox_y = self.HEIGHT - total_height - 80
        else:
            textbox_x, textbox_y = position
        
        textbox_rect = pygame.Rect(textbox_x, textbox_y, textbox_width, total_height)
        pygame.draw.rect(self.screen, (255, 255, 255), textbox_rect)
        pygame.draw.rect(self.screen, (0, 0, 0), textbox_rect, 2)
        
        for i, line in enumerate(lines):
            text_surface = self.textbox_font.render(line, True, (0, 0, 0))
            self.screen.blit(text_surface, (textbox_x + 5, textbox_y + 5 + i * line_height))
    
    def draw_progress_bar(self, total_progress):
        """Draws the progress bar with highlighting"""
        progress_bar_y = (self.HEIGHT // 3) + 50
        
        for step in range(1, 21):
            fill_color = (0, 255, 0) if step <= total_progress else self.PROGRESS_BAR_COLOR
            
            rect = pygame.Rect(step * (self.WIDTH // 22), progress_bar_y, self.WIDTH // 20, 20)
            pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)
            inner_rect = pygame.Rect(rect.x + 1, rect.y + 1, rect.width - 2, rect.height - 2)
            pygame.draw.rect(self.screen, fill_color, inner_rect)
    
    def draw_paths(self, actionpaths):
        """Draws four paths with progress indicators"""
        path_start_y = (self.HEIGHT // 3) + 140
        path_spacing = 60
        path_offset_x = 50
        path_names = ["battle", "Journey", "fellowship", "Journey"]
        colors = [(255, 100, 100), (100, 255, 100), (100, 100, 255), (255, 255, 100)]
        
        for path in range(4):
            path_name = path_names[path]
            path_progress = actionpaths.get(path_name, 0)
            
            # Draw label
            label = self.button_font.render(path_name.capitalize(), True, (0, 0, 0))
            label_y = path_start_y + path * path_spacing - 35
            self.screen.blit(label, (path_offset_x, label_y))
            
            # Draw progress circles
            for step in range(1, 11):
                circle_x = step * (self.WIDTH // 25) + path_offset_x
                circle_y = path_start_y + path * path_spacing
                
                color = colors[path] if step <= path_progress else self.PATH_COLOR
                pygame.draw.circle(self.screen, color, (circle_x, circle_y), 15)
                pygame.draw.circle(self.screen, (0, 0, 0), (circle_x, circle_y), 15, 2)
    
    def draw_button(self, rect, text, hover=False, text_color=(0, 0, 0), font=None):
        """Draw a button with hover effects"""
        if font is None:
            font = self.button_font
            
        color = self.BUTTON_HOVER_COLOR if hover else self.BUTTON_COLOR
        pygame.draw.rect(self.screen, color, rect)
        pygame.draw.rect(self.screen, (0, 0, 0), rect, 2)
        
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)
    
    def draw_card_count(self, rect, count):
        """Draw card count indicator on button"""
        count_text = self.small_font.render(str(count), True, (255, 0, 0))
        count_pos = (rect.right - 20, rect.top + 5)
        self.screen.blit(count_text, count_pos)


class ButtonManager:
    """Manages button layouts and interactions"""
    
    def __init__(self, screen_width, screen_height):
        self.WIDTH = screen_width
        self.HEIGHT = screen_height
        self.button_height = 50
        self.button_margin_bottom = 10
        self.button_start_y = self.HEIGHT - self.button_height - self.button_margin_bottom
        self.button_width = self.WIDTH // 4
        self.small_button_width = 120
        
        # Button definitions
        self.action_buttons = ["Battle", "Journey", "Fellowship", "Journey"]
        self.control_buttons = ["Next Player", "Skip Turn", "Show Cards", "New Level"]
        
        # Calculate positions
        self.quit_button_rect = pygame.Rect(
            self.WIDTH - 80 - 10,  # 80px width + 10px margin from right edge
            10,  # 10px margin from top edge
            80,  # Smaller width
            30   # Smaller height
        )
        
        self.start_button_rect = pygame.Rect(
            self.WIDTH // 2 - self.button_width // 2,  # Center horizontally
            400,  # Keep same vertical position
            self.button_width, 
            self.button_height
        )
    
    def get_action_button_rect(self, index):
        """Get rectangle for action button at index"""
        return pygame.Rect(
            index * self.button_width,
            self.button_start_y,
            self.button_width,
            self.button_height
        )
    
    def get_control_button_rect(self, index):
        """Get rectangle for control button at index"""
        return pygame.Rect(
            20,
            20 + index * (self.button_height + 5),
            self.small_button_width,
            self.button_height
        )
    
    def get_clicked_button(self, pos):
        """Determine which button was clicked"""
        # Check action buttons
        for i, button_name in enumerate(self.action_buttons):
            if self.get_action_button_rect(i).collidepoint(pos):
                return ("action", button_name)
        
        # Check control buttons
        for i, button_name in enumerate(self.control_buttons):
            if self.get_control_button_rect(i).collidepoint(pos):
                return ("control", button_name)
        
        # Check special buttons
        if self.quit_button_rect.collidepoint(pos):
            return ("special", "quit")
        
        if self.start_button_rect.collidepoint(pos):
            return ("special", "start")
        
        return None


class GameStateManager:
    """Manages game state and engine interactions"""
    
    def __init__(self, engine=None):
        self.engine = engine  # Use provided engine or create one
        self.current_message = "Welcome! Click START to begin."
        self.awaiting_input = False
        self.input_prompt = ""
        
        if self.engine is None:
            self._initialize_engine()
    
    def _initialize_engine(self):
        """Initialize the game engine"""
        try:
            # Import your actual GameEngine
            from GameEngine import ClassGameEngine
            self.engine = ClassGameEngine()
            print("✓ Real GameEngine loaded successfully!")
            print(f"Engine initialized with game_statusID: {self.engine.game_statusID}")
        except ImportError as e:
            print(f"❌ GameEngine import failed: {e}")
            print("Make sure GameEngine.py is in the same directory as your GUI")
            self.engine = self._create_mock_engine()
        except Exception as e:
            print(f"❌ Error loading GameEngine: {e}")
            print("Using mock engine for testing")
            self.engine = self._create_mock_engine()
    
    def _create_mock_engine(self):
        """Create a mock engine for testing"""
        class MockGameEngine:
            def __init__(self):
                self.game_statusID = 1
                self.numberOfPlayers = 0
                self.activePlayerID = 1
                self.actioncards_played = 0
                self.roundcounter = 1
                self.actionpaths = {"battle": 0, "Journey": 0, "fellowship": 0, "Journey": 0}
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
            
            def update_actioncards(self):
                pass
                
            def trigger_cardEffect(self):
                pass
            
            def userInput_prompt(self):
                return f"Mock prompt for player {self.activePlayerID}"
        
        return MockGameEngine()
    
    def get_status_text(self):
        """Generate status text based on current game state"""
        if not self.engine:
            return "No game engine loaded"
        
        status_lines = [
            f"Game Status: {getattr(self.engine, 'game_statusID', 'Unknown')}",
            f"Players: {getattr(self.engine, 'numberOfPlayers', 0)}",
            f"Active Player: {getattr(self.engine, 'activePlayerID', 0)}",
            f"Round: {getattr(self.engine, 'roundcounter', 0)}",
            f"Total Cards Played: {getattr(self.engine, 'actioncards_played', 0)}",
            "",
            f"Action Paths Progress:",
            f"Battle: {self.engine.actionpaths.get('battle', 0)}",
            f"Journey: {self.engine.actionpaths.get('Journey', 0)}",
            f"Fellowship: {self.engine.actionpaths.get('fellowship', 0)}",
            f"Journey: {self.engine.actionpaths.get('Journey', 0)}",
            "",
            self.current_message
        ]
        
        return "\n".join(status_lines)
    
    def get_total_progress(self):
        """Get total progress from action paths"""
        return sum(self.engine.actionpaths.values()) if hasattr(self.engine, 'actionpaths') else 0
    
    def get_actionpaths(self):
        """Get action paths dictionary"""
        return getattr(self.engine, 'actionpaths', {})
    
    def get_player_card_count(self, card_name):
        """Get card count for active player"""
        if (hasattr(self.engine, 'playerData') and self.engine.playerData and 
            hasattr(self.engine, 'activePlayerID') and self.engine.activePlayerID > 0):
            
            player_key = f"player {self.engine.activePlayerID}"
            if (player_key in self.engine.playerData and 
                'actioncards' in self.engine.playerData[player_key]):
                return self.engine.playerData[player_key]['actioncards'].get(card_name.lower(), 0)
        
        return 0


class ClassBoardGameGUI:
    """Main GUI class that coordinates all components"""
    
    def __init__(self, engine=None):
        pygame.init()
        
        # Screen setup
        self.WIDTH, self.HEIGHT = 1500, 750
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Board Game Interface")
        
        # Initialize components
        self.graphics = GraphicsManager()
        self.renderer = UIRenderer(self.screen, self.graphics)
        self.buttons = ButtonManager(self.WIDTH, self.HEIGHT)
        self.game_state = GameStateManager(engine)  # Pass engine if provided
        
        # For backwards compatibility, expose the engine
        self.engine = self.game_state.engine
        
        # Input state
        self.mouse_pos = (0, 0)
    
    def handle_button_click(self, pos):
        """Handle button click events"""
        button_info = self.buttons.get_clicked_button(pos)
        if not button_info:
            return
        
        button_type, button_name = button_info
        
        if button_type == "action":
            self._handle_action_card(button_name)
        elif button_type == "control":
            self._handle_game_control(button_name)
        elif button_type == "special":
            self._handle_special_button(button_name)
    
    def _handle_action_card(self, card_name):
        """Handle action card button clicks"""
        try:
            action_input = card_name.lower()
            result = self.game_state.engine.process_user_input(action_input)
            
            if result:
                # Update cards and trigger effects
                card_result = self.game_state.engine.update_actioncards()
                effect_result = self.game_state.engine.trigger_cardEffect()
                
                # Check if player has enough cards or used joker
                active_player_key = self.game_state.engine.get_activePlayer_playerKey()
                if (hasattr(self.game_state.engine, 'playerData') and 
                    active_player_key in self.game_state.engine.playerData):
                    cards_played = self.game_state.engine.playerData[active_player_key].get('actioncards_played', 0)
                    self.game_state.current_message = f"Played {card_name} card! Cards played this turn: {cards_played}"
                else:
                    self.game_state.current_message = f"Played {card_name} card!"
                
                # Check if turn should end (2 cards played)
                if self.game_state.engine.actioncards_played >= 2:
                    old_player = self.game_state.engine.activePlayerID
                    self.game_state.engine.nextPlayer()
                    self.game_state.engine.actioncards_played = 0
                    new_player = self.game_state.engine.activePlayerID
                    self.game_state.current_message += f"\nTurn complete! Now Player {new_player}'s turn."
                    
            else:
                self.game_state.current_message = f"Cannot play {card_name} - invalid action or insufficient cards"
                
        except Exception as e:
            print(f"Error handling action card: {e}")
            self.game_state.current_message = f"Error playing {card_name}: {str(e)}"
    
    def _handle_game_control(self, control_name):
        """Handle game control button clicks"""
        try:
            if control_name == "Next Player":
                old_player = getattr(self.game_state.engine, 'activePlayerID', 0)
                new_player = self.game_state.engine.nextPlayer()
                self.game_state.current_message = f"Switched from Player {old_player} to Player {new_player}"
                
            elif control_name == "Skip Turn":
                self.game_state.engine.process_user_input("skip")
                self.game_state.current_message = "Turn skipped!"
                
            elif control_name == "Show Cards":
                self._show_player_cards()
                
            elif control_name == "New Level":
                result = self.game_state.engine.run_level_loop()
                self.game_state.current_message = f"Level loop result: {result}"
                
        except Exception as e:
            print(f"Error handling game control: {e}")
            self.game_state.current_message = f"Error with {control_name}: {str(e)}"
    
    def _show_player_cards(self):
        """Display current player's cards"""
        engine = self.game_state.engine
        if (hasattr(engine, 'playerData') and engine.playerData and 
            hasattr(engine, 'activePlayerID') and engine.activePlayerID > 0):
            
            player_key = f"player {engine.activePlayerID}"
            if player_key in engine.playerData:
                cards = engine.playerData[player_key].get('actioncards', {})
                card_text = ", ".join([f"{k}: {v}" for k, v in cards.items() if v > 0])
                if card_text:
                    self.game_state.current_message = f"Player {engine.activePlayerID} cards: {card_text}"
                else:
                    self.game_state.current_message = f"Player {engine.activePlayerID} has no cards!"
                    
                # Also show endurance and cards played
                endurance = engine.playerData[player_key].get('endurance', 15)
                cards_played = engine.playerData[player_key].get('actioncards_played', 0)
                self.game_state.current_message += f"\nEndurance: {endurance}, Cards played: {cards_played}"
            else:
                self.game_state.current_message = "No card data available for current player"
        else:
            self.game_state.current_message = "No active player data"
    
    def _handle_special_button(self, button_name):
        """Handle special buttons (quit, start)"""
        if button_name == "quit":
            pygame.quit()
            sys.exit()
        elif button_name == "start":
            self._start_game()
    
    def _start_game(self):
        """Initialize and start the game"""
        try:
            players = self.game_state.engine.initialize_game(2)
            self.game_state.current_message = f"Game initialized with {players} players"
            
            result = self.game_state.engine.deal_6_cards_perplayer()
            self.game_state.current_message += f"\n{result}"
            
            self.game_state.engine.game_statusID = 1000
            print(f"Game status changed to: {self.game_state.engine.game_statusID}")
            
        except Exception as e:
            print(f"Error starting game: {e}")
            self.game_state.current_message = f"Error starting game: {str(e)}"
    
    def draw_action_buttons(self):
        """Draw action card buttons with card counts"""
        for i, button_text in enumerate(self.buttons.action_buttons):
            button_rect = self.buttons.get_action_button_rect(i)
            hover = button_rect.collidepoint(self.mouse_pos)
            
            self.renderer.draw_button(button_rect, button_text, hover=hover)
            
            # Show card count
            card_count = self.game_state.get_player_card_count(button_text)
            if card_count > 0:
                self.renderer.draw_card_count(button_rect, card_count)
    
    def draw_control_buttons(self):
        """Draw game control buttons"""
        for i, button_text in enumerate(self.buttons.control_buttons):
            button_rect = self.buttons.get_control_button_rect(i)
            hover = button_rect.collidepoint(self.mouse_pos)
            self.renderer.draw_button(button_rect, button_text, hover=hover)
    
    def runGUI_initialize_game(self):
        """Run the game initialization screen"""
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
                    if event.button == 1:
                        self.handle_button_click(event.pos)
                        
                        # Check if we should exit this loop
                        if (self.game_state.engine and 
                            hasattr(self.game_state.engine, 'game_statusID') and
                            self.game_state.engine.game_statusID == 1000):
                            running = False
            
            self.screen.fill(self.renderer.BACKGROUND_COLOR)
            self.renderer.draw_textbox("Click START to initialize the game\nwith 2 players and deal cards.")
            
            # Draw quit button (now in top right corner and smaller)
            hover = self.buttons.quit_button_rect.collidepoint(self.mouse_pos)
            self.renderer.draw_button(self.buttons.quit_button_rect, "QUIT", hover=hover)
            
            # Draw start button
            hover = self.buttons.start_button_rect.collidepoint(self.mouse_pos)
            self.renderer.draw_button(self.buttons.start_button_rect, "START", hover=hover, 
                                    text_color=(255, 0, 0), font=self.renderer.large_font)
            
            pygame.display.flip()
            clock.tick(60)
    
    def runGUI_game(self):
        """Run the main game screen"""
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
                    if event.button == 1:
                        self.handle_button_click(event.pos)
            
            self.screen.fill(self.renderer.BACKGROUND_COLOR)
            
            # Draw all UI elements
            self.renderer.draw_image_space()
            self.renderer.draw_textbox(self.game_state.get_status_text())
            self.renderer.draw_progress_bar(self.game_state.get_total_progress())
            self.renderer.draw_paths(self.game_state.get_actionpaths())
            
            self.draw_action_buttons()
            self.draw_control_buttons()
            
            # Draw quit button (now in top right corner and smaller)
            hover = self.buttons.quit_button_rect.collidepoint(self.mouse_pos)
            self.renderer.draw_button(self.buttons.quit_button_rect, "QUIT", hover=hover)
            
            # Show start button if game isn't fully initialized
            if getattr(self.game_state.engine, 'game_statusID', 0) < 1000:
                hover = self.buttons.start_button_rect.collidepoint(self.mouse_pos)
                self.renderer.draw_button(self.buttons.start_button_rect, "START", hover=hover,
                                        text_color=(255, 0, 0), font=self.renderer.large_font)
            
            pygame.display.flip()
            clock.tick(60)
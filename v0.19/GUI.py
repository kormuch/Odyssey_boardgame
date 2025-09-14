import pygame
import sys

# Import our modular components
from graphics_manager import GraphicsManager
from ui_renderer import UIRenderer
from button_manager import ButtonManager
from game_state_manager import GameStateManager


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
    
    def _handle_action_card(self, card_name):
        """Handle action card button clicks"""
        try:
            action_input = card_name.lower()
            result = self.game_state.engine.process_user_input(action_input)
            
            if result:
                # Store current state before operations
                cards_before = self.game_state.engine.actioncards_played
                player_before = self.game_state.engine.activePlayerID
                
                # Update cards and trigger effects
                card_result = self.game_state.engine.update_actioncards()
                effect_result = self.game_state.engine.trigger_cardEffect()
                
                self.game_state.current_message = f"Played {card_name} card! Cards played this turn: {self.game_state.engine.actioncards_played}"
                
                # Let the engine handle turn switching logic
                game_status = self.game_state.engine.run_level_loop()
                
                # Check if turn switched (counter reset means new player)
                if (self.game_state.engine.actioncards_played == 0 and 
                    self.game_state.engine.activePlayerID != player_before):
                    self.game_state.current_message += f"\nTurn complete! Now Player {self.game_state.engine.activePlayerID}'s turn."
                    
            else:
                self.game_state.current_message = f"Cannot play {card_name} - invalid action or insufficient cards"
                
        except Exception as e:
            print(f"Error handling action card: {e}")
            self.game_state.current_message = f"Error playing {card_name}: {str(e)}"
    
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
            # Show start button only if game hasn't been started yet
            if getattr(self.game_state.engine, 'game_statusID', 0) == 0:
                hover = self.buttons.start_button_rect.collidepoint(self.mouse_pos)
                self.renderer.draw_button(self.buttons.start_button_rect, "START", hover=hover,
                                        text_color=(255, 0, 0), font=self.renderer.large_font)
            
            pygame.display.flip()
            clock.tick(60)
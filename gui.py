# gui.py
import pygame
import sys
from gamelog import logger

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
        self.game_state = GameStateManager(engine)
        
        # For backwards compatibility, expose the engine
        self.engine = self.game_state.engine
        
        # Input state
        self.mouse_pos = (0, 0)
        logger.info("=== GUI Ready ===")
    
    def handle_button_click(self, pos):
        """Handle button click events"""
        button_info = self.buttons.get_clicked_button(pos)
        
        if not button_info:
            logger.ui_debug(f"Click at {pos} - no button")
            return
        
        button_type, button_name = button_info
        logger.info(f"Button clicked: {button_type}.{button_name} at {pos}")
        
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
            player_id = self.game_state.engine.activePlayerID
            
            logger.player_action(
                player_id,
                f"Attempting to play card '{card_name}'",
                cards_played_so_far=self.game_state.engine.actioncards_played
            )
            
            result = self.game_state.engine.process_user_input(action_input)
            
            if result:
                # Store current state before operations
                cards_before = self.game_state.engine.actioncards_played
                player_before = self.game_state.engine.activePlayerID
                
                # Update cards and trigger effects
                self.game_state.engine.update_actioncards()
                self.game_state.engine.trigger_cardEffect()
                
                self.game_state.current_message = f"Played {card_name} card! Cards played this turn: {self.game_state.engine.actioncards_played}"
                
                # Let the engine handle turn switching logic
                game_status = self.game_state.engine.run_level_loop()
                
                # Check if turn switched
                if (self.game_state.engine.actioncards_played == 0 and 
                    self.game_state.engine.activePlayerID != player_before):
                    logger.player_action(
                        player_before,
                        "Turn completed",
                        next_player=self.game_state.engine.activePlayerID
                    )
                    self.game_state.current_message += f"\nTurn complete! Now Player {self.game_state.engine.activePlayerID}'s turn."
                    
            else:
                self.game_state.current_message = f"Cannot play {card_name} - invalid action or insufficient cards"
                logger.warning(f"Player {player_id} failed to play '{card_name}'")
                
        except Exception as e:
            logger.error(f"Error handling action card {card_name}: {e}")
            logger.exception("Full traceback:")
            self.game_state.current_message = f"Error playing {card_name}: {str(e)}"
    
    def _handle_game_control(self, button_name):
        """Handle game control buttons"""
        logger.info(f"Control action: {button_name}")
        
        if button_name == "Next Player":
            old_player = self.game_state.engine.activePlayerID
            self.game_state.engine.nextPlayer()
            new_player = self.game_state.engine.activePlayerID
            logger.player_action(old_player, "Switched to next player", next_player=new_player)
            self.game_state.current_message = f"Switched to Player {new_player}"
            
        elif button_name == "Skip Turn":
            player_id = self.game_state.engine.activePlayerID
            self.game_state.engine.process_user_input("skip")
            logger.player_action(player_id, "Skipped turn")
            self.game_state.current_message = f"Player {player_id} skipped turn"
            
        elif button_name == "Show Cards":
            self._show_player_cards()
            
        elif button_name == "New Level":
            logger.game_event("new_level_requested")
            self.game_state.current_message = "New level feature coming soon!"
    
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
                
                logger.info(f"Displayed cards for Player {engine.activePlayerID}: {card_text}")
            else:
                self.game_state.current_message = "No card data available for current player"
                logger.warning(f"No data for player key '{player_key}'")
        else:
            self.game_state.current_message = "No active player data"
            logger.warning("No active player data available")
    
    def _handle_special_button(self, button_name):
        """Handle special buttons (quit, start)"""
        if button_name == "quit":
            logger.info("=== User initiated quit ===")
            pygame.quit()
            sys.exit()
        elif button_name == "start":
            self._start_game()
    
    def _start_game(self):
        """Initialize and start the game"""
        try:
            logger.game_event("game_start_requested")
            players = self.game_state.engine.initialize_game(2)
            self.game_state.current_message = f"Game initialized with {players} players"
            
            old_status = self.game_state.engine.game_statusID
            self.game_state.engine.game_statusID = 1000
            logger.state_change("game_status", old_status, 1000)
            
        except Exception as e:
            logger.error(f"Failed to start game: {e}")
            logger.exception("Full traceback:")
            self.game_state.current_message = f"Error starting game: {str(e)}"
    
    def draw_action_buttons(self):
        """Draw action card buttons with card counts (use images when available)"""
        # map your button labels to graphics_manager keys
        image_map = {
            "battle": "actioncard battle 01",
            "wits": "actioncard wits 01",
            "fellowship": "actioncard fellowship 01",
            "journey": "actioncard journey 01",
        }

        for i, button_text in enumerate(self.buttons.action_buttons):
            button_rect = self.buttons.get_action_button_rect(i)
            hover = button_rect.collidepoint(self.mouse_pos)

            key = image_map.get(button_text.strip().lower())
            # if there is a mapped image and the graphics manager has it, draw image button
            if key and self.graphics.get_image(key):
                self.renderer.draw_image_button(button_rect, key, hover=hover, text=button_text)
            else:
                # fallback to plain styled button
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
        logger.info("=== Initialization Screen ===")
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    logger.info("Quit event during initialization")
                    running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEMOTION:
                    self.mouse_pos = event.pos
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.handle_button_click(event.pos)
                        
                        if (self.game_state.engine and 
                            hasattr(self.game_state.engine, 'game_statusID') and
                            self.game_state.engine.game_statusID == 1000):
                            logger.info("Game initialized, transitioning to main game")
                            running = False
            
            self.renderer.draw_background()
            self.renderer.draw_textbox("Click START to initialize the game\nwith 2 players and deal cards.")
            
            hover = self.buttons.quit_button_rect.collidepoint(self.mouse_pos)
            self.renderer.draw_button(self.buttons.quit_button_rect, "QUIT", hover=hover)
            
            hover = self.buttons.start_button_rect.collidepoint(self.mouse_pos)
            self.renderer.draw_button(self.buttons.start_button_rect, "START", hover=hover, 
                                      text_color=(255, 0, 0), font=self.renderer.large_font)
            
            pygame.display.flip()
            clock.tick(60)
    
    def runGUI_game(self):
        """Run the main game screen"""
        logger.info("=== Main Game Screen ===")
        clock = pygame.time.Clock()
        running = True
        frame_count = 0
        
        while running:
            frame_count += 1
            
            # Log every 300 frames (5 seconds at 60fps) to show game is running
            if frame_count % 300 == 0:
                logger.game_debug(f"Game running... (frame {frame_count})")
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    logger.info("Quit event during game")
                    running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEMOTION:
                    self.mouse_pos = event.pos
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.handle_button_click(event.pos)
            
            self.renderer.draw_background()
            
            self.renderer.draw_image_space()
            self.renderer.draw_textbox(self.game_state.get_status_text())
            
            # FIXED: Draw collision track instead of progress bar
            collision_data = self.game_state.get_collision_track_data()
            self.renderer.draw_collision_track(collision_data)
            
            # Draw action paths (quest progress) - unchanged
            self.renderer.draw_paths(self.game_state.get_actionpaths())
            
            self.draw_action_buttons()
            self.draw_control_buttons()
            
            hover = self.buttons.quit_button_rect.collidepoint(self.mouse_pos)
            self.renderer.draw_button(self.buttons.quit_button_rect, "QUIT", hover=hover)
            
            if getattr(self.game_state.engine, 'game_statusID', 0) == 0:
                hover = self.buttons.start_button_rect.collidepoint(self.mouse_pos)
                self.renderer.draw_button(self.buttons.start_button_rect, "START", hover=hover,
                                          text_color=(255, 0, 0), font=self.renderer.large_font)
            
            pygame.display.flip()
            clock.tick(60)
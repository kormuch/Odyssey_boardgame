# Main class
import pygame
from GameEngineV2 import GameEngine



# Create an instance of the game engine
game = GameEngine()

# Ask for the number of players
players = game.initialize_game()


while game.game_statusID != 0:
    # Initialize pygame
    pygame.init()
    game.deal_6_cards_perplayer()
    game.game_statusID = 1000
    
    while game.game_statusID == 1000:
        game.run_level_loop()

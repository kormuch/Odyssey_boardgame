# Main class
import pygame
import json
from PlayerData import Player
from GameEngine import GameEngine



# Create an instance of the game engine
game = GameEngine()

# Ask for the number of players
players = game.initialize_game()

while game.gamestatus != 0:
    # Initialize pygame
    pygame.init()

    game.gamestatus = 1000
    game.deal_6_cards_perplayer()
    
    while game.gamestatus == 1000:
        game.run_level_loop()

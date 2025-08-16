# Main class
import pygame
from GameEngine import GameEngine
from GUI import BoardGameGUI

# gui_loop.py
import sys



# Create an instance of the game engine
game = GameEngine()
gui = BoardGameGUI()


while game.game_statusID != 0:
    gui.runGUI()


# Ask for the number of players
players = game.initialize_game()


while game.game_statusID != 0:
    if game.game_statusID == 1:
        pygame.init()
        game.deal_6_cards_perplayer()
        game.game_statusID = 1000
        
    if game.game_statusID == 1000:
        game.run_level_loop()
        

    

pygame.quit()
sys.exit()

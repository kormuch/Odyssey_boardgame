#### Zuletzt: GUI Button Quit2 mit StatusID=1 zum laufen bringen

# Main class
import pygame
from GameEngine import ClassGameEngine
from GUI import ClassBoardGameGUI

# gui_loop.py
import sys



# Create an instance of the game engine
engine = ClassGameEngine()
gui = ClassBoardGameGUI()


while engine.game_statusID != 0:
    gui.runGUI()


# Ask for the number of players
players = engine.initialize_game()


while engine.game_statusID != 0:
    if engine.game_statusID == 1:
        pygame.init()
        engine.deal_6_cards_perplayer()
        engine.game_statusID = 1000
        
    if engine.game_statusID == 1000:
        engine.run_level_loop()
        

    

pygame.quit()
sys.exit()

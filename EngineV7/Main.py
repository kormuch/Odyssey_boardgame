# Main class
import pygame
from GameEngine import GameEngine
from GUI import BoardGameGUI

# gui_loop.py
import sys



# Create an instance of the game engine
game = GameEngine(actioncards_played=0, actioncounters={}, activePlayerID=1, currentActionKey="", 
             counter_userinput_execution=0, game_statusID=1, playerData={},
             possibleActionKeys_tuple=[], possibleActionValues_tuple=[], roundcounter=0, userInput="")
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

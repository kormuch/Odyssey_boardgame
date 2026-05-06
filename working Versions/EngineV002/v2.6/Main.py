# Main class
import pygame
from GameEngineV2 import GameEngine



# Create an instance of the game engine
game = GameEngine(actioncards_played=0, activePlayer=False, currentActionKey=None, 
             counter_battle=0, counter_fellowship=0, counter_artisanship=0,
             counter_journey=0, game_statusID=1, playerData={},
             possibleActions_tuple={}, roundcounter=0, turncounter=0)


#load arguments from json

# Ask for the number of players
players = game.initialize_game()


while game.game_statusID != 0:
    # Initialize pygame
    pygame.init()
    game.deal_6_cards_perplayer()
    game.game_statusID = 1000
    
    while game.game_statusID == 1000:
        game.run_level_loop()
        if game.actioncounter == 10:
            game.game_statusID = 0

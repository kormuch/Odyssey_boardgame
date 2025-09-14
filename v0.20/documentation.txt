# -*- coding: utf-8 -*-
"""
Created on Sun Oct  8 09:05:21 2023

@author: Korbinian Much

to do:
    lose actioncard needs to be standardized, one function for every actioncard


problem:    
    this does not work: no actions from list do match
    
    quote:
        elif user_input.lower() in self.tuple_possibleActions:
            for actionKey, list_actions in self.actionDictionary.items():
                for action in list_actions:
                    if user_input.lower() in list_actions:
                        print(f"user_input match: '{user_input}' found in '{actionKey}'")
                        print(f"returning actionKey '{actionKey}'")
                        return(actionKey)                        

solution:
    when get_actionKey_from_userInput is trigerred the current action is saved in a gamestate jsonfile

    


class GameEngine:
    initializes all values needed later in the game

def initialize_game:
    sets up the game: number of players, dealing out cards, cardcounter, turncounter
    
run_level_loop:
    * gets the active player
    * ask the active player for an input
    * processes the input
    * update the gamestate in a jsonfile
    * repeat with next player
    

    

ideas:
    choosing a strategy: you choose a faction and then a certain type of cards gets doubled
    example: 
        you choose dwarf craftsmen: starting cards "craftsmanship" gets doubled
        you choose rangers: journey cards get doubled



"""


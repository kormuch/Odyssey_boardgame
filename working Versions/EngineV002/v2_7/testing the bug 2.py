print("V3")

    
class GameEngine:
    def __init__(self, gamestate):
        self.gamestate = gamestate
        
    def update_gamestate(self):
        self.gamestate += 1
        return(self.gamestate)


game = GameEngine(gamestate=0)    
gamestate_2 = game.update_gamestate()


print(gamestate_2)
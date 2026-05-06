print("V1")
class GameEngine:
    def __init__(self, activePlayer):
        self.activePlayer = activePlayer

    def set_activePlayer(self):
        self.activePlayer = 0
        return(self.activePlayer)

    def update_gamestate(self, activePlayer):
        self.activePlayer = activePlayer
        print("update_gamestate executed")
        print(self.activePlayer)
    
game = GameEngine(1)    
game.update_gamestate(1)










print("V2")

y = 2

class GameEngine:
    def __init__(self, activePlayer):
        self.activePlayer = activePlayer

    def set_activePlayer(self):
        self.activePlayer = 0
        return(self.activePlayer)

    def update_gamestate(self, activePlayer):
        self.activePlayer = activePlayer
        print("update_gamestate executed")
        print(self.activePlayer)

game = GameEngine(y)    
game.update_gamestate(y)





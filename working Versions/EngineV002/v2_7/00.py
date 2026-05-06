print("V3")

    
class GameEngine:
    def __init__(self, actioncards_played, gamestate, activePlayer, game_statusID, turncounter):
        self.actioncards_played = 0
        self.gamestate = gamestate
        self.activePlayer = activePlayer
        self.game_statusID = game_statusID
        self.turncounter = turncounter
        
    def test_gamestate(self):
        self.gamestate += 1
        return(self.gamestate)

    def update_gamestate(self):
        print("update_gamestate executed")
        if self.actioncards_played < 2:
            self.turncounter += 1
            self.actioncards_played = 0
            print(f"level: {self.game_statusID} | turn: {self.turncounter}")
            return(self.turncounter, self.actioncards_played)



game = GameEngine(actioncards_played=0, gamestate=0, activePlayer=0, game_statusID=0, turncounter=0)    
gamestate_2 = game.update_gamestate()


print(gamestate_2)




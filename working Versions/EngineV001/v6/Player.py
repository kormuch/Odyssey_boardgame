class Player:
    def __init__(self, playerNumber, actioncards=None, actioncards_played=0, damageSuffered_player=0):
        self.playerNumber = playerNumber
        self.actioncards = actioncards if actioncards is not None else {}
        self.actioncards_played = actioncards_played
        self.damageSuffered_player = damageSuffered_player

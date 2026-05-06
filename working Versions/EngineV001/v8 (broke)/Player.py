class Player:
    def __init__(self, playerNumber):
        self.playerNumber = playerNumber
        self.actioncards = {}
        self.actioncards_played = 0  # Initialize the counter for played action cards
        self.damageSuffered_player = 0
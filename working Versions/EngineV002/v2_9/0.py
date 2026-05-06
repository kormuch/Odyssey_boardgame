num_players = 2
playerData = {}

if 1 <= num_players <= 5:
    playerData["numPlayers"] = num_players
    playerData["activePlayer"] = 1
    print(playerData)

    for playerID in range(1, num_players + 1):
        playerData["player " + str(playerID)] = {
            'playerID': playerID,
            'actioncards': {},
            'actioncards_played': 0,
            'endurance': 15,
            'activePlayer': False
        }

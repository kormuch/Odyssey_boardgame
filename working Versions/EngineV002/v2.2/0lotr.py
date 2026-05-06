import json

def get_active_player():
    with open("playerData.json", "r") as json_file:
        playerData = json.load(json_file)
        for player, playerAttributes in playerData.items():
            if playerAttributes["active_Player"] == True: 
                print(f"Active player found: {player}")
                print(f"PlayerID: {playerAttributes['playerID']}")
                
get_active_player()
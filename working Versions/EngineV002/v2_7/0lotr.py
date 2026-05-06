import json

with open("gamestate.json", "r") as json_file:
    gamestate = json.load(json_file)
    print(gamestate)

players = [1,2]
active_player = 0   
active_player = (active_player + 1) % len(players)

#active_player = 1
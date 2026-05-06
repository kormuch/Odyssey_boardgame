import json

with open("gamestate.json", "w") as json_file:
    gamestate = json.load(json_file)
    print(json_file)
    
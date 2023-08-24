import pygame
import json
from PlayerData import Player
from GameEngine import GameEngine

gamestatus = 1

# Ask for the number of players
while gamestatus == 1:
    num_players = input("Enter the number of players (1 to 5) or enter 'q' to quit: ")
    if num_players.isdigit() and 1 <= int(num_players) <= 5:
        num_players = int(num_players)
        break

    else:
        print("Invalid input. Please enter a number between 1 and 5.")

players = [Player(player_number) for player_number in range(1, num_players + 1)]

# Save player information to a JSON file
player_data = [{"playerNumber": player.playerNumber,
                "actioncards": player.actioncards,
                "actioncards_played": player.actioncards_played,
                "damageSuffered_player": player.damageSuffered_player}
               for player in players]

with open("players.json", "w") as json_file:
    json.dump(player_data, json_file, indent=4)

print("Player information saved to 'players.json'.")

# Now you can access player information using the players list
for player in players:
    print(f"Player {player.playerNumber}: {player.actioncards}")

# Initialize pygame
pygame.init()

# Create an instance of the game engine
game = GameEngine(gamestatus, players)

gamestatus = 1000

game.setup_lvl_0()

game.run_game_loop()

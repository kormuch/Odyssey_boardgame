import pygame
import json
from PlayerData import Player
from GameEngine import GameEngine


gamestatus = 1
# Ask for the number of players
while gamestatus == 1:
    num_players = input("Enter the number of players (1 to 5): ")
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
game = GameEngine()

gamestatus = 1000

game.setup_lvl_0()

while gamestatus == 1000:
    user_input = input("\nEnter a command (enter 'quit' or 'q' to exit): ")
    print("You entered:", user_input)

    if user_input.lower() == "quit" or user_input.lower() == "q":
        print("Exiting the program...")
        break

    elif user_input.lower() == "joker" or user_input.lower() == "0":
        if game.actioncards["joker"] > 0:
            user_input_joker = input("\nEnter an action (enter 'quit' or 'q' to exit): ")
            if user_input_joker.lower() == "fight" or user_input_joker.lower() == "1":
                fight_counter = game.handle_actions("fight")
                print("Fight Counter:", fight_counter)
            elif user_input_joker.lower() == "friendship" or user_input_joker.lower() == "2":
                friendship_counter = game.handle_actions("friendship")
                print("Friendship Counter:", friendship_counter)
            elif user_input_joker.lower() == "hide" or user_input_joker.lower() == "3":
                hide_counter = game.handle_actions("hide")
                print("Hide Counter:", hide_counter)
            elif user_input_joker.lower() == "run" or user_input_joker.lower() == "4":
                run_counter = game.handle_actions("run")
                print("Run Counter:", run_counter)
            game.actioncards["joker"] -= 1
        else:
            print('no joker available')
    elif user_input.lower() == "fight" or user_input.lower() == "1":
        fight_counter = game.handle_actions("fight")
        print("Fight Counter:", fight_counter)
    elif user_input.lower() == "friendship" or user_input.lower() == "2":
        friendship_counter = game.handle_actions("friendship")
        print("Friendship Counter:", friendship_counter)
    elif user_input.lower() == "hide" or user_input.lower() == "3":
        hide_counter = game.handle_actions("hide")
        print("Hide Counter:", hide_counter)
    elif user_input.lower() == "run" or user_input.lower() == "4":
        run_counter = game.handle_actions("run")
        print("Run Counter:", run_counter)

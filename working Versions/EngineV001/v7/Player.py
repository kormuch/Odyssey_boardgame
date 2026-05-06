class Player:
    def __init__(self, playerNumber):
        self.playerNumber = playerNumber
        self.actioncards = {}
        self.actioncards_played = 0  # Initialize the counter for played action cards
        self.damageSuffered_player = 0


    def play_action_card(self, card_type):
        if card_type.isdigit():
            card_type = int(card_type)
        card_type = self.convert_input_to_action(card_type)
        if card_type:
            if self.actioncards[card_type] > 0:
                self.actioncards[card_type] -= 1
                self.actioncards_played += 1
                return True
            else:
                print("You don't have that card to play.")
                return False
        else:
            print("Invalid input. Please enter a valid action card.")
            return False

    def convert_input_to_action(self, input_value):
        if isinstance(input_value, int) or input_value.isdigit():
            input_value = int(input_value)
            if input_value == 1 or input_value == "fight":
                return "fight"
            elif input_value == 2 or input_value == "friendship":
                return "friendship"
            elif input_value == 3 or input_value == "hide":
                return "hide"
            elif input_value == 4 or input_value == "run":
                return "run"
            else:
                return None
        elif isinstance(input_value, str):
            input_value = input_value.lower()
            if input_value in ["fight", "friendship", "hide", "run"]:
                return input_value
            else:
                return None
        else:
            return None
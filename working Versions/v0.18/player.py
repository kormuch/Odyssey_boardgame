from actioncard import ActionCardManager

class Player:
    """
    Handles all player-specific data and operations
    """
    
    def __init__(self, player_id, starting_endurance=15, card_manager=None):
        self.player_id = player_id
        self.actioncards = {}
        self.actioncards_played = 0
        self.endurance = starting_endurance
        self.is_active = False
        
        # Use provided card manager or create default one
        self.card_manager = card_manager if card_manager else ActionCardManager()
    
    def initialize_actioncards(self, card_names=None):
        """Initialize empty actioncards dict with all possible card types"""
        if card_names is None:
            card_names = self.card_manager.get_all_card_names()
        
        self.actioncards = {card_name: 0 for card_name in card_names}
    
    def deal_cards(self, num_cards=6):
        """Deal random cards to this player using ActionCardManager"""
        if not self.actioncards:
            self.initialize_actioncards()
        
        # Use card manager to deal cards
        card_counts = self.card_manager.deal_random_cards(num_cards)
        
        # Update player's hand
        for card_name, count in card_counts.items():
            if card_name in self.actioncards:
                self.actioncards[card_name] = count
        
        print(f"Player {self.player_id} dealt cards:", self.actioncards)
        return self.actioncards
    
    def has_card(self, card_name):
        """Check if player has a specific card type"""
        return self.actioncards.get(card_name, 0) > 0
    
    def play_card(self, card_name):
        """
        Try to play a specific card type
        Returns True if successful, False if not enough cards
        """
        if self.has_card(card_name):
            self.actioncards[card_name] -= 1
            self.actioncards_played += 1
            print(f"Player {self.player_id} played '{card_name}'")
            print(f"Remaining cards:", self.actioncards)
            return True
        elif self.has_card('joker'):
            # Use joker as substitute
            self.actioncards['joker'] -= 1
            self.actioncards_played += 1
            print(f"Player {self.player_id} used joker for '{card_name}'")
            print(f"Remaining cards:", self.actioncards)
            return True
        else:
            print(f"Player {self.player_id} doesn't have '{card_name}' or joker cards")
            return False
    
    def can_play_card(self, card_name):
        """Check if player can play a specific card (including joker substitute)"""
        return self.has_card(card_name) or self.has_card('joker')
    
    def get_card_count(self, card_name):
        """Get number of specific card type"""
        return self.actioncards.get(card_name, 0)
    
    def get_total_cards(self):
        """Get total number of cards in hand"""
        return sum(self.actioncards.values())
    
    def get_playable_cards(self):
        """Get list of cards player can currently play"""
        playable = []
        for card_name, count in self.actioncards.items():
            if count > 0:
                playable.append(card_name)
        return playable
    
    def set_active(self, active=True):
        """Set player as active or inactive"""
        self.is_active = active
    
    def reset_cards_played(self):
        """Reset the counter for cards played this round"""
        self.actioncards_played = 0
    
    def set_card_manager(self, card_manager):
        """Set the card manager for this player"""
        self.card_manager = card_manager
    
    def to_dict(self):
        """Convert player data to dictionary format (for JSON saving)"""
        return {
            'playerID': self.player_id,
            'actioncards': self.actioncards.copy(),
            'actioncards_played': self.actioncards_played,
            'endurance': self.endurance,
            'activePlayer': self.is_active
        }
    
    @classmethod
    def from_dict(cls, data, card_manager=None):
        """Create Player instance from dictionary data (for JSON loading)"""
        player = cls(data['playerID'], data.get('endurance', 15), card_manager)
        player.actioncards = data.get('actioncards', {})
        player.actioncards_played = data.get('actioncards_played', 0)
        player.is_active = data.get('activePlayer', False)
        return player
    
    def __str__(self):
        return f"Player {self.player_id} - Cards: {self.actioncards}, Endurance: {self.endurance}, Active: {self.is_active}"
    
    def __repr__(self):
        return self.__str__()
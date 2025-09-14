from actioncard import ActionCardManager

class Player:
    """
    Handles all player-specific data and operations
    """
    
    def __init__(self, player_id, starting_endurance=15, card_manager=None):
        self.player_id = player_id
        self.endurance = starting_endurance
        self.is_active = False
        self.actioncards_played = 0
        
        # Use provided card manager or create default one
        self.card_manager = card_manager if card_manager else ActionCardManager()
        
        # Initialize actioncards dictionary with all available cards
        self._initialize_actioncards()
    
    def _initialize_actioncards(self):
        """Initialize actioncards dictionary with all available card types set to 0"""
        card_names = self.card_manager.get_all_card_names()
        self.actioncards = {card_name: 0 for card_name in card_names}
    
    # =============================================================================
    # CARD MANAGEMENT
    # =============================================================================
    
    def deal_cards(self, num_cards=6):
        """
        Deal random cards to this player
        
        Args:
            num_cards: Number of cards to deal (default: 6)
            
        Returns:
            dict: Updated actioncards dictionary
        """
        card_counts = self.card_manager.deal_random_cards(num_cards)
        
        # Add dealt cards to player's hand
        for card_name, count in card_counts.items():
            if card_name in self.actioncards:
                self.actioncards[card_name] += count
            else:
                # Handle case where new card types are added to card manager
                self.actioncards[card_name] = count
        
        return self.actioncards
    
    def has_card(self, card_name):
        """Check if player has at least one of the specified card"""
        return self.actioncards.get(card_name, 0) > 0
    
    def play_card(self, card_name):
        """
        Attempt to play a card from player's hand
        
        Args:
            card_name: Name of the card to play
            
        Returns:
            bool: True if card was successfully played, False otherwise
        """
        if self.has_card(card_name):
            self.actioncards[card_name] -= 1
            self.actioncards_played += 1
            return True
        elif self.has_card('joker'):
            # Use joker as substitute
            self.actioncards['joker'] -= 1
            self.actioncards_played += 1
            return True
        return False
    
    def can_play_card(self, card_name):
        """Check if player can play the specified card (either has it or has joker)"""
        return self.has_card(card_name) or self.has_card('joker')
    
    def get_card_count(self, card_name):
        """Get the number of a specific card type in player's hand"""
        return self.actioncards.get(card_name, 0)
    
    def get_total_cards(self):
        """Get total number of cards in player's hand"""
        return sum(self.actioncards.values())
    
    def get_playable_cards(self):
        """Get list of card names that player currently has (count > 0)"""
        return [card_name for card_name, count in self.actioncards.items() if count > 0]
    
    def add_card(self, card_name, count=1):
        """
        Add cards to player's hand
        
        Args:
            card_name: Name of the card to add
            count: Number of cards to add (default: 1)
        """
        if card_name in self.actioncards:
            self.actioncards[card_name] += count
        else:
            self.actioncards[card_name] = count
    
    def remove_card(self, card_name, count=1):
        """
        Remove cards from player's hand
        
        Args:
            card_name: Name of the card to remove
            count: Number of cards to remove (default: 1)
            
        Returns:
            bool: True if cards were successfully removed, False if not enough cards
        """
        current_count = self.actioncards.get(card_name, 0)
        if current_count >= count:
            self.actioncards[card_name] = current_count - count
            return True
        return False
    
    # =============================================================================
    # PLAYER STATE MANAGEMENT
    # =============================================================================
    
    def set_active(self, active=True):
        """Set player's active status"""
        self.is_active = active
    
    def reset_for_new_round(self):
        """Reset player state for a new round"""
        self.actioncards_played = 0
    
    def take_damage(self, damage):
        """Reduce player's endurance"""
        self.endurance = max(0, self.endurance - damage)
        return self.endurance
    
    def heal(self, amount):
        """Increase player's endurance"""
        self.endurance += amount
        return self.endurance
    
    def is_alive(self):
        """Check if player has endurance remaining"""
        return self.endurance > 0
    
    # =============================================================================
    # SERIALIZATION
    # =============================================================================
    
    def to_dict(self):
        """Convert player data to dictionary for saving"""
        return {
            'playerID': self.player_id,
            'actioncards': self.actioncards.copy(),
            'actioncards_played': self.actioncards_played,
            'endurance': self.endurance,
            'activePlayer': self.is_active
        }
    
    @classmethod
    def from_dict(cls, data, card_manager=None):
        """
        Create Player instance from dictionary data
        
        Args:
            data: Dictionary containing player data
            card_manager: ActionCardManager instance (optional)
            
        Returns:
            Player: New Player instance with loaded data
        """
        player = cls(
            player_id=data['playerID'], 
            starting_endurance=data.get('endurance', 15),
            card_manager=card_manager
        )
        
        # Load saved state
        player.actioncards = data.get('actioncards', {})
        player.actioncards_played = data.get('actioncards_played', 0)
        player.is_active = data.get('activePlayer', False)
        
        # Ensure all current card types exist in actioncards
        # (in case new cards were added since save)
        current_cards = player.card_manager.get_all_card_names()
        for card_name in current_cards:
            if card_name not in player.actioncards:
                player.actioncards[card_name] = 0
        
        return player
    
    # =============================================================================
    # STRING REPRESENTATION
    # =============================================================================
    
    def __str__(self):
        active_status = "Active" if self.is_active else "Inactive"
        total_cards = self.get_total_cards()
        return f"Player {self.player_id} - {total_cards} cards, {self.endurance} endurance, {active_status}"
    
    def __repr__(self):
        return f"Player(id={self.player_id}, endurance={self.endurance}, active={self.is_active}, cards={self.get_total_cards()})"
    
    def detailed_info(self):
        """Get detailed information about player's current state"""
        info = [
            f"Player {self.player_id}:",
            f"  Endurance: {self.endurance}",
            f"  Status: {'Active' if self.is_active else 'Inactive'}",
            f"  Cards played this turn: {self.actioncards_played}",
            f"  Total cards in hand: {self.get_total_cards()}",
            "  Card breakdown:"
        ]
        
        for card_name, count in sorted(self.actioncards.items()):
            if count > 0:
                info.append(f"    {card_name}: {count}")
        
        return "\n".join(info)
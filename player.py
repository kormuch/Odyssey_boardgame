# player.py
from actioncard import ActionCardManager
from gamelog import logger


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
        
        logger.game_debug(f"Player {player_id} created with {starting_endurance} endurance")
    
    def _initialize_actioncards(self):
        """Initialize actioncards dictionary with all available card types set to 0"""
        card_names = self.card_manager.get_all_card_names()
        self.actioncards = {card_name: 0 for card_name in card_names}
    
    # =============================================================================
    # CARD MANAGEMENT
    # =============================================================================
    
    def deal_cards(self, num_cards=6):
        """Deal random cards to this player"""
        card_counts = self.card_manager.deal_random_cards(num_cards)
        for card_name, count in card_counts.items():
            self.actioncards[card_name] = self.actioncards.get(card_name, 0) + count
        
        # Log only non-zero cards for cleaner output
        dealt = {k: v for k, v in card_counts.items() if v > 0}
        logger.player_action(
            self.player_id, 
            f"Received {num_cards} cards",
            cards=dealt,
            total_cards=self.get_total_cards()
        )
        return self.actioncards
    
    def has_card(self, card_name):
        """Check if player has at least one of the specified card"""
        return self.actioncards.get(card_name, 0) > 0
    
    def play_card(self, card_name):
        """Attempt to play a card, using joker as fallback"""
        if self.has_card(card_name):
            self.actioncards[card_name] -= 1
            self.actioncards_played += 1
            logger.player_action(
                self.player_id,
                f"Played {card_name}",
                cards_played_total=self.actioncards_played,
                remaining_count=self.actioncards[card_name]
            )
            return True
        elif self.has_card('joker'):
            self.actioncards['joker'] -= 1
            self.actioncards_played += 1
            logger.player_action(
                self.player_id,
                f"Played joker as {card_name}",
                cards_played_total=self.actioncards_played,
                jokers_remaining=self.actioncards['joker']
            )
            return True
        
        logger.warning(f"Player {self.player_id} cannot play '{card_name}' - insufficient cards")
        return False
    
    def can_play_card(self, card_name):
        """Check if player can play the specified card (own or joker)"""
        return self.has_card(card_name) or self.has_card('joker')
    
    def get_card_count(self, card_name):
        """Get the number of a specific card type in hand"""
        return self.actioncards.get(card_name, 0)
    
    def get_total_cards(self):
        """Get total number of cards in hand"""
        return sum(self.actioncards.values())
    
    def get_playable_cards(self):
        """Get list of card names currently playable (count > 0)"""
        return [name for name, count in self.actioncards.items() if count > 0]
    
    def add_card(self, card_name, count=1):
        """Add cards to hand"""
        self.actioncards[card_name] = self.actioncards.get(card_name, 0) + count
        logger.game_debug(f"Player {self.player_id} received {count}x {card_name}")
    
    def remove_card(self, card_name, count=1):
        """Remove cards from hand if enough available"""
        if self.actioncards.get(card_name, 0) >= count:
            self.actioncards[card_name] -= count
            logger.game_debug(f"Player {self.player_id} lost {count}x {card_name}")
            return True
        logger.warning(f"Player {self.player_id} cannot remove {count}x {card_name} - insufficient cards")
        return False
    
    # =============================================================================
    # PLAYER STATE MANAGEMENT
    # =============================================================================
    
    def set_active(self, active=True):
        """Set player's active status"""
        old_state = self.is_active
        self.is_active = active
        if old_state != active:
            logger.state_change(
                f"player_{self.player_id}_active",
                old_state,
                active
            )
    
    def reset_for_new_round(self):
        """Reset player-specific counters for new round"""
        old_count = self.actioncards_played
        self.actioncards_played = 0
        logger.player_action(
            self.player_id,
            "Round reset",
            cards_played_last_round=old_count
        )
    
    def take_damage(self, damage):
        """Reduce endurance, not below 0"""
        old_endurance = self.endurance
        self.endurance = max(0, self.endurance - damage)
        logger.player_action(
            self.player_id,
            f"Took {damage} damage",
            old_endurance=old_endurance,
            new_endurance=self.endurance
        )
        return self.endurance
    
    def heal(self, amount):
        """Increase endurance"""
        old_endurance = self.endurance
        self.endurance += amount
        logger.player_action(
            self.player_id,
            f"Healed {amount}",
            old_endurance=old_endurance,
            new_endurance=self.endurance
        )
        return self.endurance
    
    def is_alive(self):
        """Check if player is alive"""
        return self.endurance > 0
    
    # =============================================================================
    # SERIALIZATION
    # =============================================================================
    
    def to_dict(self):
        """Convert player data to dict for saving"""
        return {
            'playerID': self.player_id,
            'actioncards': self.actioncards.copy(),
            'actioncards_played': self.actioncards_played,
            'endurance': self.endurance,
            'activePlayer': self.is_active
        }
    
    @classmethod
    def from_dict(cls, data, card_manager=None):
        """Reconstruct Player from dictionary"""
        player = cls(
            player_id=data['playerID'], 
            starting_endurance=data.get('endurance', 15),
            card_manager=card_manager
        )
        player.actioncards = data.get('actioncards', {})
        player.actioncards_played = data.get('actioncards_played', 0)
        player.is_active = data.get('activePlayer', False)
        
        # Ensure all current card types exist in actioncards
        for card_name in player.card_manager.get_all_card_names():
            player.actioncards.setdefault(card_name, 0)
        
        logger.info(f"Player {player.player_id} loaded from save data")
        return player
    
    # =============================================================================
    # STRING REPRESENTATION
    # =============================================================================
    
    def __str__(self):
        status = "Active" if self.is_active else "Inactive"
        return f"Player {self.player_id} - {self.get_total_cards()} cards, {self.endurance} endurance, {status}"
    
    def __repr__(self):
        return f"Player(id={self.player_id}, endurance={self.endurance}, active={self.is_active}, cards={self.get_total_cards()})"
    
    def detailed_info(self):
        """Detailed multiline info about player"""
        info = [
            f"Player {self.player_id}:",
            f"  Endurance: {self.endurance}",
            f"  Status: {'Active' if self.is_active else 'Inactive'}",
            f"  Cards played this turn: {self.actioncards_played}",
            f"  Total cards in hand: {self.get_total_cards()}",
            "  Card breakdown:"
        ]
        for name, count in sorted(self.actioncards.items()):
            if count > 0:
                info.append(f"    {name}: {count}")
        return "\n".join(info)
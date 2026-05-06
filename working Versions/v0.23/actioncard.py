# actioncard.py
import random
from gamelog import logger


class ActionCard:
    """
    Represents a single action card type with its properties
    """

    def __init__(self, name, keywords, effect=None, category="basic"):
        self.name = name
        self.keywords = keywords if isinstance(keywords, list) else [keywords]
        self.effect = effect if effect else {}
        self.category = category
        logger.game_debug(f"ActionCard created: {self.name} (keywords={self.keywords}, category={self.category})")

    def has_effect(self):
        """Check if card has an effect"""
        return bool(self.effect)

    def get_effect_value(self):
        """Get the effect value for this card"""
        return self.effect.get(self.name, 0) if self.has_effect() else 0

    def matches_keyword(self, keyword):
        """Check if keyword matches this card"""
        return keyword.lower() in [k.lower() for k in self.keywords]

    def __str__(self):
        return f"ActionCard({self.name}, keywords={self.keywords}, effect={self.effect})"

    def __repr__(self):
        return self.__str__()


class ActionCardManager:
    """
    Manages all action cards, their definitions, and related operations
    """

    def __init__(self):
        self.cards = {}  # name -> ActionCard
        self.shortcut_mapping = {}
        logger.info("ActionCardManager initializing...")
        self._initialize_default_cards()
        self._build_shortcut_mapping()
        logger.info(f"ActionCardManager ready with {len(self.cards)} card types")

    def _initialize_default_cards(self):
        """Initialize the default card set"""
        card_definitions = [
            ("battle", ["battle", "b"], {"battle": 1}, "combat"),
            ("fellowship", ["fellowship", "f"], {"fellowship": 1}, "social"),
            ("wits", ["wits", "cr"], {"wits": 1}, "skill"),
            ("journey", ["journey", "j"], {"journey": 1}, "exploration"),
            ("joker", ["joker"], {}, "special"),
            ("2x battle", ["double battle", "bb"], {"battle": 2}, "combat"),
            ("2x fellowship", ["double fellowship", "ff"], {"fellowship": 2}, "social"),
            ("2x wits", ["double wits", "ww"], {"wits": 2}, "skill"),
            ("2x journey", ["double journey", "jj"], {"journey": 2}, "exploration"),
            ("2x joker", ["double joker"], {}, "special")
        ]

        for name, keywords, effect, category in card_definitions:
            self.add_card(name, keywords, effect, category)
        
        logger.game_debug(f"Loaded {len(card_definitions)} default card types")

    def _build_shortcut_mapping(self):
        """Build mapping from shortcuts to full card names"""
        self.shortcut_mapping = {}
        for card_name, card in self.cards.items():
            for keyword in card.keywords:
                if keyword != card_name:
                    self.shortcut_mapping[keyword.lower()] = card_name

    def add_card(self, name, keywords, effect=None, category="basic"):
        """Add a new card to the manager"""
        card = ActionCard(name, keywords, effect, category)
        self.cards[name] = card
        self._build_shortcut_mapping()
        logger.info(f"Card registered: {name}")

    def get_card(self, name):
        """Get card by name"""
        return self.cards.get(name)

    def get_card_by_keyword(self, keyword):
        """Get card by any of its keywords"""
        keyword_lower = keyword.lower()
        for card_name, card in self.cards.items():
            if card_name.lower() == keyword_lower or card.matches_keyword(keyword):
                return card
        return None

    def resolve_input_to_card_name(self, user_input):
        """Convert user input (including shortcuts) to full card name"""
        user_input_lower = user_input.lower()
        
        # Check shortcut mapping first
        if user_input_lower in self.shortcut_mapping:
            resolved = self.shortcut_mapping[user_input_lower]
            logger.game_debug(f"Input '{user_input}' resolved via shortcut → '{resolved}'")
            return resolved

        # Check exact match
        for card_name in self.cards.keys():
            if card_name.lower() == user_input_lower:
                logger.game_debug(f"Input '{user_input}' matched exactly → '{card_name}'")
                return card_name

        logger.warning(f"Could not resolve input '{user_input}' to any card")
        return None

    def get_all_card_names(self):
        return tuple(self.cards.keys())

    def get_all_keywords(self):
        keywords = [k for card in self.cards.values() for k in card.keywords]
        return tuple(keywords)

    def get_basic_cards(self):
        basic_cards = [name for name, card in self.cards.items()
                       if not name.startswith("2x") and card.category != "special"]
        return basic_cards

    def get_cards_by_category(self, category):
        return [name for name, card in self.cards.items() if card.category == category]

    def deal_random_cards(self, num_cards=6, card_pool=None):
        """Deal random cards from available pool"""
        if card_pool is None:
            card_pool = self.get_basic_cards()

        dealt_cards = [random.choice(card_pool) for _ in range(num_cards)]
        dealt_cards.sort()
        card_counts = {card_name: dealt_cards.count(card_name) for card_name in card_pool}
        
        # Log summary only
        non_zero = {k: v for k, v in card_counts.items() if v > 0}
        logger.info(f"Dealt {num_cards} cards: {non_zero}")
        return card_counts

    def get_legacy_action_dictionary(self):
        legacy_dict = {}
        for card_name, card in self.cards.items():
            if card.category == "special":
                legacy_dict[card_name] = card.keywords
            else:
                legacy_dict[card_name] = {"keywords": card.keywords, "effect": card.effect}
        return legacy_dict

    def validate_input(self, user_input):
        valid = user_input.lower() in [k.lower() for k in self.get_all_keywords()]
        if not valid:
            logger.game_debug(f"Invalid input: '{user_input}'")
        return valid

    def trigger_card_effect(self, card_name, action_paths):
        card = self.get_card(card_name)
        if not card or not card.has_effect():
            logger.game_debug(f"No effect to trigger for '{card_name}'")
            return card_name

        for effect_key, effect_value in card.effect.items():
            if effect_key in action_paths:
                old_value = action_paths[effect_key]
                action_paths[effect_key] += effect_value
                logger.state_change(
                    f"action_path.{effect_key}",
                    old_value,
                    action_paths[effect_key],
                    card=card_name,
                    effect_value=effect_value
                )

        return action_paths

    def __len__(self):
        return len(self.cards)

    def __iter__(self):
        return iter(self.cards.values())

    def __contains__(self, card_name):
        return card_name in self.cards
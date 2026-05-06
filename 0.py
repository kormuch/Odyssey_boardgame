To apply **composition over inheritance** for card behaviors, define behaviors as standalone, reusable components (classes or functions), then have each card instance "own" or use these behavior objects rather than inheriting methods from a parent class. This keeps card logic flexible and mix-and-match, avoiding rigid inheritance trees.[1][3]

***

## How to Implement Behavior Composition

### Step 1: Define Behavior Classes

Instead of building a class hierarchy (`BattleCard`, `JourneyCard`, etc.), define separate **behavior classes** for each possible action a card can perform.

```python
class EffectBehavior:
    def apply(self, game, player):
        pass

class BattleEffect(EffectBehavior):
    def apply(self, game, player):
        # logic for battle effect
        print(f"{player.name} triggers a battle!")
        # Update game state as needed

class FellowshipEffect(EffectBehavior):
    def apply(self, game, player):
        print(f"{player.name} triggers fellowship!")
        # Update game state
```

***

### Step 2: Compose Cards with Behaviors

Each card "has-a" behavior object, and delegates effect logic to that object.

```python
class Card:
    def __init__(self, name, behavior):
        self.name = name
        self.behavior = behavior  # Composed object

    def play(self, game, player):
        self.behavior.apply(game, player)
```

***

### Step 3: Create Cards by Combining Components

You can now easily mix and match behaviors without duplicating code or creating new subclasses for every card type.

```python
# Examples:
battle_card = Card("battle", BattleEffect())
fellowship_card = Card("fellowship", FellowshipEffect())
# Add more cards and behaviors as needed
```

***

## Advantages

- **Flexibility:** Add new card types or effects by simply creating new behaviors and composing them into cards.[3]
- **Maintainability:** All card logic is isolated in small testable units, not tangled together in subclasses.[1]
- **Extensibility:** Easily experiment with new rules, effects, or stack behaviors by combining components.
- **Avoids Rigid Inheritance Hierarchies:** The code remains modular and not locked into hard-to-alter family trees.[3]

***

**Summary:**  
Define each card's special behavior as a dedicated class or component, and compose card objects by including or referencing these behaviors, rather than inheriting from a base `Card` class. This keeps the game engine flexible, maintainable, and easy to extend.[1][3]

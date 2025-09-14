# Main class
import pygame
import sys

def main():
    try:
        # Import the GUI class
        from gui import ClassBoardGameGUI
        
        # Create GUI instance (it will handle GameEngine loading internally)
        gui = ClassBoardGameGUI()  # No parameters - use your existing class as-is
        engine = gui.engine
        
        # Initialize the game
        print("Initializing game...")
        players = engine.initialize_game()
        print(f"Game initialized with {players} players")
        print(f"Initial game status: {engine.game_statusID}")
        
        # Main game loop
        while engine.game_statusID != -1:
            print(f"Current game status: {engine.game_statusID}")
            
            if engine.game_statusID == 1:
                print("Running initialization GUI...")
                gui.runGUI_initialize_game()
                
            elif engine.game_statusID == 1000:
                print("Running main game GUI...")
                gui.runGUI_game()
                
                # If you want the game to continue running, add your game logic here
                # For now, we'll break to prevent infinite loop
                print("Game loop completed")
                break
                
            else:
                print(f"Unknown game status: {engine.game_statusID}")
                break
                
    except ImportError as e:
        print(f"Import error: {e}")
        print("Make sure GUI.py exists in the same directory")
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Clean up
        try:
            pygame.quit()
        except:
            pass
        print("Program ended")

if __name__ == "__main__":
    main()
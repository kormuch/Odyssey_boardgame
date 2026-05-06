import pygame
from gamelog import setup_logger

logger = setup_logger()  # New logfile per session

def main():
    logger.info("Starting main program...")
    try:
        from gui import ClassBoardGameGUI
        gui = ClassBoardGameGUI()
        engine = gui.engine

        logger.info("Initializing game...")
        players = engine.initialize_game()
        logger.info(f"Game initialized with {players} players")

        while engine.game_statusID != -1:
            logger.info(f"Current game status: {engine.game_statusID}")

            if engine.game_statusID == 1:
                logger.info("Running initialization GUI...")
                gui.runGUI_initialize_game()

            elif engine.game_statusID == 1000:
                logger.info("Running main game GUI...")
                gui.runGUI_game()
                logger.info("Game loop completed")
                break

            else:
                logger.warning(f"Unknown game status: {engine.game_statusID}")
                break

    except Exception as e:
        logger.exception(f"An error occurred: {e}")
    finally:
        try:
            pygame.quit()
        except:
            pass
        logger.info("Program ended")

if __name__ == "__main__":
    main()

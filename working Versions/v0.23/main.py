#main.py
import pygame
from gamelog import setup_logger

# Initialize logger at the very start
logger = setup_logger(debug_ui=False, debug_game=True, keep_logs_days=7)

def main():
    logger.info("=" * 60)
    logger.info("=== ODYSSEY GAME STARTING ===")
    logger.info("=" * 60)
    
    try:
        from gui import ClassBoardGameGUI
        
        logger.info("Initializing GUI...")
        gui = ClassBoardGameGUI()
        engine = gui.engine

        logger.info("Initializing game with default settings...")
        players = engine.initialize_game()
        logger.game_event("game_setup_complete", players=players)

        # Main game loop
        while engine.game_statusID != -1:
            current_status = engine.game_statusID
            logger.game_debug(f"Game loop iteration - status: {current_status}")

            if engine.game_statusID == 1:
                logger.info("--- Entering initialization screen ---")
                gui.runGUI_initialize_game()
                logger.info("--- Initialization screen completed ---")

            elif engine.game_statusID == 1000:
                logger.info("--- Entering main game screen ---")
                gui.runGUI_game()
                logger.info("--- Main game screen exited ---")
                break

            else:
                logger.warning(f"Unknown game status encountered: {engine.game_statusID}")
                break

    except KeyboardInterrupt:
        logger.info("=== Game interrupted by user (Ctrl+C) ===")
    except Exception as e:
        logger.error(f"=== FATAL ERROR ===")
        logger.exception(f"Unhandled exception: {e}")
    finally:
        try:
            pygame.quit()
            logger.info("Pygame shut down cleanly")
        except:
            pass
        
        logger.info("=" * 60)
        logger.info("=== ODYSSEY GAME ENDED ===")
        logger.info("=" * 60)

if __name__ == "__main__":
    main()
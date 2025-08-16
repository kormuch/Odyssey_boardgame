# gui_loop.py
import pygame
import sys
import GUI_functions as guif



# Initialize Pygame
pygame.init()


# Main game loop

def run_GUI():
    running = True
    button_clicked = None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if any button is clicked
                mouse_pos = pygame.mouse.get_pos()
                for i, button_text in enumerate(guif.buttons):
                    button_rect = pygame.Rect(i * guif.button_width, guif.button_start_y, guif.button_width, guif.button_height)
                    if button_rect.collidepoint(mouse_pos):
                        button_clicked = button_text
                        break
                else:
                    button_clicked = None
    
        guif.screen.fill(guif.SCREEN_COLOR)
        # Draw game elements using functions
        guif.draw_image_space()
        guif.draw_textbox("This is some text for the textbox.")
        guif.draw_progress_bar()
        guif.draw_paths()
        guif.draw_buttons()
    
        # Handle button click
        if button_clicked:
            print(f"Button clicked: {button_clicked}")
            button_clicked = None  # Reset the button state
    
        pygame.display.flip()

run_GUI()
pygame.quit()
sys.exit()
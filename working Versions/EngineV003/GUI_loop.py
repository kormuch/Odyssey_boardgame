import pygame
import sys
from GUI_functions import *


# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Draw background
    screen.fill(BACKGROUND_COLOR)

    # Draw game elements using functions
    draw_image_space()
    draw_textbox("This is some text for the textbox.")
    draw_progress_bar()
    draw_paths()
    draw_buttons()

    pygame.display.flip()
import pygame
import sys
import GameEngine as engine

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 700
BACKGROUND_COLOR = (152, 251, 152)  # Shades of green
SCREEN_COLOR = (152, 251, 152)  # Shades of green
PROGRESS_BAR_COLOR = (255, 255, 255)
PATH_COLOR = (255, 255, 255)
BUTTON_COLOR = (255, 255, 255)

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Board Game Interface")

def draw_image_space():
    """Draws the black rectangle for the image space."""
    image_space_height = HEIGHT // 3
    image_space = pygame.Rect(WIDTH // 4, 0, WIDTH // 2, image_space_height)
    pygame.draw.rect(screen, (0, 0, 0), image_space)

def draw_textbox(text):
    """Draws the textbox with the given text."""
    textbox_font = pygame.font.Font(None, 24)
    text_surface = textbox_font.render(text, True, (0, 0, 0))
    text_width, text_height = text_surface.get_size()
    textbox_x = WIDTH // 4
    textbox_y = (HEIGHT // 3) + 10
    textbox_rect = pygame.Rect(textbox_x, textbox_y, text_width, text_height)
    pygame.draw.rect(screen, (255, 255, 255), textbox_rect)
    screen.blit(text_surface, textbox_rect)

def draw_progress_bar():
    """Draws the progress bar with 20 squares."""
    progress_bar_offset_x = 0
    progress_bar_y = (HEIGHT // 3) + 35 
    border_thickness = 1
    for step in range(1, 21):
        border_color = (0, 0, 0)
        pygame.draw.rect(screen, border_color, (step * (WIDTH // 22) + progress_bar_offset_x, 
                                                progress_bar_y, WIDTH // 20, 20), border_thickness)
        pygame.draw.rect(screen, PROGRESS_BAR_COLOR, (step * (WIDTH // 22) + progress_bar_offset_x + border_thickness, 
                                                progress_bar_y + border_thickness, 
                                                WIDTH // 20 - 2*border_thickness, 20 - 2*border_thickness))

def draw_paths():
    """Draws four paths with 10 circles each."""
    path_start_y = (HEIGHT // 3) + 95
    path_spacing = 48
    path_offset_x = 0
    for path in range(4):
        for step in range(1, 11):
            circle_radius = 15
            circle_x = step * (WIDTH // 25) + path_offset_x
            circle_y = path_start_y + path * path_spacing
            pygame.draw.circle(screen, PATH_COLOR, (circle_x, circle_y), circle_radius)



# Global variables
buttons = ["Battle", "Craftsmanship", "Fellowship", "Journey"]  # Define buttons globally
button_height = 50
button_margin_bottom = 10
button_start_y = HEIGHT - button_height - button_margin_bottom  # Assuming HEIGHT is defined
button_width = WIDTH // 4  # Assuming WIDTH is defined


def draw_buttons():
    """Draws buttons as per the globally defined 'buttons' list."""
    button_font = pygame.font.Font(None, 36)

    for i, button_text in enumerate(buttons):
        button_rect = pygame.Rect(i * button_width, button_start_y, button_width, button_height)
        pygame.draw.rect(screen, BUTTON_COLOR, button_rect)  # Assuming BUTTON_COLOR and screen are defined
        text_surface = button_font.render(button_text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=button_rect.center)
        screen.blit(text_surface, text_rect)
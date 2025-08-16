import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 700
BACKGROUND_COLOR = (152, 251, 152)  # Shades of green
PROGRESS_BAR_COLOR = (255, 255, 255)
PATH_COLOR = (255, 255, 255)
BUTTON_COLOR = (255, 255, 255)
BUTTON_HOVER_COLOR = (0,0,0)

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Board Game Interface")



def draw_button(screen, button_rect, button_text, color, hover_color, pressed=False):
    if pressed:
        button_color = hover_color
        button_rect.move_ip(0, 2)  # Move the button down slightly when pressed
    else:
        button_color = color

    pygame.draw.rect(screen, button_color, button_rect)
    pygame.draw.rect(screen, (0, 0, 0), button_rect, 2)  # Draw button border

    text_surface = button_font.render(button_text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)

# Draw buttons at the bottom, below the paths
button_font = pygame.font.Font(None, 36)
buttons = ["Battle", "Craftsmanship", "Fellowship", "Journey"]
button_height = 50
button_margin_bottom = 10  # Margin between buttons and bottom screen edge

# Calculate the bottom position for buttons, leaving a margin at the bottom
button_start_y = HEIGHT - button_height - button_margin_bottom

button_rects = []
for i, button_text in enumerate(buttons):
    button_rect = pygame.Rect(i * (WIDTH // 4), button_start_y, WIDTH // 4, button_height)
    button_rects.append(button_rect)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i, button_rect in enumerate(button_rects):
                if button_rect.collidepoint(event.pos):
                    # Button clicked, perform corresponding action
                    if i == 0:
                        print("Battle button clicked")
                    elif i == 1:
                        print("Craftsmanship button clicked")
                    elif i == 2:
                        print("Fellowship button clicked")
                    elif i == 3:
                        print("Journey button clicked")

    # Draw buttons
    for i, button_rect in enumerate(button_rects):
        hover = button_rect.collidepoint(pygame.mouse.get_pos())
        pressed = pygame.mouse.get_pressed()[0] and hover
        draw_button(screen, button_rect, buttons[i], BUTTON_COLOR, BUTTON_HOVER_COLOR, pressed)

    pygame.display.flip()

pygame.quit()
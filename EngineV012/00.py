import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 640, 480
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT = pygame.font.Font(None, 32)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set up the text box
text_box = pygame.Rect(100, 100, 400, 50)
active = False
text = ''

# Set up the button
button = pygame.Rect(510, 100, 100, 50)

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if text_box.collidepoint(event.pos):
                active = True
            elif button.collidepoint(event.pos):
                print(text)
            else:
                active = False
        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    print(text)
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode

    # Draw everything
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLACK, text_box, 2)
    txt_surface = FONT.render(text, True, BLACK)
    screen.blit(txt_surface, (text_box.x+5, text_box.y+5))
    pygame.draw.rect(screen, BLACK, button)
    btn_surface = FONT.render('Enter', True, BLACK)
    screen.blit(btn_surface, (button.x+10, button.y+10))

    # Update the display
    pygame.display.flip()
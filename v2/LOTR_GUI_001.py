import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Define colors (RGB)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)

# Screen dimensions
WIDTH = 1080
HEIGHT = 640

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lord of the Rings Board Game")

# Main Path parameters
Path_HEIGHT = 100
Path_WIDTH = WIDTH - 200
Path_X = 100
MAIN_Path_Y = (HEIGHT - Path_HEIGHT) // 2
NUM_STEPS_MAIN = 10
STEP_WIDTH_MAIN = Path_WIDTH // NUM_STEPS_MAIN

# Calculate the percentage of main Path width for smaller Paths
PERCENTAGE_SMALL_Path = 0.7
NUM_STEPS_SMALL_PathS = 7
STEP_WIDTH_SMALL_PathS = int(Path_WIDTH * PERCENTAGE_SMALL_Path) // NUM_STEPS_SMALL_PathS
DISTANCE_BETWEEN_PathS = 30

# Create a deck of 10 random numbers representing actions
deck_size = 10
deck = [random.randint(1, 4) for _ in range(deck_size)]

# Initialize Counter_mainPath
Counter_mainPath = 0

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

def draw_main_Path():
    pygame.draw.rect(screen, GRAY, (Path_X, MAIN_Path_Y, Path_WIDTH, Path_HEIGHT))

    for step in range(NUM_STEPS_MAIN):
        step_x = Path_X + step * STEP_WIDTH_MAIN
        step_y = MAIN_Path_Y
        color = WHITE if step + 1 <= Counter_mainPath else (0, 255, 0)
        pygame.draw.circle(screen, color, (step_x + STEP_WIDTH_MAIN // 2, step_y + Path_HEIGHT // 2), STEP_WIDTH_MAIN // 2)

def draw_smaller_Paths():
    for Path_num in range(2):
        Path_label = f"SMALL_Path_{Path_num + 1}"
        Path_y = MAIN_Path_Y + Path_HEIGHT + DISTANCE_BETWEEN_PathS + (Path_HEIGHT + DISTANCE_BETWEEN_PathS) * Path_num
        pygame.draw.rect(screen, GRAY, (Path_X, Path_y, Path_WIDTH * PERCENTAGE_SMALL_Path, Path_HEIGHT))
        for step in range(NUM_STEPS_SMALL_PathS):
            step_x = Path_X + step * STEP_WIDTH_SMALL_PathS
            pygame.draw.circle(screen, WHITE, (step_x + STEP_WIDTH_SMALL_PathS // 2, Path_y + Path_HEIGHT // 2), STEP_WIDTH_SMALL_PathS // 4)
        font = pygame.font.Font(None, 36)
        label_text = font.render(Path_label, True, WHITE)
        label_rect = label_text.get_rect(center=(WIDTH // 2, Path_y + Path_HEIGHT + DISTANCE_BETWEEN_PathS // 2))
        screen.blit(label_text, label_rect)

def draw_cards():
    card_width = 60
    card_height = 90
    card_spacing = 10
    top_cards_y = 20

    for i, number in enumerate(deck):
        card_x = (WIDTH - (card_width + card_spacing) * len(deck)) // 2 + i * (card_width + card_spacing)
        pygame.draw.rect(screen, GRAY, (card_x, top_cards_y, card_width, card_height))
        font = pygame.font.Font(None, 24)
        number_text = font.render(str(number), True, WHITE)
        number_rect = number_text.get_rect(center=(card_x + card_width // 2, top_cards_y + card_height // 2))
        screen.blit(number_text, number_rect)

# Set the background color outside the loop
screen.fill(WHITE)

# Main loop
while True:
    handle_events()

    # Increment Counter_mainPath
    Counter_mainPath = min(Counter_mainPath + 1, NUM_STEPS_MAIN)

    # Draw the game board and other elements here
    draw_main_Path()
    draw_smaller_Paths()
    draw_cards()

    pygame.display.flip()  # Update the screen

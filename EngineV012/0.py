import sys
import os

# Fix 1: Use os.path.join() to properly join paths
dir_graphics = os.path.join("gamegraphics", "odysseus_01.png")

# Fix 2: Use print() instead of display
print("Graphics path:", dir_graphics)

# Additional helpful functions:

# Check if the file exists
if os.path.exists(dir_graphics):
    print(f"✓ File found: {dir_graphics}")
else:
    print(f"❌ File not found: {dir_graphics}")

# Show the absolute path
absolute_path = os.path.abspath(dir_graphics)
print(f"Absolute path: {absolute_path}")

# Show current working directory
current_dir = os.getcwd()
print(f"Current directory: {current_dir}")

# List files in gamegraphics directory (if it exists)
graphics_folder = "gamegraphics"
if os.path.exists(graphics_folder):
    print(f"\nFiles in {graphics_folder}:")
    for file in os.listdir(graphics_folder):
        print(f"  - {file}")
else:
    print(f"\n❌ Directory '{graphics_folder}' not found")

# For pygame, you can load the image like this:
# import pygame
# pygame.init()
# try:
#     image = pygame.image.load(dir_graphics)
#     print(f"✓ Image loaded successfully: {image.get_size()}")
# except pygame.error as e:
#     print(f"❌ Could not load image: {e}")
import pygame
import os

pygame.init()

# Define colors
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# Set window size and caption
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Yellow Triangle Path")

# Load images
BACKGROUND_IMG = pygame.image.load(os.path.join('assets', 'metroMap.png')).convert()
TRIANGLE_IMG = pygame.image.load(os.path.join('assets', 'yellowTriangle.png')).convert_alpha()

# Define triangle starting position (adjust based on your map)
triangle_x = 200
triangle_y = 400

# Define movement speed
speed = 5

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get keyboard input
    keys = pygame.key.get_pressed()

    # Move triangle based on input and clamp within valid range
    triangle_x = max(0, min(triangle_x + (speed * keys[pygame.K_RIGHT] - speed * keys[pygame.K_LEFT]), WIDTH - TRIANGLE_IMG.get_width()))
    triangle_y = max(0, min(triangle_y + (speed * keys[pygame.K_DOWN] - speed * keys[pygame.K_UP]), HEIGHT - TRIANGLE_IMG.get_height()))

    # Check if triangle is on the yellow path (replace with your path detection logic)
    # This example checks a corner pixel within the triangle's bottom-left corner
    path_color = BACKGROUND_IMG.get_at((triangle_x, triangle_y + TRIANGLE_IMG.get_height() - 1))
    if path_color == YELLOW:
        # Triangle is on the path, continue moving
        pass
    else:
        # Triangle is off the path, handle accordingly (e.g., stop movement, visual feedback)
        # You can implement snapping back to the path or other corrective actions here
        pass  # Placeholder to fix the syntax error

    # Draw the game elements
    WIN.fill(BLACK)
    WIN.blit(BACKGROUND_IMG, (0, 0))
    WIN.blit(TRIANGLE_IMG, (triangle_x, triangle_y))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()

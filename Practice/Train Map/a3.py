import pygame
import os

# Initialize Pygame
pygame.init()

# Set window size
WIDTH, HEIGHT = 1280, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Yellow Triangle Path")

# Load images
TRACK_IMAGE = pygame.image.load(os.path.join('assets', 'yellowTrack.png'))
TRIANGLE_IMAGE = pygame.image.load(os.path.join('assets', 'yellowTriangle.png'))

# Define colors
YELLOW = (237, 167, 45)
BLACK = (0, 0, 0)

# Define triangle starting position
triangle_x = 100
triangle_y = 350

# Define movement speed
speed = 5

# Scale down the triangle image
TRIANGLE_SIZE = (20, 20)  # New size for the triangle image
TRIANGLE_IMAGE = pygame.transform.scale(TRIANGLE_IMAGE, TRIANGLE_SIZE)

# Main loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Check if triangle is on the yellow path
    if 0 <= triangle_x < WIDTH and 0 <= triangle_y < HEIGHT:
        pixel_color = TRACK_IMAGE.get_at((int(triangle_x), int(triangle_y)))
        if pixel_color == YELLOW:
            # Move triangle based on arrow keys
            keys = pygame.key.get_pressed()
            triangle_x += speed * (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT])
            triangle_y += speed * (keys[pygame.K_DOWN] - keys[pygame.K_UP])
    
    # Clear the screen
    WIN.fill(BLACK)
    
    # Draw the track and triangle
    WIN.blit(TRACK_IMAGE, (0, 0))
    WIN.blit(TRIANGLE_IMAGE, (triangle_x, triangle_y))

    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()

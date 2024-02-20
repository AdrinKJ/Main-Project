import pygame
import os

pygame.init()

FPS = 60

WIDTH, HEIGHT = 1280, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Train Mapping")

TRIANGLE_HEIGHT, TRIANGLE_WIDTH = 60, 60

# Load the background image
BACKGROUND = pygame.image.load(os.path.join('Assets', 'metroMap.png')).convert()

YELLOW_TRIANGLE_IMAGE = pygame.image.load(os.path.join('Assets', 'yellowTriangle.png'))
YELLOW_TRIANGLE = pygame.transform.rotate(pygame.transform.scale(YELLOW_TRIANGLE_IMAGE, (TRIANGLE_WIDTH, TRIANGLE_HEIGHT)), 90)

def draw_window():
    # Draw the background image onto the window
    WIN.blit(BACKGROUND, (0, 0))
    
    # Blit the yellow triangle onto the window
    WIN.blit(YELLOW_TRIANGLE, (100, 300))

def main():

    yellow = pygame.Rect(100, 300, TRIANGLE_WIDTH, TRIANGLE_HEIGHT)

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        draw_window()

        # Update the display
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()

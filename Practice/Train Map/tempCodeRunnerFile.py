import pygame
import sys

# Constants
WIDTH = 800
HEIGHT = 600
TRACK_COLOR = (100, 100, 100)
TRAIN_COLOR = (255, 0, 0)
TRAIN_SIZE = (50, 20)

class Train:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, *TRAIN_SIZE)
        self.speed = 3

    def move_right(self):
        self.rect.x += self.speed

    def move_left(self):
        self.rect.x -= self.speed

    def move_up(self):
        self.rect.y -= self.speed

    def move_down(self):
        self.rect.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, TRAIN_COLOR, self.rect)

class Track:
    def __init__(self):
        self.segments = [
            pygame.Rect(100, 250, 300, 20),
            pygame.Rect(400, 200, 20, 150),
            pygame.Rect(400, 200, 300, 20),
            pygame.Rect(700, 200, 20, 150),
            pygame.Rect(500, 350, 200, 20),
            pygame.Rect(500, 350, 20, 150),
            pygame.Rect(400, 500, 120, 20)
        ]

    def draw(self, screen):
        for segment in self.segments:
            pygame.draw.rect(screen, TRACK_COLOR, segment)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Train Simulator")
    clock = pygame.time.Clock()

    train = Train(100, 240)
    track = Track()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            if train.rect.right < track.segments[-1].right:
                train.move_right()
        if keys[pygame.K_LEFT]:
            if train.rect.left > track.segments[0].left:
                train.move_left()
        if keys[pygame.K_UP]:
            if train.rect.top > 0:
                train.move_up()
        if keys[pygame.K_DOWN]:
            if train.rect.bottom < HEIGHT:
                train.move_down()

        screen.fill((0, 0, 0))
        track.draw(screen)
        train.draw(screen)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()

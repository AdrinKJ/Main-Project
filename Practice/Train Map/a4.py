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
            pygame.Rect(400, 350, 120, 20),
            pygame.Rect(520, 350, 20, 150),
            pygame.Rect(520, 500, 280, 20),
            pygame.Rect(800, 350, 20, 150),
            pygame.Rect(800, 200, 100, 20),
            pygame.Rect(700, 200, 20, 150),
            pygame.Rect(700, 350, 120, 20),
            pygame.Rect(600, 350, 20, 150),
            pygame.Rect(600, 250, 100, 20),
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
            for segment in track.segments:
                if train.rect.colliderect(segment) and train.rect.right < segment.right:
                    train.move_right()
                    break
        if keys[pygame.K_LEFT]:
            for segment in track.segments:
                if train.rect.colliderect(segment) and train.rect.left > segment.left:
                    train.move_left()
                    break
        if keys[pygame.K_UP]:
            for segment in track.segments:
                if train.rect.colliderect(segment) and train.rect.top > segment.top:
                    train.move_up()
                    break
        if keys[pygame.K_DOWN]:
            for segment in track.segments:
                if train.rect.colliderect(segment) and train.rect.bottom < segment.bottom:
                    train.move_down()
                    break

        screen.fill((0, 0, 0))
        track.draw(screen)
        train.draw(screen)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
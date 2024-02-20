#Spaceship pygame
import pygame
import os
pygame.font.init() #For font
pygame.mixer.init() #For audio

WIDTH, HEIGHT = 900, 500 #of the game window
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) #Setting the game window
pygame.display.set_caption("First Game!")

#Initializing the colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

#Setting the border inside the game
BORDER = pygame.Rect(WIDTH//2 -5, 0, 10, HEIGHT) #Double slash is to make sure its rounded so as to make it integer


HEALTH_FONT = pygame.font.SysFont('verdana', 30)
WINNER_FONT = pygame.font.SysFont('verdana', 100)

FPS = 60
VEL = 5
BULLET_VEL = 8
MAX_BULLETS = 5
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 50, 40

YELLOW_HIT = pygame.USEREVENT + 1 #Created an event to inform the main function that the player has been hit
RED_HIT = pygame.USEREVENT + 2

#Loading and rendering the assets
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), -90)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE, (0, 0)) #is used to draw (or blit) one surface onto another surface
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render("Red Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Yellow Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y)) #blit() is used to draw the thing onto the screen
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    
    for bullet in  yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()

def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: #Key 'a' is pressed to move left
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width - 5.2 < BORDER.x: #Key 'd' is pressed to move right
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: #Key 'w' is pressed to move up
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 5: #Key 's' is pressed to move DOWN
        yellow.y += VEL

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width: #left arrow Key is pressed to move left
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL - 10 + red.width < WIDTH: #right  arrow Key is pressed to move right
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0: #Up arrow Key is pressed to move UP
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 5: #Down arrow Key is pressed to move DOWN
        red.y += VEL

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, PURPLE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    
    # Timer
    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_time < 5000:  # 5000 milliseconds = 5 seconds
        remaining_time = int((5000 - (pygame.time.get_ticks() - start_time)) / 1000) + 1
        timer_text = f"Returning to Game in {remaining_time}..."
        timer_rendered = HEALTH_FONT.render(timer_text, 1, PURPLE)
        WIN.fill(BLACK)  # Fill the screen with black before updating the timer text
        WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
        WIN.blit(timer_rendered, (WIDTH/2 - timer_rendered.get_width()/2, HEIGHT/2 + draw_text.get_height() + 10))
        pygame.display.update()



def main():
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)#is a rectangle (red.x = 700 and red.y = 300) (x, y) = (700, 300)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 -2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 -2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()
            
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = "YELLOW WINS"

        if yellow_health <= 0:
            winner_text = "RED WINS"
        
        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

    main()

if __name__ == "__main__":
    main()
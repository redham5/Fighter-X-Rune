import pygame
from fighter import Fighter


pygame.init()

#create game window

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((  SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fighter X Rune")

#screen framerate
clock = pygame.time.Clock()
FPS = 60

#defind colors
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

#define fighter variables
SHUGI_SIZE = 162
SHUGI_DATA = [SHUGI_SIZE]

TSUGI_SIZE = 250
TSUDI_DATA = [TSUGI_SIZE]


#load Background image
bg_image = pygame.image.load("assets/images/background/Fighter X Rune Map.png").convert_alpha()

#load characters
shagu_sheet = pygame.image.load("assets/images/heros/Shagu/Sprites/warrior.png")
tsugi_sheet = pygame.image.load("assets/images/heros/Tsugi/Sprites/wizard.png")

#cgaracters animations steps
SHAGU_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
TSUGI_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]

#function for background image
def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))

#function for health bar
def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 405, 20))
    pygame.draw.rect(screen, RED, (x, y, 400, 15))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 15))


#create two instances of fighters
fighter_1 = Fighter(200, 420, shagu_sheet, SHUGI_DATA, SHAGU_ANIMATION_STEPS)

fighter_2 = Fighter(700, 420, tsugi_sheet, TSUDI_DATA, TSUGI_ANIMATION_STEPS)


#game loop
run = True
while run:

    clock.tick(FPS)

    #draw background
    draw_bg()

    #show player health
    draw_health_bar(fighter_1.health, 20, 20)
    draw_health_bar(fighter_2.health, 580, 20)

    #move player
    fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2)


    #draw fighter
    fighter_1.draw(screen)
    fighter_2.draw(screen)


    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    #update display
    pygame.display.update()

#exit pygame
pygame.quit()
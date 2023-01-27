import pygame

class Fighter():
    def __init__(self, x, y):
        self.rect = pygame.Rect((x, y, 80, 120))
        self.vel_y = 0
        self.jump = False
    
    def move(self, screen_width, screen_height):
        SPEED = 10
        GRAVITY = 1.5
        dx = 0
        dy = 0

        #get key pressess
        key = pygame.key.get_pressed()

        #movement
        if key [pygame.K_a]:
            dx = -SPEED
        
        if key [pygame.K_d]:
            dx = SPEED

        #jump
        if key [pygame.K_w] and self.jump == False:
            self.vel_y = - 30
            self.jump = True

        #add gravity
        self.vel_y += GRAVITY
        dy += self.vel_y

        #unsure player stays in the screen
        if self.rect.left + dx < 0:
            dx = 0 - self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 30:
            self.vel_y = 0
            self.jump = False
            dy = screen_height - 30 - self.rect.bottom

        #update player positions
        self.rect.x += dx
        self.rect.y += dy

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect)

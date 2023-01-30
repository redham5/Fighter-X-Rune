import pygame

class Fighter():
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps):
        self.player = player
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = flip
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0 #0:idle #1:run #2:jump #3:attack1 #4:attack2 #5:hit #6:death
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x, y, 80, 150))
        self.vel_y = 0
        self.running = False
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        self.attack_cooldown = 0
        self.hit = False
        self.health = 10
        self.alive = True
    
    def load_images(self, sprite_sheets, animation_steps):
        #extract images from spritesheets
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheets.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list

    
    def move(self, screen_width, screen_height, surface, target):
        SPEED = 10
        GRAVITY = 1.5
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0

        #get key pressess
        key = pygame.key.get_pressed()

        #can only perfrom other actions if not currently attacking
        if self.attacking == False and self.alive == True:
            #check player 1 controls
            if self.player == 1:
                
                #movement
                if key [pygame.K_a]:
                    dx = -SPEED
                    self.running = True
                
                if key [pygame.K_d]:
                    dx = SPEED
                    self.running = True

                #jump
                if key [pygame.K_w] and self.jump == False:
                    self.vel_y = - 30
                    self.jump = True

                #attack
                if key [pygame.K_v] or key [pygame.K_g]:
                    self.attack(surface, target)

                    #attack type
                    if key [pygame.K_v]:
                        self.attack_type = 1
                    
                    if key [pygame.K_g]:
                        self.attack_type = 2
            
            
            #check player 2 controls
            if self.player == 2:
                
                #movement
                if key [pygame.K_LEFT]:
                    dx = -SPEED
                    self.running = True
                
                if key [pygame.K_RIGHT]:
                    dx = SPEED
                    self.running = True

                #jump
                if key [pygame.K_UP] and self.jump == False:
                    self.vel_y = - 30
                    self.jump = True

                #attack
                if key [pygame.K_KP1] or key [pygame.K_KP2]:
                    self.attack(surface, target)

                    #attack type
                    if key [pygame.K_KP1]:
                        self.attack_type = 1
                    
                    if key [pygame.K_KP2]:
                        self.attack_type = 2


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
        
        #ensure that players face each other
        if target.rect.centerx > self.rect.centerx and self.alive == True:
            self.flip = False
        else:
            self.flip = True

        #attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1


        #update player positions
        self.rect.x += dx
        self.rect.y += dy

        #handel animation update
    def update(self):

        #check what action player performing
        #for death
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(6) #6:death

        #for hit
        elif self.hit == True:
            self.update_action(5) #5:hit

        #for attacking
        elif self.attacking == True:
            if self.attack_type == 1:
                self.update_action(3) #3:attact1
            elif self.attack_type == 2:
                self.update_action(4) #3:attact2

        #for jumping
        elif self.jump == True:
            self.update_action(2) #2:jump

        #for running
        elif self.running == True:
            self.update_action(1) #1:run
        else:
            self.update_action(0) #0:idle

        animation_cooldown = 50
        #update image
        self.image = self.animation_list[self.action][self.frame_index]
        #check is enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        #check if animation finished
        if self.frame_index >= len(self.animation_list[self.action]):
            #check the player is dead, then end then animation
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

                #check if an attack was executed
                if self.action == 3 or self.action == 4:
                    self.attacking = False
                    self.attack_cooldown = 20
                if self.action == 5:
                    self.hit = False
                    #if player in middel of a attack, then attack is stoped
                    self.attacking = False
                    self.attack_cooldown = 20


    def attack(self, surface, target):
        if self.attack_cooldown == 0:
            self.attacking = True
            attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
        
            if attacking_rect.colliderect(target.rect):
                target.health -= 10
                target.hit = True
            pygame.draw.rect(surface, (0, 255, 0), attacking_rect)


    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            #update animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()


    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        pygame.draw.rect(surface, (255, 0, 0), self.rect)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))

















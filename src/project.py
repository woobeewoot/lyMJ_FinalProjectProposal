import pygame
import os
pygame.init()

#screen
screen_height = 600
screen_width = 1100
screen = pygame.display.set_mode((screen_width, screen_height))

running = [pygame.image.load(os.path.join("baseAssets", "DinoRun1.png")),
           pygame.image.load(os.path.join("baseAssets", "DinoRun2.png"))]
ducking = [pygame.image.load(os.path.join("baseAssets", "DinoDuck1.png")),
           pygame.image.load(os.path.join("baseAssets", "DinoDuck2.png"))]
jumping = [pygame.image.load(os.path.join("baseAssets", "DinoJump.png"))]

s_cactus = [pygame.image.load(os.path.join("baseAssets", "SmallCactus1.png"))]
l_cactus = [pygame.image.load(os.path.join("baseAssets", "LargeCactus1.png"))]

flyingMan = [pygame.image.load(os.path.join("baseAssets", "Bird1.png"))]

cloud = [pygame.image.load(os.path.join("baseAssets", "Cloud.png"))]

track = [pygame.image.load(os.path.join("baseAssets", "Track.png"))]

class StarRanger:
    x_pos = 80
    y_pos = 310
    y_pos_duck = 340
    JUMP_VEL = 8.5 #velocity

    def __init__(self):
        self.run_img = running
        self.duck_img = ducking
        self.jump_img = jumping
        #gamestart
        self.player_run = True
        self.player_duck = False
        self.player_jump = False
        
        self.step_index = 0 #animateassist
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0] #startsprite
        self.player_rect = self.image.get_rect() #hitbox
        self.player_rect.x = self.x_pos
        self.player_rect.y = self.y_pos

    def update(self, userInput):
        if self.player_run:
            self.run()
        if self.player_duck:
            self.duck()
        if self.player_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if userInput[pygame.K_UP] and not self.player_jump:
            self.player_run = False
            self.player_duck = False
            self.player_jump = True
        elif userInput[pygame.K_DOWN] and not self.player_jump:
            self.player_run = False
            self.player_duck = True
            self.player_jump = False
        elif not (self.player_jump or userInput [pygame.K_DOWN]):
            self.player_run = True
            self.player_duck = False
            self.player_jump = False

    def run(self):
        self.image = self.run_img[self.step_index//5]
        self.player_rect = self.image.get_rect()
        self.player_rect.x = self.x_pos
        self.player_rect.y = self.y_pos
        self.step_index += 1

    def duck(self):
        self.image = self.duck_img[self.step_index//5]
        self.player_rect = self.image.get_rect()
        self.player_rect.x = self.x_pos
        self.player_rect.y = self.y_pos_duck
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img[0]
        if self.player_jump:
            self.player_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < - self.JUMP_VEL:
            self.player_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, screen):
        screen.blit(self.image, (self.player_rect.x, self.player_rect.y))

def main():
    run = True
    clock = pygame.time.Clock()
    player = StarRanger()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        screen.fill((255, 255, 255))
        userInput = pygame.key.get_pressed()

        player.draw(screen)
        player.update(userInput)

        clock.tick(30)
        pygame.display.update()



main()
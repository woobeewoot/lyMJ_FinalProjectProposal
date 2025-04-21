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
           [pygame.image.load(os.path.join("baseAssets", "DinoDuck2.png"))]]
jumping = [pygame.image.load(os.path.join("baseAssets", "DinoJump.png"))]

s_cactus = [pygame.image.load(os.path.join("baseAssets", "SmallCactus1.png"))]
l_cactus = [pygame.image.load(os.path.join("baseAssets", "LargeCactus1.png"))]

bird = [pygame.image.load(os.path.join("baseAssets", "Bird1.png"))]

cloud = [pygame.image.load(os.path.join("baseAssets", "Cloud.png"))]

track = [pygame.image.load(os.path.join("baseAssets", "Track.png"))]

class StarRanger:
    x_pos = 80
    y_pos = 310

    def __init__(self):
        self.run_img = running
        self.duck_img = ducking
        self.jump_img = jumping
        #gamestart
        self.dino_run = True
        self.dino_duck = False
        self.dino_jump = False
        
        self.step_index = 0 #animateassist
        self.image = self.run_img[0] #startsprite
        self.dino_rect = self.image.get_rect() #hitbox
        self.dino_rect.x = self.x_pos
        self.dino_rect.y = self.y_pos

    def update(self, userInput):
        if self.dino_run:
            self.run()
        if self.dino_duck:
            self.duck()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if userInput[pygame.K_UP] and not self.dino_jump:
            self.dino_run = False
            self.dino_duck = False
            self.dino_jump = True
        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_run = False
            self.dino_duck = True
            self.dino_jump = False
        elif not (self.dino_jump or userInput [pygame.K_DOWN]):
            self.dino_run = True
            self.dino_suck = False
            self.dino_jump = False

    def run(self):
        pass

    def duck(self):
        pass

    def jump(self):
        pass

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
import pygame
import os
import random
import sys
pygame.init()

#screen
screen_height = 600
screen_width = 1100
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Star Ranger Run")

running = [pygame.image.load(os.path.join("baseAssets", "DinoRun1.png")),
           pygame.image.load(os.path.join("baseAssets", "DinoRun2.png"))]
ducking = [pygame.image.load(os.path.join("baseAssets", "DinoDuck1.png")),
           pygame.image.load(os.path.join("baseAssets", "DinoDuck2.png"))]
jumping = [pygame.image.load(os.path.join("baseAssets", "DinoJump.png"))]

s_cactus = [pygame.image.load(os.path.join("baseAssets", "SmallCactus1.png")),
            pygame.image.load(os.path.join("baseAssets", "SmallCactus2.png")),
            pygame.image.load(os.path.join("baseAssets", "SmallCactus3.png"))]

l_cactus = [pygame.image.load(os.path.join("baseAssets", "LargeCactus1.png")),
            pygame.image.load(os.path.join("baseAssets", "LargeCactus2.png")),
            pygame.image.load(os.path.join("baseAssets", "LargeCactus3.png"))]

flyingMan = [pygame.image.load(os.path.join("baseAssets", "Ceci.png"))]

cloud = [pygame.image.load(os.path.join("baseAssets", "Cloud.png"))]

track = [pygame.image.load(os.path.join("baseAssets", "Track.png"))]

BG = [pygame.image.load(os.path.join("baseAssets", "BG.png"))]

class StarRanger:
    x_pos = 80
    y_pos = 305
    y_pos_duck = 330
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

class Cloud:
    def __init__(self):
        self.x = screen_width + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = cloud[0]
        self.width = self.image.get_width()

    def update(self, game_speed):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = screen_width + random.randint(2500, 3000)
            self.y = random.randint (50, 100)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = screen_width

    def update(self, game_speed):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, screen):
        screen.blit(self.image[self.type], self.rect)

class SmallKaku(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0,2)
        super().__init__(image, self.type)
        self.rect.y = 325

class LargeKaku(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0,2)
        super().__init__(image, self.type)
        self.rect.y = 300

class PropellerMan(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 250
        self.index = 0

    def draw(self, screen):
        frame = (self.index // 5) % len(self.image)  #safecycle
        screen.blit(self.image[frame], self.rect)
        self.index += 1

def main():
    global game_speed, x_pos_bg, y_pos_bg, pts, obstacles
    run = True
    clock = pygame.time.Clock()
    player = StarRanger()
    cloud_int = Cloud()
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 380
    pts = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []
    death_count = 0

    def score():
        global pts, game_speed
        pts += 1
        if pts % 100 == 0:
            game_speed += 1

        text = font.render("Points: " + str(pts), True, (0, 0, 0))
        textBox = text.get_rect()
        textBox.center = (1000, 40)
        screen.blit(text, textBox)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = track[0].get_width()
        screen.blit(track[0], (x_pos_bg, y_pos_bg))
        screen.blit(track[0], (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width: #creates 'continuous' bg
            screen.blit(track[0], (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        userInput = pygame.key.get_pressed()
        
        screen.blit(BG[0], (0, 0))
        background()
        cloud_int.draw(screen)
        player.draw(screen)

        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallKaku(s_cactus))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeKaku(l_cactus))
            elif random.randint(0, 2) == 2:
                obstacles.append(PropellerMan(flyingMan))

        for obstacle in obstacles:
            obstacle.draw(screen)
            obstacle.update(game_speed)
            if player.player_rect.colliderect(obstacle.rect):
                pygame.time.delay(1000)
                death_count += 1
                menu(death_count)
        
        cloud_int.update(game_speed)
        player.update(userInput)
        score()

        clock.tick(30)
        pygame.display.update()

def menu(death_count):
    global pts
    run = True
    while run:
        screen.fill((255, 255, 255))
        font = pygame.font.Font('freesansbold.ttf', 30)

        if death_count == 0:
            text = font.render("Press any Key to Start", True, (0, 0, 0))
        elif death_count > 0:
            text = font.render("Press any Key to Restart", True, (0, 0, 0))
            score = font.render("Your Score: " + str(pts), True, (0, 0, 0))
            scoreBox = score.get_rect()
            scoreBox.center = (screen_width // 2, screen_height // 2 + 50)
            screen.blit(score, scoreBox)
        textBox = text.get_rect()
        textBox.center = (screen_width // 2, screen_height // 2 - 140)
        screen.blit(text, textBox)
        pygame.display.update()
        # quit game safely
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                sys.exit()
            #restart game
            if event.type == pygame.KEYDOWN:
                main()


menu(death_count=0)
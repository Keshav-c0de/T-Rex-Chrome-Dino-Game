import pygame
import os
import random
import sys

pygame.init()

# --- Global Constants ---
screen_height = 600
screen_width = 1100
screen = pygame.display.set_mode((screen_width, screen_height))

# Assets
running = [pygame.image.load(os.path.join("assets", "DinoRun1.png")),
           pygame.image.load(os.path.join("assets", "DinoRun2.png"))]
jumping = pygame.image.load(os.path.join("assets", "DinoJump.png"))
ducking = [pygame.image.load(os.path.join("assets", "DinoDuck1.png")),
           pygame.image.load(os.path.join("assets", "DinoDuck2.png"))]
small_cactus = [pygame.image.load(os.path.join("assets", "SmallCactus1.png")),
                pygame.image.load(os.path.join("assets", "SmallCactus2.png")),
                pygame.image.load(os.path.join("assets", "SmallCactus3.png"))]
large_cactus = [pygame.image.load(os.path.join("assets", "LargeCactus1.png")),
                pygame.image.load(os.path.join("assets", "LargeCactus2.png")),
                pygame.image.load(os.path.join("assets", "LargeCactus3.png"))]
bird = [pygame.image.load(os.path.join("assets", "Bird1.png")),
        pygame.image.load(os.path.join("assets", "Bird2.png"))]

cloud_img = pygame.image.load(os.path.join("assets", "Cloud.png"))
reset = pygame.image.load(os.path.join("assets", "Reset.png"))
track = pygame.image.load(os.path.join("assets", "Track.png"))
GameOver = pygame.image.load(os.path.join("assets", "GameOver.png"))
DinoStart = pygame.image.load(os.path.join("assets", "DinoStart.png"))

# Settings
color = (255, 255, 255)
font = pygame.font.SysFont("arial", 30)
pygame.display.set_caption("Dino Game")

class Dinosaur:
    x_pos = 80
    y_pos = 310
    y_pos_ducking = 340
    y_jump_vel = 8.5

    def __init__(self):
        self.duck_ing = ducking
        self.run_ing = running
        self.jump_ing = jumping

        self.dino_jump = False
        self.dino_run = True
        self.dino_duck = False

        self.stepIndex = 0
        self.image = self.run_ing[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.x_pos
        self.dino_rect.y = self.y_pos
        self.y_jump = self.y_jump_vel

    def update(self, userInput):
        if self.dino_duck:
            self.duck()
        if self.dino_jump:
            self.jump()
        if self.dino_run:
            self.run()

        if self.stepIndex >= 10:
            self.stepIndex = 0

        if userInput[pygame.K_UP] and not self.dino_jump:
            self.dino_jump = True
            self.dino_run = False
            self.dino_duck = False
        elif userInput[pygame.K_DOWN] and not self.dino_duck:
            self.dino_jump = False
            self.dino_run = False
            self.dino_duck = True
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_jump = False
            self.dino_run = True
            self.dino_duck = False

    def duck(self):
        self.image = self.duck_ing[self.stepIndex // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.x_pos
        self.dino_rect.y = self.y_pos_ducking
        self.stepIndex += 1

    def jump(self):
        self.image = self.jump_ing
        if self.dino_jump:
            self.dino_rect.y -= self.y_jump * 4
            self.y_jump -= 0.8
        if self.y_jump <= -self.y_jump_vel:
            self.dino_jump = False
            self.y_jump = self.y_jump_vel
            self.dino_run = True

    def run(self):
        self.image = self.run_ing[self.stepIndex // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.x_pos
        self.dino_rect.y = self.y_pos
        self.stepIndex += 1

    def draw(self, screen):
        screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

class Cloud:
    def __init__(self):
        self.x = screen_width + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = cloud_img
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = screen_width + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class Obstacles:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = screen_width

    def update(self):
        self.rect.x -= game_speed
        # Removed pop() here to avoid list errors

    def draw(self, screen):
        screen.blit(self.image[self.type], self.rect)

class LargeCactus(Obstacles):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300

class SmallCactus(Obstacles):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325

class Bird(Obstacles):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 250
        self.index = 0

    def draw(self, screen):
        if self.index >= 9:
            self.index = 0
        screen.blit(self.image[self.index // 5], self.rect)
        self.index += 1

def background():
    global x_bg, y_bg
    image_width = track.get_width()
    screen.blit(track, (x_bg, y_bg))
    screen.blit(track, (image_width + x_bg, y_bg))
    if x_bg <= -image_width:
        screen.blit(track, (image_width + x_bg, y_bg))
        x_bg = 0
    x_bg -= game_speed

def update_score():
    global game_speed, score
    score += 1
    if score % 100 == 0:
        game_speed += 1
    text = font.render("SCORE: " + str(score), True, (0, 0, 0))
    text_rect = text.get_rect(center=(1000, 40))
    screen.blit(text, text_rect)

def main():
    global game_speed, x_bg, y_bg, score, obstacles
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()
    game_speed = 14
    x_bg = 0
    y_bg = 380
    score = 0
    obstacles = []
    death_count = 0

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()

        screen.fill(color)
        
        # Draw Background
        background()
        cloud.draw(screen)
        cloud.update()
        
        # Update Player
        user_input = pygame.key.get_pressed()
        player.draw(screen)
        player.update(user_input)

        # Handle Obstacles
        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(small_cactus))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(large_cactus))
            elif random.randint(0, 2) == 2:
                obstacles.append(Bird(bird))

        for obstacle in obstacles:
            obstacle.draw(screen)
            obstacle.update()
            # Collision
            if player.dino_rect.colliderect(obstacle.rect):
                # Draw "Game Over" ONCE before freezing
                screen.blit(GameOver, GameOver.get_rect(center=(screen_width // 2, screen_height // 2 - 50)))
                screen.blit(reset, reset.get_rect(center=(screen_width // 2, screen_height // 2 + 50)))
                pygame.display.update() # Update screen so player sees it
                pygame.time.delay(2000) # Freeze for 2 seconds
                death_count += 1
                menu(death_count)
            
            # Remove obstacles that have gone off screen
            if obstacle.rect.x < -obstacle.rect.width:
                obstacles.remove(obstacle)

        update_score()
        clock.tick(30)
        pygame.display.update()

def menu(death_count):
    global score
    is_jumping = False # The Flag
    menu_dino_y = 360
    jump_vel = 8.5
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(30)
        if death_count == 0:
            screen.fill(color)
            if is_jumping:
                menu_dino_y -= jump_vel * 4
                jump_vel -= 0.8
                if jump_vel <= -8.5:
                    main()
                    return
                screen.blit(jumping, jumping.get_rect(center=(120,int(menu_dino_y))))
            else:
                screen.blit(DinoStart, DinoStart.get_rect(center=(120, int(menu_dino_y))))


        elif death_count > 0:
            score_text = font.render("YOUR SCORE:" + str(score), True, (0, 0, 0))
            score_rect = score_text.get_rect(center=(950,40))
            screen.blit(score_text, score_rect)

        pygame.display.update()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if death_count == 0:
                    is_jumping = True 
                else:
                    main()



menu(death_count=0) 
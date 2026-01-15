import pygame
import os
import random
import sys
import time

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

#Sound_effects
die = pygame.mixer.Sound(os.path.join("sound","die.mp3"))
point = pygame.mixer.Sound(os.path.join("sound","point.mp3"))
point.set_volume(0.5)
jump = pygame.mixer.Sound(os.path.join("sound","jump.mp3"))
jump.set_volume(0.5)

# Settings
bg_color = (230, 230, 230)
score_color = (100, 100, 100)
font_2 = pygame.font.SysFont("Helvetica", 30)
font_1 = pygame.font.SysFont("Helvetica", 10)
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
        self.jump_sound = jump

    def update(self):
        if self.dino_duck:
            self.duck()
        elif self.dino_jump:
            self.jump()
        else:
            self.run()

        if self.stepIndex >= 10:
            self.stepIndex = 0

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
            self.y_jump -= 0.6
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

    def update(self,clouds):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = screen_width + random.randint(1200, 3600)
            self.y = random.randint(50, 100)
        '''if self.x < -self.width:
            clouds.remove(self)'''

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class Obstacles:
    def __init__(self, image, type_):
        self.image = image
        self.type = type_
        self.rect = self.image[self.type].get_rect()
        self.rect.x = screen_width
        self.width = self.image[self.type].get_width()

    def update(self,obstacles):
        self.rect.x -= game_speed
        # Removed pop() here to avoid list errors
        if self.rect.x < -self.width:
            obstacles.remove(self)

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
        self.rect.y = random.randint(200,300)
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
    if score % 1000 == 0:
        point.play()
        game_speed += 0.1
    score_text = font_2.render("SCORE: " + str(score), True, score_color)
    score_rect = score_text.get_rect(topleft=(900,20))
    screen.blit(score_text, score_rect)

def main():
    global game_speed, x_bg, y_bg, score, obstacles
    run = True
    clock = pygame.time.Clock()
    obstacle_timer, cloud_timer = 0, 0
    spawn_delay = 1000  # Spawn every 1000 milliseconds (1 seconds)
    last_time = pygame.time.get_ticks()
    player = Dinosaur()
    clouds = Cloud()
    game_speed = 10
    x_bg = 0
    y_bg = 380
    score = 0
    obstacles = []
    clouds = []
    death_count = 0
    obs = ["smallcactus", "largecactus", "bird"]
    ratio = [45,35,20]

    while run:
        screen.fill(bg_color)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    player.dino_jump = True
                    player.dino_run = False
                    player.dino_duck = False
                    jump.play()
                    
                if event.key == pygame.K_DOWN:
                    player.dino_jump = False
                    player.dino_run = False
                    player.dino_duck = True
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    player.dino_duck = False
                    player.dino_run = True

        screen.fill(bg_color)

        player.draw(screen)            
        player.update()

        # time for showing Obstacles and clouds 
        current_time = pygame.time.get_ticks()
        delta_time = current_time - last_time
        last_time = current_time
        obstacle_timer += delta_time * (game_speed / 10)
        cloud_timer += delta_time * (game_speed / 10)
        
        # Draw Background
        background()
        if cloud_timer >= (spawn_delay+ random.randint(0, 20)):
            cloud_timer = 0
            if len(clouds) <= 5:
                clouds.append(Cloud())
        
        # drawing and removing clouds
        for cloud in clouds:
            cloud.draw(screen)
            cloud.update(clouds)
            

        # Handle Obstacles
        if obstacle_timer >= spawn_delay:
            choice = random.choices(obs,weights=ratio,k=1)[0]
            if choice == "smallcactus":
                obstacles.append(SmallCactus(small_cactus))
            elif choice == "largecactus":
                obstacles.append(LargeCactus(large_cactus))
            elif choice == "bird":
                obstacles.append(Bird(bird))
            obstacle_timer = 0

        # drawing and removing obstacles
        for obstacle in obstacles[:]:
            obstacle.draw(screen)
            obstacle.update(obstacles)
                
                # Collision
            if player.dino_rect.inflate(-20, -20).colliderect(obstacle.rect.inflate(-10, -10)):
                die.play()
                    # Draw "Game Over" ONCE before freezing
                screen.blit(GameOver, GameOver.get_rect(center=(screen_width // 2, screen_height // 2 - 50)))
                screen.blit(reset, reset.get_rect(center=(screen_width // 2, screen_height // 2 + 50)))
                score_text = font_2.render("SCORE: " + str(score), True, score_color)
                score_rect = score_text.get_rect(topleft=(900,20))
                screen.blit(score_text, score_rect)
                pygame.display.update()  # Update screen so player sees it
                pygame.time.delay(2000) # Freeze for 2 seconds
                death_count += 1
                menu(death_count)
                

        update_score()
        clock.tick(60)
        pygame.display.update()

def menu(death_count):
    global score
    is_jumping = False # The Flag
    menu_dino_y = 360
    jump_vel = 8.5
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        if death_count == 0:
            screen.fill(bg_color)
            text = ("PRESS ANY KEY TO START ;}")
            text_display = font_1.render(text, True, score_color)
            screen.blit(text_display,(950,580))
            if is_jumping:
                menu_dino_y -= jump_vel * 4
                jump_vel -= 0.6
                if jump_vel <= -8.5:
                    main()
                    return
                screen.blit(jumping, jumping.get_rect(center=(120,int(menu_dino_y))))
            else:
                screen.blit(DinoStart, DinoStart.get_rect(center=(120, int(menu_dino_y))))


        elif death_count > 0:
            text = ("PRESS ANY KEY TO START ;}")
            text_display = font_1.render(text, True, score_color)
            screen.blit(text_display,(950,580))

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
            if event.type == pygame.MOUSEBUTTONDOWN:
                if death_count == 0:
                    is_jumping = True 
                else:
                    main()


menu(death_count=0) 
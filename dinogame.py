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
cloud_img =pygame.transform.scale(cloud_img,(128,128))
reset = pygame.image.load(os.path.join("assets", "Reset.png"))
track = pygame.image.load(os.path.join("assets", "Track.png"))
GameOver = pygame.image.load(os.path.join("assets", "GameOver.png"))
DinoStart = pygame.image.load(os.path.join("assets", "DinoStart.png"))
img = [pygame.image.load(os.path.join("assets", "sun.png")),
                pygame.image.load(os.path.join("assets", "moon.png"))]

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
night_filter = pygame.Surface((screen_width, screen_height))
night_filter.fill((255, 255, 255)) 



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
    global game_speed, score, is_night
    score += 1
    if score % 1000 == 0:
        point.play()
        game_speed += 0.1
    if (score // 500) % 2 == 1:
        is_night = True
    else:
        is_night = False

def display_score(score,high_score):
    # score display
    score_text = font_2.render("SCORE: " + str(score), True, score_color)
    score_rect = score_text.get_rect(topleft=(20,900))
    screen.blit(score_text, score_rect)
    # high score display
    
    high_score_text = font_2.render("HIGH-SCORE: " + str(high_score), True, score_color)
    high_score_rect = high_score_text.get_rect(topleft=((20, 20)))
    screen.blit(high_score_text, high_score_rect)

def check_highscore(current_score):
    high_score = 0
    if os.path.exists("high_score.txt"):
        try:
            with open("high_score.txt", "r") as f:
                high_score = int(f.read())
        except:
            high_score = 0
    if current_score >= high_score:
        high_score = current_score
        with open("high_score.txt","w") as f:
            f.write(str(high_score))

    return high_score

def apply_night_mode(screen):
    current_frame = screen.copy()
    screen.fill((255, 255, 255))
    screen.blit(current_frame, (0, 0), special_flags=pygame.BLEND_SUB)

def change_color(image, new_color):
    colored_image = image.copy()
    pixels = pygame.PixelArray(colored_image)
    pixels.replace((0, 0, 0), new_color)
    del pixels
    return colored_image

def main():
    global game_speed, x_bg, y_bg, score, obstacles, is_night
    is_night = False
    score = 0
    run = True
    clock = pygame.time.Clock()
    high_score=check_highscore(score)
    obstacle_timer, cloud_timer = 0, 0
    spawn_delay = 1000  # Spawn every 1000 milliseconds (1 seconds)
    last_time = pygame.time.get_ticks()
    player = Dinosaur()
    clouds = Cloud()
    game_speed = 10
    death_count = 0
    x_bg = 0
    y_bg = 380
    obstacles = []
    clouds = []
    obs = ["smallcactus", "largecactus", "bird"]
    ratio = [45,35,20]

    while run:
        
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
                high_score=check_highscore(score)
                death_count += 1
                death_surface = screen.copy()
                menu(death_count, score, death_surface)

        if is_night:
            apply_night_mode(screen)
                
         # updating and displaying scorces       
        update_score()
        display_score(score,high_score)


        clock.tick(60)
        pygame.display.update()

def menu(death_count, score, death_surface):
    global  mode 
    mode = 0
    high_score = check_highscore(score)
    is_jumping = False # The Flag
    menu_dino_y = 360
    jump_vel = 8.5
    run = True
    clock = pygame.time.Clock()
    
    img[0] = pygame.transform.scale(img[0], (64, 64))
    img[0] =change_color(img[0],(100,100,100))
    img[1] = pygame.transform.scale(img[1], (64, 64))
    img[1] =change_color(img[1],(100,100,100))

    while run:
        clock.tick(60)
        screen.fill(bg_color)
        # starting screen display
        if death_count == 0:
            display_score(score, high_score)
            if is_jumping:
                menu_dino_y -= jump_vel * 4
                jump_vel -= 0.6
                if jump_vel <= -8.5:
                    main()
                    return
                screen.blit(jumping, jumping.get_rect(center=(120,int(menu_dino_y))))
            else:
                screen.blit(DinoStart, DinoStart.get_rect(center=(120, int(menu_dino_y))))

        # after death
        elif death_count > 0:
            # collision frame display
            if death_surface:
                screen.blit(death_surface, (0, 0))
            else:
                screen.fill(bg_color)
             # gameover and reset display
            screen.blit(GameOver, GameOver.get_rect(center=(screen_width // 2, screen_height // 2 - 50)))
            screen.blit(reset, reset.get_rect(center=(screen_width // 2, screen_height // 2 + 50)))
            score_text = font_2.render("SCORE: " + str(score), True, score_color)
            score_rect = score_text.get_rect(topleft=(900,20))
            screen.blit(score_text, score_rect)
            display_score(score, high_score)
    
        # how to start
        text = ("PRESS ANY KEY TO START ;}")
        text_display = font_1.render(text, True, score_color)
        screen.blit(text_display,(950,580))

        # Display_mode
        img_rect = img[mode].get_rect(topleft=(900, 100))
        if mode == 1:
            is_night = True
            screen.blit(img[mode], img_rect) # Draw Moon
        else:
            is_night = False
            screen.blit(img[mode], img_rect)  # Draw Sun


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
                mou_pos=pygame.mouse.get_pos()
                if img_rect.collidepoint(mou_pos):
                    mode = (mode+1)%2
                else:
                    if death_count == 0:
                        is_jumping = True 
                    else:        
                        main()
        if is_night:
            apply_night_mode(screen)
        pygame.display.update()

menu(death_count=0, score =0, death_surface=None) 
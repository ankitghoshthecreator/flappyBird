import pygame
import sys
import random

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# --- HARDCODED FILE PATHS ---
bird_path = r"E:\Flappy Ammu\bird.png"
obstacle_path = r"E:\Flappy Ammu\obs.jpg"
background_path = r"E:\Flappy Ammu\SRM-University-in-Chennai.jpg"
tap_sound_path = r"E:\Flappy Ammu\udaan.mp3"
clash_obstacle_path = r"E:\Flappy Ammu\obstacle.mp3"

# --- SCREEN SETTINGS ---
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird Clone")

# --- LOAD IMAGES ---
try:
    BIRD_IMG = pygame.image.load(bird_path)
    PIPE_IMG = pygame.image.load(obstacle_path)
    BG_IMG = pygame.image.load(background_path)
except:
    print("Error: One or more image paths are invalid.")
    pygame.quit()
    sys.exit()

# --- LOAD SOUNDS ---
try:
    tap_sound = pygame.mixer.Sound(tap_sound_path)
    clash_obstacle = pygame.mixer.Sound(clash_obstacle_path)
except:
    print("Error: One or more sound paths are invalid.")
    pygame.quit()
    sys.exit()

# --- RESIZE IMAGES ---
BIRD_IMG = pygame.transform.scale(BIRD_IMG, (90, 50))
PIPE_IMG = pygame.transform.scale(PIPE_IMG, (80, 400))
BG_IMG = pygame.transform.scale(BG_IMG, (WIDTH, HEIGHT))

# --- GAME VARIABLES ---
gravity = 0.4
bird_movement = 0
bird_rect = BIRD_IMG.get_rect(center=(150, HEIGHT // 2))

pipe_gap = 150
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1500)

font = pygame.font.SysFont("Arial", 30)
score = 0
clock = pygame.time.Clock()

# --- FUNCTIONS ---

def create_pipe():
    height = random.randint(150, 350)
    top_pipe = PIPE_IMG.get_rect(midbottom=(WIDTH + 50, height - pipe_gap // 2))
    bottom_pipe = PIPE_IMG.get_rect(midtop=(WIDTH + 50, height + pipe_gap // 2))
    return top_pipe, bottom_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return [p for p in pipes if p.right > 0]

def draw_pipes(pipes):
    for i, pipe in enumerate(pipes):
        if i % 2 == 0:
            WIN.blit(PIPE_IMG, pipe)
        else:
            flipped = pygame.transform.flip(PIPE_IMG, False, True)
            WIN.blit(flipped, pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            clash_obstacle.play()
            return False
    if bird_rect.top <= -50 or bird_rect.bottom >= HEIGHT:
        clash_obstacle.play()
        return False
    return True

def display_score(score):
    score_surface = font.render(f"Score: {score}", True, (255, 255, 255))
    WIN.blit(score_surface, (10, 10))

# --- GAME LOOP ---
running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = -8
                tap_sound.play()
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

    # BACKGROUND
    WIN.blit(BG_IMG, (0, 0))

    # BIRD MOVEMENT
    bird_movement += gravity
    bird_rect.centery += bird_movement
    WIN.blit(BIRD_IMG, bird_rect)

    # PIPE MOVEMENT
    pipe_list = move_pipes(pipe_list)
    draw_pipes(pipe_list)

    # COLLISION CHECK
    game_active = check_collision(pipe_list)
    if not game_active:
        pygame.time.wait(1000)
        print(f"Game Over! Final Score: {score}")
        pygame.quit()
        sys.exit()

    # SCORING
    for pipe in pipe_list:
        if pipe.centerx == bird_rect.centerx:
            score += 0.5  # since 2 pipes per pair
    display_score(int(score))

    pygame.display.update()

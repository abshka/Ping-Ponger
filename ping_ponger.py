import pygame
import sys
import time
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 500, 500
BG_COLOR = (173, 216, 230)
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_SIZE = 20
PADDLE_SPEED = 5
BALL_SPEED_X, BALL_SPEED_Y = 5, 5

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")

# Paddle and Ball Images
paddle1_img = pygame.image.load('racket.png')
paddle2_img = pygame.image.load('racket.png')
ball_img = pygame.image.load('tenis_ball.png')

# Classes
class Paddle:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.rect = self.img.get_rect(topleft=(x, y))

    def move(self, dy):
        if 0 <= self.y + dy <= HEIGHT - PADDLE_HEIGHT:
            self.y += dy
            self.rect.y = self.y

    def draw(self):
        screen.blit(self.img, (self.x, self.y))

class Ball:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.rect = self.img.get_rect(topleft=(x, y))
        self.speed_x = BALL_SPEED_X
        self.speed_y = BALL_SPEED_Y
        self.last_collision_time = 0

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.rect.topleft = (self.x, self.y)

    def draw(self):
        screen.blit(self.img, (self.x, self.y))

    def check_collision(self, paddle1, paddle2):
        current_time = pygame.time.get_ticks()

        if self.rect.colliderect(paddle1.rect) and self.speed_x < 0:
            if current_time - self.last_collision_time > 100:
                self.speed_x = -self.speed_x
                self.last_collision_time = current_time

        if self.rect.colliderect(paddle2.rect) and self.speed_x > 0:
            if current_time - self.last_collision_time > 100:
                self.speed_x = -self.speed_x
                self.last_collision_time = current_time

        if self.y <= 0 or self.y >= HEIGHT - BALL_SIZE:
            self.speed_y = -self.speed_y

    def reset_position(self):
        self.x, self.y = WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2
        self.rect.topleft = (self.x, self.y)
        self.speed_x = random.choice([BALL_SPEED_X, -BALL_SPEED_X])
        self.speed_y = random.choice([BALL_SPEED_Y, -BALL_SPEED_Y])

# Functions
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def reset_game():
    global paddle1, paddle2, ball, score1, score2, start_time
    paddle1 = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT//2, paddle1_img)
    paddle2 = Paddle(WIDTH - 20, HEIGHT//2 - PADDLE_HEIGHT//2, paddle2_img)
    ball = Ball(WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2, ball_img)
    score1 = 0
    score2 = 0
    start_time = time.time()

# Initialization
paddle1 = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT//2, paddle1_img)
paddle2 = Paddle(WIDTH - 20, HEIGHT//2 - PADDLE_HEIGHT//2, paddle2_img)
ball = Ball(WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2, ball_img)
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Counters
score1 = 0
score2 = 0
start_time = time.time()
paused = False
game_active = False

# Main Loop
running = True
while running:
    screen.fill(BG_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                paused = not paused
            if event.key == pygame.K_r:
                reset_game()
                game_active = True
                paused = False
        if event.type == pygame.MOUSEBUTTONDOWN and not game_active:
            mx, my = pygame.mouse.get_pos()
            if play_button.collidepoint((mx, my)):
                reset_game()
                game_active = True

    if not game_active:
        draw_text('Добро пожаловать в Ping-Ponger', font, (0, 0, 0), screen, WIDTH // 2, HEIGHT // 2 - 50)
        play_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2, 100, 50)
        pygame.draw.rect(screen, (0, 0, 0), play_button)
        draw_text('PLAY', font, (255, 255, 255), screen, WIDTH // 2, HEIGHT // 2 + 25)
    elif paused:
        draw_text('PAUSED', font, (0, 0, 0), screen, WIDTH // 2, HEIGHT // 2)
    else:
        elapsed_time = int(time.time() - start_time)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            paddle1.move(-PADDLE_SPEED)
        if keys[pygame.K_s]:
            paddle1.move(PADDLE_SPEED)
        if keys[pygame.K_UP]:
            paddle2.move(-PADDLE_SPEED)
        if keys[pygame.K_DOWN]:
            paddle2.move(PADDLE_SPEED)

        ball.move()
        ball.check_collision(paddle1, paddle2)

        if ball.x < 0:
            score2 += 1
            ball.reset_position()
        if ball.x > WIDTH:
            score1 += 1
            ball.reset_position()

        paddle1.draw()
        paddle2.draw()
        ball.draw()

        score1_text = font.render(f'Score: {score1}', True, (0, 0, 0))
        score2_text = font.render(f'Score: {score2}', True, (0, 0, 0))
        time_text = font.render(f'Time: {elapsed_time}', True, (0, 0, 0))

        screen.blit(score1_text, (50, 10))
        screen.blit(score2_text, (WIDTH - 150, 10))
        screen.blit(time_text, (WIDTH // 2.5, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

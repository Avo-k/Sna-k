# Pygame template - skeleton for new pygame project
import pygame
from pygame import K_UP, K_DOWN, K_RIGHT, K_LEFT
import random

WIDTH = 400
HEIGHT = 400
FPS = 30

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 230, 0)
BLUE = (0, 0, 255)


# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.draw.line(screen, WHITE, (200, 0), (200, 400), 2)


pygame.display.set_caption("Sna-k")
clock = pygame.time.Clock()


class Snake(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.topleft = (150, 150)

        self.speed = 150 / FPS  # speed is relative to fps in order to be independent
        self.dir = None
        self.next_dir = None  # doesnt move at the beginning of the game

    def update(self):
        if all(x % 50 == 0 for x in self.rect.topleft) and\
                {self.dir, self.next_dir} not in [{K_UP, K_DOWN}, {K_RIGHT, K_LEFT}]:
            self.dir = self.next_dir

        if self.dir == K_UP:
            self.rect.move_ip(0, -self.speed)
        elif self.dir == K_RIGHT:
            self.rect.move_ip(self.speed, 0)
        elif self.dir == K_DOWN:
            self.rect.move_ip(0, self.speed)
        elif self.dir == K_LEFT:
            self.rect.move_ip(-self.speed, 0)


class Apple(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.topleft = (250, 250)

    def update(self):
        pass


def draw_screen(s):
    s.fill(BLACK)

    for row in range(1, 8):
        pygame.draw.line(s, WHITE, (row*50, 0), (row*50, 400))
        pygame.draw.line(s, WHITE, (0, row*50), (400, row*50))


all_sprites = pygame.sprite.Group()
snake = Snake()
apple = Apple()
all_sprites.add(snake)
all_sprites.add(apple)
next_dir = None

# Game loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            snake.next_dir = event.key

    # Update
    all_sprites.update()

    # is the snake still in the screen
    for i in range(2):
        if 0 > snake.rect.topleft[i] or snake.rect.topleft[i] > WIDTH - snake.rect.width:
            running = False

    # Draw / render
    draw_screen(screen)
    all_sprites.draw(screen)


    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()

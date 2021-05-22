# Pygame template - skeleton for new pygame project
import pygame
import random

WIDTH = 400
HEIGHT = 400
FPS = 30

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Directions
N, E, W, S = (-1, 0), (0, 1), (1, 0), (0, -1)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH + 10, HEIGHT + 10))
pygame.display.set_caption("Sna-k")
clock = pygame.time.Clock()


class Cube(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)

        self.speed = 150 / FPS
        self.dir = None  # doesnt move at the beginning of the game

    def update(self, *args):

        if self.dir == pygame.K_UP:
            self.rect.move_ip(0, -self.speed)
        elif self.dir == pygame.K_RIGHT:
            self.rect.move_ip(self.speed, 0)
        elif self.dir == pygame.K_DOWN:
            self.rect.move_ip(0, self.speed)
        elif self.dir == pygame.K_LEFT:
            self.rect.move_ip(-self.speed, 0)


all_sprites = pygame.sprite.Group()
snake = Cube()
all_sprites.add(snake)
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

            snake.dir = event.key

    # Update
    all_sprites.update()

    # if snake.rect.right > WIDTH or snake.rect.left < 0 or snake.rect. < 0 or snake.rect.down > HEIGHT:
    #     running = False

    # Draw / render
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()

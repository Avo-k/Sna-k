import pygame
from pygame import K_UP, K_DOWN, K_RIGHT, K_LEFT
import random

WIDTH = 500
HEIGHT = 500
SQUARE = 50
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

pygame.display.set_caption("Sna-k")
clock = pygame.time.Clock()


class Snake(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((SQUARE, SQUARE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.topleft = (SQUARE * 3, SQUARE * 3)

        self.speed = 150 / FPS  # speed is relative to fps in order to be independent
        self.next_dir = None
        self.dir = None  # doesnt move at the beginning of the game

        self.new = 0
        first_tail = Bodypart(self)
        all_sprites.add(first_tail)
        self.body = [first_tail]

    def update(self):
        """direct the snake using keyboard inputs"""
        if all(x % SQUARE == 0 for x in self.rect.topleft) and \
                {self.dir, self.next_dir} not in [{K_UP, K_DOWN}, {K_RIGHT, K_LEFT}]:

            for b in list(reversed(self.body))[self.new:]:
                b.dir = b.parent.dir
            self.new = 0

            self.dir = self.next_dir

        for cube in [self] + self.body:
            if cube.dir == K_UP:
                cube.rect.move_ip(0, -self.speed)
            elif cube.dir == K_RIGHT:
                cube.rect.move_ip(self.speed, 0)
            elif cube.dir == K_DOWN:
                cube.rect.move_ip(0, self.speed)
            elif cube.dir == K_LEFT:
                cube.rect.move_ip(-self.speed, 0)

    def eat(self):
        new_tail = Bodypart(self.body[-1])
        self.body.append(new_tail)
        all_sprites.add(new_tail)
        self.new = 1


class Bodypart(pygame.sprite.Sprite):
    def __init__(self, parent):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((SQUARE, SQUARE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = parent.rect.center
        self.dir = None
        self.parent = parent


class Apple(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('pic/Applepix.png')
        self.image = pygame.transform.scale(self.image, (SQUARE, SQUARE))
        self.rect = self.image.get_rect()
        self.rect.topleft = random.sample(range(0, WIDTH + 1 - SQUARE, SQUARE), 2)

        self.eaten = False

    def update(self):
        if self.eaten:
            self.rect.topleft = random.sample(range(0, WIDTH + 1 - SQUARE, SQUARE), 2)
            self.eaten = False


def draw_screen(s):
    """fill the screen and draw the grid"""
    s.fill(BLACK)
    for row in range(1, 11):
        pygame.draw.line(s, WHITE, (row * SQUARE, 0), (row * SQUARE, HEIGHT))
        pygame.draw.line(s, WHITE, (0, row * SQUARE), (WIDTH, row * SQUARE))


all_sprites = pygame.sprite.Group()
snake = Snake()
apple = Apple()
all_sprites.add(apple)
all_sprites.add(snake)

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
        # check for keyboard input
        if event.type == pygame.KEYDOWN:
            snake.next_dir = event.key

    # did the snake eat the apple ?
    if snake.rect.center == apple.rect.center:
        apple.eaten = True
        snake.eat()

    # did the snake hit itself ?
    if snake.rect.collidelist([bp.rect for bp in snake.body[1:]]) != -1:
        print("You tried to eat yourself")
        running = False

    # is the snake still in the screen
    for i in range(2):
        if 0 > snake.rect.topleft[i] or snake.rect.topleft[i] > WIDTH - SQUARE:
            print("You went off screen")
            running = False

    # Update
    all_sprites.update()

    # Draw / render
    draw_screen(screen)
    all_sprites.draw(screen)

    # flip the display
    pygame.display.flip()

print(f"Score is: {len(snake.body)}")
pygame.quit()

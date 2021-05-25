import pygame
from pygame import K_UP, K_DOWN, K_RIGHT, K_LEFT


WIDTH = 500
HEIGHT = 500
SQUARE = 50
FPS = 30

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 230, 0)

gen_sq = range(0, WIDTH + 1 - SQUARE, SQUARE)
ALL_SQUARES = {(x, y) for x in gen_sq for y in gen_sq}
ALL_SPRITES = pygame.sprite.Group()


class Apple(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('pic/Applepix.png')
        self.image = pygame.transform.scale(self.image, (SQUARE, SQUARE))
        self.rect = self.image.get_rect()
        self.rect.topleft = (350, 250)


class Snake(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((SQUARE, SQUARE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.speed = 10

        # Gameplay
        self.dir = None  # doesnt move at the beginning of the game
        self.apple_pos = (350, 250)

        # Body
        self.new = 0
        first_tail = self.Body_part(self)
        ALL_SPRITES.add(first_tail)
        self.body = [first_tail]

    def update(self):
        if all(x % SQUARE == 0 for x in self.rect.topleft):
            for bp in list(reversed(self.body))[self.new:]:
                bp.dir = bp.parent.dir
            self.new = 0

            self.dir = self.think()

        for bp in [self] + self.body:
            if bp.dir == K_UP:
                bp.rect.move_ip(0, -self.speed)
            elif bp.dir == K_RIGHT:
                bp.rect.move_ip(self.speed, 0)
            elif bp.dir == K_DOWN:
                bp.rect.move_ip(0, self.speed)
            elif bp.dir == K_LEFT:
                bp.rect.move_ip(-self.speed, 0)

    def eat(self):
        """Create a new body_part"""
        new_tail = self.Body_part(self.body[-1])
        self.body.append(new_tail)
        ALL_SPRITES.add(new_tail)
        self.new = 1

    class Body_part(pygame.sprite.Sprite):
        def __init__(self, parent):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface((SQUARE, SQUARE))
            self.image.fill(GREEN)
            self.rect = self.image.get_rect()
            self.rect.center = parent.rect.center

            self.dir = None
            self.pos = self.rect.topleft
            self.parent = parent



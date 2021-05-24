import pygame
import itertools

from constants import *


class Ravenous(Snake):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        super().__init__()

    def move(self):
        vector = tuple(self.apple_pos[i] - self.rect.topleft[i] for i in range(2))
        if abs(vector[0]) > abs(vector[1]):
            if vector[0] > 0:
                return K_RIGHT
            else:
                return K_LEFT
        else:
            if vector[1] > 0:
                return K_DOWN
            else:
                return K_UP


class Patient(Snake):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        super().__init__()
        self.gps = itertools.cycle(self.hamiltonian_gps())
        self.speed = 25

    def move(self):
        return next(self.gps)

    def hamiltonian_gps(self):
        # go around the grid
        for _ in range(9):
            yield K_RIGHT
        for _ in range(9):
            yield K_DOWN
        for __ in range(9):
            yield K_LEFT
        yield K_UP

        # snake through the rest
        for _ in range(4):
            for __ in range(8):
                yield K_RIGHT
            yield K_UP
            for __ in range(8):
                yield K_LEFT
            yield K_UP


class Keyboard(Snake):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        super().__init__()
        self.next_dir = None

    def move(self):
        if {self.dir, self.next_dir} not in [{K_UP, K_DOWN}, {K_RIGHT, K_LEFT}]:
            return self.next_dir
        else:
            return self.dir

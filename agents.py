import pygame
import itertools
import random

from constants import *


class BFS(Snake):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        super().__init__()
        self.speed = 25

    def think(self):
        """Breath-first search algorithm"""

        queue = [self.rect.topleft]
        visited = []
        back_tracking = {}
        occupied = [bp.rect.topleft for bp in self.body]

        def is_square_free(pos):
            return False if any(not 0 <= coord <= WIDTH - SQUARE for coord in pos) or pos in occupied else True

        def ask_for_direction(pos):
            if pos == (self.rect.topleft[0], self.rect.topleft[1] - SQUARE):
                return K_UP
            elif pos == (self.rect.topleft[0] + SQUARE, self.rect.topleft[1]):
                return K_RIGHT
            elif pos == (self.rect.topleft[0], self.rect.topleft[1] + SQUARE):
                return K_DOWN
            elif pos == (self.rect.topleft[0] - SQUARE, self.rect.topleft[1]):
                return K_LEFT

        while queue and self.apple_pos not in visited:

            current = queue[0]
            sq_up = (current[0], current[1] - SQUARE)
            sq_right = (current[0] + SQUARE, current[1])
            sq_down = (current[0], current[1] + SQUARE)
            sq_left = (current[0] - SQUARE, current[1])

            for sq in [sq_up, sq_right, sq_down, sq_left]:
                if is_square_free(sq) and sq not in visited:
                    back_tracking[sq] = current
                    visited.append(sq)
                    queue.append(sq)

            queue.pop(0)

        if self.apple_pos in visited:
            path = []
            c = self.apple_pos
            path.append(self.apple_pos)
            while self.rect.topleft != c:
                c = back_tracking[c]
                path.append(c)

            return ask_for_direction(path[-2])

        else:
            if visited:
                return ask_for_direction(visited[0])
            else:
                return K_UP


class Ravenous(Snake):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        super().__init__()

    def think(self):
        vector = tuple(self.apple_pos[i] - self.rect.topleft[i] for i in range(2))
        if abs(vector[0]) > abs(vector[1]):
            if vector[0] >= 0 and self.dir != K_LEFT:
                return K_RIGHT
            elif vector[0] < 0 and self.dir != K_RIGHT:
                return K_LEFT
            else:
                return random.choice((K_DOWN, K_UP))
        else:
            if vector[1] >= 0 and self.dir != K_UP:
                return K_DOWN
            elif vector[1] < 0 and self.dir != K_DOWN:
                return K_UP
            else:
                return random.choice((K_LEFT, K_RIGHT))


class Patient(Snake):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        super().__init__()
        self.gps = itertools.cycle(self.hamiltonian_gps())
        self.speed = 25

    def think(self):
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

    def think(self):
        if {self.dir, self.next_dir} not in [{K_UP, K_DOWN}, {K_RIGHT, K_LEFT}]:
            return self.next_dir
        else:
            return self.dir

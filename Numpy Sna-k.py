import numpy as np
import time


N, E, W, S = (-1, 0), (0, 1), (1, 0), (0, -1)


class Grid:
    def __init__(self):
        self.board = np.zeros((8, 8))

    def update(self, *args):
        self.board = np.zeros((8, 8))
        for obj in args:
            obj.update()
            self.board[obj.pos] = int(obj)

    def __str__(self):
        s = ""
        for line in self.board:
            for square in line:
                if not square:
                    s += ". "
                elif square == 1:
                    s += "S "
                else:
                    s += "F "
            s += "\n"
        return s


class Apple:
    def __init__(self):
        self.pos = tuple(np.random.randint(0, 8, size=2))

    def __int__(self):
        return 2

    def update(self):
        pass


class Snake:
    def __init__(self):
        self.pos = (3, 3)
        self.dir = N

    def __int__(self):
        return 1

    def update(self):
        self.pos = tuple(np.array(self.pos) + np.array(self.dir))


grid = Grid()
a = Apple()
s = Snake()

while True:

    grid.update(a, s)
    print(grid)

    time.sleep(1)

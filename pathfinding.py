import random

MOVEMENTS = {"Down": (0, 1),
             "Up": (0, -1),
             "Left": (-1, 0),
             "Right": (1, 0),
             "Stay": (0, 0)
             }


class Point(object):
    '''Creates a point on a coordinate plane with values x and y.'''

    def __init__(self, x, y):
        '''Defines x and y variables'''
        self.x = x
        self.y = y

    def __str__(self):
        return f'({self.x},{self.y})'

    @property
    def getx(self):
        return self.x

    @property
    def gety(self):
        return self.y

    def equals(self, p):
        return (p.x == self.x and p.y == self.y)

    def move(self, dx, dy):
        '''Determines where x and y move'''
        self.x += dx
        self.y += dy


class PathFind(object):

    def __init__(self, grid, start, end):
        self.grid = grid
        self.start = start
        self.end = end

        self.grid[start.x][start.y] = 0
        self.grid[end.x][end.y] = 0

        # тут может map использовать и лямбды?
        for a in self.grid:
            # assert isinstance(a, object) - # что это?
            for b in a:
                if b != 0:
                    b = -1

    def __ingrid(self, x, y):
        return 0 <= x < len(self.grid) and 0 <= y < len(self.grid[0])

    # def __pf_step(self, i, j, level):
    #     # print(level, i,j)
    #     k = self.grid[i][j]
    #     if (k != 0) and (k <= level): return
    #
    #     self.grid[i][j] = level
    #     for x, y in MOVEMENTS.values():
    #         # x, y = movm
    #         x += i
    #         y += j
    #         if self.__ingrid(x, y):
    #             self.__pf_step(x, y, level + 1)
    #
    #
    # def findpath(self) -> str:
    #     self.__pf_step(self.end.x, self.end.y, 1)
    #
    #     if self.grid[self.start.x][self.start.y] == 0: return "Stay"
    #
    #     for m in MOVEMENTS:
    #         x, y = MOVEMENTS[m]
    #         x += self.start.x
    #         y += self.start.y
    #         if self.__ingrid(x, y):
    #             if self.grid[x][y] == self.grid[self.start.x][self.start.y] - 1:
    #                 return m

    def __pf_wave(self):
        level = 1
        self.grid[self.end.x][self.end.y] = level
        wave = ((self.end.x, self.end.y),)
        while len(wave) > 0:
            level += 1
            wave_new = []
            for i, j in wave:
                for x, y in MOVEMENTS.values():  # sorted(MOVEMENTS.values(),reverse=(random.randint(1,10)>5)):
                    # x, y = movm
                    x += i
                    y += j
                    if self.__ingrid(x, y):
                        if self.grid[x][y] == 0:
                            self.grid[x][y] = level
                            wave_new.append((x, y))
                            if x == self.start.x and y == self.start.y:
                                # print(level)
                                return
            wave = tuple(wave_new)
        print(level)

    def findpath_wave(self) -> str:
        self.__pf_wave()

        if self.grid[self.start.x][self.start.y] == 0: return "Stay"

        # for m in MOVEMENTS:
        for m in sorted(MOVEMENTS, reverse=(random.randint(1, 10) > 5)):
            x, y = MOVEMENTS[m]
            x += self.start.x
            y += self.start.y
            if self.__ingrid(x, y):
                if self.grid[x][y] == self.grid[self.start.x][self.start.y] - 1:
                    return m

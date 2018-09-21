# https://github.com/brean/python-pathfinding/tree/master/pathfinding


from tkinter import *
# from pathfinding import MOVEMENTS
from pathfinding import Point
from pathfinding import PathFind
# from copy import deepcopy
# from enum import Enum
import time
import random
from threading import Thread

WIDHT = 60
HEIGHT = 40
# WIDHT = 15
# HEIGHT = 10
DRAW_SCALE = 15

MOVEMENTS = {"Down": (0, 1),
             "Up": (0, -1),
             "Left": (-1, 0),
             "Right": (1, 0),
             "Stay": (0, 0)
             }


# class MyThread(Thread):
#     def __init__(self, name):
#         Thread.__init__(self)
#         self.name = name
#
#     def __str__(self):
#         return (f'Thread: {self.name}')
#
#     def run(self):
#         time.sleep(3)
#         while True:
#         """Запуск потока"""
#         amount = random.randint(3, 15)
#         time.sleep(amount)
#         msg = "%s is running" % self.name
#         print(msg)


class Snake(object):
    """класс змейки"""

    def __init__(self, x, y, rgb=(250, 0, 0)):
        self.segments = [Point(x, y)]
        self.rgb = rgb

    # @property
    # def segments(self) -> list:
    #     return self.segments

    @property
    def head(self) -> Point:
        return self.segments[-1]

    @property
    def body(self) -> list:
        return self.segments

    def __move_by_direction(self, p, move_dir_str) -> Point:
        dx = 0
        dy = 0
        if move_dir_str in MOVEMENTS:
            dx, dy = MOVEMENTS[move_dir_str]
        return Point(p.x + dx, p.y + dy)

    def draw(self):
        for i, p in enumerate(self.segments, 1):
            d = 1.0 - 0.3 * float(i) / float(len(self.segments))

            r = int(d * float(self.rgb[0]))
            g = int(d * float(self.rgb[1]))
            b = int(d * float(self.rgb[2]))
            draw_snake_rect(p, RGBToHTMLColor((r, g, b)))

    def move(self, move_dir_str) -> int:
        """move_result_int
            0 ok
            -1 unknown move_dir_str
            1 самопересечение
        """
        p_new = self.__move_by_direction(self.segments[-1], move_dir_str)
        if p_new.equals(self.segments[-1]):
            print(f'unknown snake direction{move_dir_str}')
            return -1
        for p in self.segments:
            if p_new.equals(p):
                print(f'есть пересечения: {p_new}')
                return 1
        self.segments.append(p_new)

        # едааа
        if not eat_point.equals(self.segments[-1]):
            draw_snake_rect(self.segments[0], 'lightgray')
            del self.segments[0]
        return 0

    def tail_kill(self):
        if len(self.segments) > 1:
            draw_snake_rect(self.segments[0], 'lightgray')
            del self.segments[0]


def get_direction(start, end) -> str:
    t = (end.x - start.x, end.y - start.y)
    # тут как-то переделать
    if t in MOVEMENTS.values():
        for s in MOVEMENTS.keys():
            if MOVEMENTS[s] == t:
                return s
    return "Stay"


def draw_snake_rect(p, color):
    # root.geometry ('800x600+10+100')
    # canv.create_line(10, 10, 100, 100, width=5)
    canv.create_rectangle(p.x * DRAW_SCALE, p.y * DRAW_SCALE, (p.x + 1) * DRAW_SCALE, (p.y + 1) * DRAW_SCALE,
                          fill=color, outline='lightgray')


def draw_canv():
    draw_snake_rect(eat_point, "white")
    for sn in snakes: sn.draw()


def key_pressed(event):
    global kb_key
    if event.keysym in MOVEMENTS:
        kb_key = event.keysym


# def main():
#     global eat_point
#     for sn in snakes:
#         sn.move(kb_key)
#         if sn.head.equals(eat_point):
#             eat_point = Point(eat_point.x + 1, eat_point.y + 1)
#     draw_canv()
#     root.after(500, main)

def main():
    global eat_point
    time.sleep(0.5)
    while True:
        for sn in snakes:
            pf = PathFind(get_find_path_grid(), sn.head, eat_point)
            pathfound = pf.findpath_wave()
            # pathfound = pf.findpath()
            if pathfound == 'Stay':
                sn.tail_kill()
            else:
                sn.move(pathfound)
                if sn.head.equals(eat_point):
                    # eat_point = Point(eat_point.x + 1, eat_point.y + 1)
                    set_eat_point()
                draw_canv()
        # time.sleep(1)
        # root.after(1, main)


def set_eat_point():
    global eat_point

    x = random.randint(0, WIDHT - 1)
    y = random.randint(0, HEIGHT - 1)

    grid = get_find_path_grid()
    while grid[x][y] != 0:
        x = random.randint(0, WIDHT - 1)
        y = random.randint(0, HEIGHT - 1)
    eat_point = Point(x, y)


def RGBToHTMLColor(rgb_tuple):
    """ convert an (R, G, B) tuple to #RRGGBB """
    hexcolor = '#%02x%02x%02x' % rgb_tuple
    # that's it! '%02x' means zero-padded, 2-digit hex values
    return hexcolor


def get_find_path_grid():
    l = []
    for j in range(HEIGHT): l.append(0)

    grid = []
    for i in range(WIDHT): grid.append(l.copy())
    # print(f'{len(grid_path_finding)} {len(grid_path_finding[0])} {grid_path_finding[0][0]}')

    for sn in snakes:
        for p in sn.body:
            grid[p.x][p.y] = -1

    return grid


"""start point"""
snakes = [Snake(0, 0, (250, 0, 0)),
          Snake(1, 0, (0, 0, 250)),
          Snake(2, 0, (0, 250, 250))
          ]
eat_point = Point(8, 8)
kb_key = "Right"

root = Tk()
canv = Canvas(root, width=WIDHT * DRAW_SCALE, height=HEIGHT * DRAW_SCALE, bg='lightgray')  # '#005500'
canv.grid()
draw_canv()

# canv.focus_set()
# canv.bind('<KeyPress>', key_pressed)

t = Thread(target=main)  # , args=(15,))
t.daemon = True
t.start()

# main()
root.mainloop()

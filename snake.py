import math
import random
import tkinter as tk
from tkinter import messagebox
import pygame


class Cube(object):
    rows = 20
    w = 500  # width

    def __init__(self, start, dirnx=1, dirny=0, color=(255, 0, 0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows   # Width/Height of each cube
        i = self.pos[0]  # Current row
        j = self.pos[1]  # Current Column

        pygame.draw.rect(surface, self.color, (i * dis +
                                               1, j * dis + 1, dis - 2, dis - 2))

        if eyes:
            center = dis // 2
            radius = 3
            circleMiddle1 = (i * dis + center - radius, j * dis + 8)
            circleMiddle2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle1, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)


class Snake(object):

    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = Cube(pos)  # The head will be the front of the snake
        # We will add head (which is a cube object) to our body list
        self.body.append(self.head)
        # These will represent the direction our snake is moving
        self.dirnx = 0  # direction for X
        self.dirny = 1  # direction for Y

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()
            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                if keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                if keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                if keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):
            p = c.pos[:]

            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])

                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                if c.dirnx == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows-1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows-1:
                    c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows-1:
                    c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows-1)
                else:
                    c.move(c.dirnx, c.dirny)

    def reset(self, pos):
        self.head = Cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        # We need to know which side of the snake to add the cube to.
        # So we check what direction we are currently moving in to determine,
        # if we need to add the cube to the left, right, above or below.

        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] + 1)))

        # We then set the cubes direction to the direction of the snake.
        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)


def drawGrid(w, rows, surface):
    sizeBetween = w // rows  # Gives us the distance between the lines
    x = 0  # Keeps track of the current x
    y = 0  # Keeps track of the current y

    # We will draw one vertical and one horizontal line each loop
    for i in range(rows):
        x = x + sizeBetween
        y = y + sizeBetween

        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))


def redrawWindow(surface):
    global rows, width, s, snack

    surface.fill((0, 0, 0))  # Fills the screen with black
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width, rows, surface)  # Will draw our grid lines
    pygame.display.update()  # Updates the screen


def randomSnack(row, item):
    position = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)

        if len(list(filter(lambda z: z.pos == (x, y), position))) > 0:
            continue
        else:
            break
    return (x, y)


def message(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)

    try:
        root.destroy()
    except:
        pass


def main():
    global width, rows, s, snack

    width = 500  # Width of our screen
    rows = 20  # Amount of rows
    win = pygame.display.set_mode((width, width))  # Creates our screen object
    # Creates a snake object which we will code later
    s = Snake((255, 0, 0), (10, 10))
    snack = Cube(randomSnack(rows, s), color=(0, 255, 0))

    flag = True
    clock = pygame.time.Clock()  # creating a clock object

    # STARTING MAIN LOOP
    while flag:
        pygame.time.delay(100)
        # This will delay the game so it doesn't run too quickly

        clock.tick(15)    # Will ensure our game runs at 10 FPS
        s.move()

        if s.body[0].pos == snack.pos:  # Checks if the head collides with the snack
            s.addCube()  # Adds a new cube to the snake
            # creates a new snack object
            snack = Cube(randomSnack(rows, s), color=(0, 255, 0))

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z: z.pos, s.body[x + 1:])):
                # This will check if any of the positions in our body list overlap
                print("Score: ", len(s.body))
                message("Game Over", "You Lost\nPlay Again")
                s.reset((10, 10))
                break
        redrawWindow(win)  # Will ensure our game runs at 10 FPS


main()

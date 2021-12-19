import random
import os
import time
import keyboard

from config import *


class Gen:

    def __init__(self):
        self.lenX = LEN_X
        self.lenY = LEN_Y
        self.direction = random.choice(['up', 'down', 'right', 'left'])
        self.parts = [[self.lenX // 2, self.lenY // 2 + i] for i in range(2)]
        self.target = [random.choice([x for x in range(self.lenX) if x != self.parts[0][0]]), random.choice([y for y in range(self.lenY) if y != self.parts[0][1]])]


    def grow(self):
        if self.parts[0] == self.target:
            self.parts.append(self.tail)
            land = list()
            for y in range(self.lenY):
                for x in range(self.lenX):
                    if self.field[y][x] == ' ':
                        land.append([x, y])
            self.target = random.choice(land)


    def draw(self):
        self.field = [[' ' for j in range(self.lenX)] for i in range(self.lenY)]
        for part in self.parts[1:]:
            self.field[part[1]][part[0]] = TAIL_SYMBOL
        self.field[self.target[1]][self.target[0]] = f'\033[0;32m{TARGET_SYMBOL}\033[0;0m'
        self.field[self.parts[0][1]][self.parts[0][0]] = HEAD_SYMBOL
        os.system('clear')
        #print('\n' * 20)
        print(' ' * (self.lenX // 2 - 3) + "SCORE: " + str(len(self.parts) - 2))
        print('_' * (self.lenX + 2))
        for line in self.field:
            print('|' + ''.join(line) + '|')
        print('‾' * (self.lenX + 2))


    def move(self):
        self.tail = self.parts[-1].copy()
        neck = self.parts[1].copy()
        for i in range(len(self.parts) - 1, 0, -1):
            self.parts[i] = self.parts[i - 1].copy()

        if self.direction == 'up':
            if (self.parts[0][1] - 1) % self.lenY != neck[1]:
                self.parts[0][1] = (self.parts[0][1] - 1) % self.lenY
            else:
                self.parts[0][1] = (self.parts[0][1] + 1) % self.lenY

        elif self.direction == 'down':
            if (self.parts[0][1] + 1) % self.lenY != neck[1]:
                self.parts[0][1] = (self.parts[0][1] + 1) % self.lenY
            else:
                self.parts[0][1] = (self.parts[0][1] - 1) % self.lenY

        elif self.direction == 'right':
            if (self.parts[0][0] + 1) % self.lenX != neck[0]:
                self.parts[0][0] = (self.parts[0][0] + 1) % self.lenX
            else:
                self.parts[0][0] = (self.parts[0][0] - 1) % self.lenX

        elif self.direction == 'left':
            if (self.parts[0][0] - 1) % self.lenX != neck[0]:
                self.parts[0][0] = (self.parts[0][0] - 1) % self.lenX
            else:
                self.parts[0][0] = (self.parts[0][0] + 1) % self.lenX


    def change_direction(self, key):
        if key.name in ('up', 'down', 'right', 'left'):
            self.direction = key.name


    def check(self):
        for part in self.parts[1:]:
            if self.parts[0] == part:
                print(' ' * (self.lenX // 2 - 4) + "\033[1;31mGAME OVER!\033[0;0m")
                exit()


    def play(self):
        keyboard.on_press(self.change_direction)
        while True:
            self.draw()
            self.move()
            self.grow()
            self.check()
            time.sleep(0.45 - (SPEED * 0.04))


if __name__ == "__main__":
    game = Gen()
    game.play()

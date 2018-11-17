
import pygame
from pygame.locals import *
import random
from copy import deepcopy
import unittest


class GameOfLife:

    def __init__(self, width=640, height=480, cell_size=10, speed=10):
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_grid(self):
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.width, y))

    def run(self):
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        # Создание списка клеток
        self.clist = CellList(self.cell_height, self.cell_width, True)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_grid()

            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            self.draw_cell_list(self.clist)
            self.clist = self.clist.update()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def draw_cell_list(self, clist) -> None:

        for cell in clist:

            color_cell = pygame.Color('white')

            if cell.is_alive():
                color_cell = pygame.Color('green')

            x0 = cell.col * self.cell_size
            y0 = cell.row * self.cell_size
            x = self.cell_size
            y = self.cell_size

            rect = Rect(x0 + 1, y0 + 1, x - 1, y - 1)
            pygame.draw.rect(self.screen, color_cell, rect)


class Cell:

    def __init__(self, row, col, state=False):
        self.row = row
        self.col = col
        self.state = state

    def is_alive(self):
        return self.state


class CellList:

    def __init__(self, nrows, ncols, randomize=False, openFile=False,
                 clist=[]):
        self.nrows = nrows
        self.ncols = ncols

        if openFile:
            self.clist = clist
            return

        self.clist = [[Cell] * ncols for i in range(nrows)]

        for i in range(nrows):
            for j in range(ncols):
                self.clist[i][j] = Cell(i, j, False)

        if randomize:
            for i in range(nrows):
                for j in range(ncols):
                    self.clist[i][j].state = random.randint(0, 1)

    def get_neighbours(self, cell: Cell) -> list:
        neighbours = []
        row = cell.row
        col = cell.col
        nrow = [-1, -1, -1, 0, 0, 1, 1, 1]
        ncol = [-1, 0, 1, -1, 1, -1, 0, 1]
        for i in range(8):
            if row + nrow[i] >= 0 and col + ncol[i] >= 0:
                if row + nrow[i] < self.nrows and col + ncol[i] < self.ncols:
                    neighbours.append(self.clist[row + nrow[i]][col + ncol[i]])
        return neighbours

    def update(self):
        new_clist = deepcopy(self.clist)
        for row in range(self.nrows):
            for col in range(self.ncols):
                neighbours = self.get_neighbours(self.clist[row][col])
                s = 0
                for i in neighbours:
                    if i.is_alive() == 1:
                        s += 1
                if not self.clist[row][col].is_alive():
                    if s == 3:
                        new_clist[row][col].state = True
                else:
                    if s == 3 or s == 2:
                        new_clist[row][col].state = True
                    else:
                        new_clist[row][col].state = False

        self.clist = new_clist
        return self

    def __iter__(self):
        self.index_row = 0
        self.index_col = 0
        return self

    def __next__(self):
        if self.index_row < self.nrows:
            cell = self.clist[self.index_row][self.index_col]
            self.index_col += 1
            if self.index_col == self.ncols:
                self.index_col = 0
                self.index_row += 1
            return cell
        else:
            raise StopIteration

    def __str__(self):
        clist = [[0] * self.ncols for i in range(self.nrows)]

        for row in range(self.nrows):
            for col in range(self.ncols):
                clist[row][col] = int(self.clist[row][col].is_alive())

        return str(clist)

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            clist = []
            i = 0
            k = 0
            ncol = 0
            for line in file:
                row = []
                for j in line:
                    if j == "0":
                        row.append(Cell(i, k, False))
                    else:
                        row.append(Cell(i, k, True))
                    ncol = k
                    k += 1

                k = 0
                i += 1
                clist.append(row)

            nrow = i
        return CellList(nrow, ncol, openFile=True, clist=clist)


if __name__ == '__main__':
    game = GameOfLife(300, 300, 20)
    game.run()
import pygame  # type: ignore
from pygame.locals import *  # type: ignore
import random
from typing import Tuple


class GameOfLife:

    def __init__(self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10):
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

    def draw_grid(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.width, y))

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        # Создание списка клеток
        self.clist = self.cell_list()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:  # type: ignore
                    running = False
            self.draw_grid()

            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            self.draw_cell_list(self.clist)
            self.clist = self.update_cell_list(self.clist)

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def cell_list(self, randomize: bool = True) -> list:
        """ Создание списка клеток.
        :param randomize: Если True, то создается список клеток, где
        каждая клетка равновероятно может быть живой (1) или мертвой (0).
        :return: Список клеток, представленный в виде матрицы
        """
        self.clist = []
        if randomize:
            self.clist = [[random.randint(0, 1) for i in range(
                int(self.cell_width))] for j in range(int(self.cell_height))]
        else:
            self.clist = [[0 for i in range(int(self.cell_width))]
                          for j in range(int(self.cell_height))]
        return self.clist


    def draw_cell_list(self, clist: list) -> None:
        """ Отображение списка клеток
        :param rects: Список клеток для отрисовки,
        представленный в виде матрицы
        """
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                color_cell = pygame.Color('white')

                if clist[i][j] == 1:
                    color_cell = pygame.Color('green')

                rect = Rect(i * self.cell_size + 1, j * self.cell_size + 1, self.cell_height,
                            self.cell_width)  # type:ignore
               
                pygame.draw.rect(self.screen, color_cell, rect)

    def get_neighbours(self, cell: tuple) -> list:
        """ Вернуть список соседей для указанной ячейки
        :param cell: Позиция ячейки в сетке, задается кортежем вида (row, col)
        :return: Одномерный список ячеек, смежных к ячейке cell
        """

        neighbours = []
        positions = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                     (0, 1), (1, 0), (1, -1), (1, 1)]
        for r, c in positions:
            if 0 <= cell[0] + r < self.cell_height and 0 <= cell[1] + c < self.cell_width:
                neighbours.append(self.clist[cell[0] + r][cell[1] + c])
        return neighbours

    def update_cell_list(self, cell_list: list) -> list:
        """ Выполнить один шаг игры.
        Обновление всех ячеек происходит одновременно. Функция возвращает
        новое игровое поле.
        :param cell_list: Игровое поле, представленное в виде матрицы
        :return: Обновленное игровое поле
        """
        new_clist: list = []
        new_clist = [[0] * self.cell_width for i in range(self.cell_height)]
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                cell = i, j
                neighbours = self.get_neighbours(cell)
                s = 0
                for neighbour in neighbours:
                    if neighbour == 1:
                        s += 1

                if cell_list[i][j] == 0:
                    if s == 3:
                        new_clist[i][j] = 1

                if cell_list[i][j] == 1:
                    if s == 3 or s == 2:
                        new_clist[i][j] = 1
                    else:
                        new_clist[i][j] = 0
        self.clist = new_clist

        return self.clist


if __name__ == '__main__':
    game = GameOfLife(300, 300, 20)
    game.run()
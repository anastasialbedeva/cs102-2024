import random
import typing as tp
from typing import Any, List, Tuple

import pygame
from pygame.locals import *

pygame.init()

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10) -> None:
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

        self.grid: Grid = []

    def draw_lines(self) -> None:
        """Отрисовать сетку"""
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        """Запустить игру"""
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        # Создание списка клеток
        self.create_grid(randomize=True)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            self.draw_lines()

            self.get_next_generation()
            self.draw_grid()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.
        """
        grid: Grid = []
        height = self.cell_height
        width = self.cell_width

        for i in range(height):
            row: Cells = []
            for j in range(width):
                if randomize:
                    cell = random.randint(0, 1)
                else:
                    cell = 0
                row.append(cell)
            self.grid.append(row)

        return self.grid

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        if self.grid is None:
            return

        for y in range(self.cell_height):
            for x in range(self.cell_width):
                if self.grid[y][x] == 1:
                    color = pygame.Color("green")
                else:
                    color = pygame.Color("white")
                pygame.draw.rect(
                    self.screen, color, (x * self.cell_size, y * self.cell_size), self.cell_size, self.cell_size
                )

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток, в котором каждая позиция – 0 или 1.
        """
        row, col = cell
        values = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                new_row, new_col = row + dx, col + dy
                if 0 <= new_row < self.cell_height and 0 <= new_col < self.cell_width:
                    values.append(self.grid[new_row][new_col])
        return values

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.
        """
        if self.grid is None:
            return self.create_grid()

        new_grid = []
        for i in range(self.cell_height):
            new_row = []
            for j in range(self.cell_width):
                # Get number of live neighbors
                neighbours = self.get_neighbours((i, j))
                live_neighbors = sum(neighbours)
                # Apply Conway's Game of Life rules
                if self.grid[i][j] == 1:
                    if live_neighbors in [2, 3]:
                        new_row.append(1)
                    else:
                        new_row.append(0)
                else:
                    if live_neighbors == 3:
                        new_row.append(1)
                    else:
                        new_row.append(0)
            new_grid.append(new_row)
        self.grid = new_grid
        return self.grid


if __name__ == "__main__":
    game = GameOfLife(320, 240, 20)
    game.run()

import pathlib
import random
import typing as tp

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.
        """
        grid = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                if randomize:
                    cell = random.randint(0, 1)
                else:
                    cell = 0
                row.append(cell)
            grid.append(row)
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        """Return list of neighbor cell values"""
        x, y = cell
        neighbor_values = []
        directions = [(-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (0, -1), (1, -1)]
        for dx, dy in directions:
            new_x = x + dx
            new_y = y + dy
            if 0 <= new_x < self.rows and 0 <= new_y < self.cols:
                neighbor_values.append(self.curr_generation[new_x][new_y])
        return neighbor_values

    def get_next_generation(self) -> Grid:
        new_grid = []
        for x in range(self.rows):
            new_row = []
            for y in range(self.cols):
                cell_state = self.curr_generation[x][y]
                neighbours = self.get_neighbours((x, y))
                live_neighbours = sum(self.get_neighbours((x, y)))
                if cell_state == 1 and live_neighbours in [2, 3]:
                    new_row.append(1)
                elif cell_state == 0 and live_neighbours == 3:
                    new_row.append(1)
                else:
                    new_row.append(0)
            new_grid.append(new_row)
        return new_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.max_generations is not None:
            return self.generations >= self.max_generations
        return False

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.curr_generation != self.prev_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        with open(filename, "r") as f:
            lines = f.readlines()
        grid = [[int(cell) for cell in line.strip()] for line in lines]
        size = (len(grid), len(grid[0]))
        game = GameOfLife(size, randomize=False)
        game.curr_generation = grid
        return game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename, "w") as f:
            for row in self.curr_generation:
                f.write("".join(map(str, row)) + "\n")

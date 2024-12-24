import curses

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)
        self.max_rows = life.rows + 2
        self.max_cols = life.cols + 2

    def draw_borders(self, screen) -> None:
        """Draw border frame."""
        try:
            screen.addch(0, 0, curses.ACS_ULCORNER)
            screen.addch(0, self.max_cols - 1, curses.ACS_URCORNER)
            screen.addch(self.max_rows - 1, 0, curses.ACS_LLCORNER)  # Fixed missing coordinate
            screen.addch(self.max_rows - 1, self.max_cols - 1, curses.ACS_LRCORNER)

            for i in range(1, self.max_cols - 1):
                screen.addch(0, i, curses.ACS_HLINE)
                screen.addch(self.max_rows - 1, i, curses.ACS_HLINE)

            for i in range(1, self.max_rows - 1):
                screen.addch(i, 0, curses.ACS_VLINE)
                screen.addch(i, self.max_cols - 1, curses.ACS_VLINE)
        except curses.error:
            pass

    def draw_grid(self, screen) -> None:
        """Отобразить состояние клеток."""
        for row in range(self.life.rows):
            for col in range(self.life.cols):
                if self.life.curr_generation[row][col] == 1:
                    char = "1"
                else:
                    char = "0"
                screen.addch(row + 1, col + 1, char)

    def run(self) -> None:
        curses.resize_term(self.max_rows + 1, self.max_cols + 1)
        screen = curses.initscr()
        # Get actual terminal size
        max_y, max_x = screen.getmaxyx()

        # Ensure window is large enough
        if max_y < self.max_rows or max_x < self.max_cols:
            curses.endwin()
            print(f"Terminal too small. Needs {self.max_rows}x{self.max_cols}, got {max_y}x{max_x}")
            return

        curses.curs_set(0)
        screen.nodelay(True)
        screen.keypad(True)

        try:
            while True:
                screen.clear()
                self.draw_borders(screen)
                self.draw_grid(screen)
                screen.refresh()

                key = screen.getch()
                if key == ord("q"):  # Нажатие 'q' завершает игру
                    break

                # Проверяем, есть ли живые клетки
                no_live_cells = all(
                    cell == 0  # Клетка мертва
                    for row in self.life.curr_generation  # Для каждой строки
                    for cell in row  # Для каждой клетки в строке
                )

                if no_live_cells or self.life.is_max_generations_exceeded:
                    break

                self.life.step()
                curses.napms(100)  # Задержка в миллисекундах
        finally:
            curses.endwin()


if __name__ == "__main__":
    game = GameOfLife(size=(10, 20))
    console = Console(game)
    console.run()

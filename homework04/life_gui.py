""" Conway's Game of Life """

import pygame
from life import GameOfLife
from pygame.locals import K_SPACE, KEYDOWN, MOUSEBUTTONDOWN, QUIT
from ui import UI


class GUI(UI):
    """Grafic user implementation for Conways Game of Life"""

    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        """Initialize GUI parameters"""

        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed
        self.width = self.life.cols * self.cell_size
        self.height = self.life.rows * self.cell_size
        self.screen = pygame.display.set_mode((self.width, self.height))

    def draw_lines(self) -> None:
        """Draw grid lines between cells"""
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        """Draw colored cells based on their state"""
        for y in range(self.life.rows):
            for x in range(self.life.cols):
                if self.life.curr_generation[y][x] == 1:
                    color = pygame.Color("green")
                else:
                    color = pygame.Color("white")
                pygame.draw.rect(
                    self.screen, color, (x * self.cell_size, y * self.cell_size), self.cell_size, self.cell_size
                )

    def run(self) -> None:
        """Main game loop"""
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        running = True
        paused = False

        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN and event.key == K_SPACE:
                    paused = not paused
                elif event.type == MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    x = pos[0] // self.cell_size
                    y = pos[1] // self.cell_size
                    if 0 <= x < self.life.cols and 0 <= y < self.life.rows:
                        self.life.curr_generation[y][x] = not self.life.curr_generation[y][x]

            self.screen.fill(pygame.Color("white"))

            if not paused and not self.life.is_max_generations_exceeded:
                self.life.step()

            self.draw_grid()
            self.draw_lines()
            pygame.display.flip()
            clock.tick(self.speed)


if __name__ == "__main__":
    life = GameOfLife(size=(50, 50))  # Create a 50x50 grid
    gui = GUI(life, cell_size=10, speed=10)
    gui.run()

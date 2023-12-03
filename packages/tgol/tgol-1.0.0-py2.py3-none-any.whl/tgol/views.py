import curses

from tgol.grid import Grid
from tgol.patterns import Pattern

__all__ = ["CursesView"]


class CursesView:
    def __init__(self, pattern: Pattern, gen=1000, fps=5, bbox=(0, 0, 40, 20)):
        self.pattern = pattern
        self.gen = gen
        self.fps = fps
        self.bbox = bbox

    def show(self):
        curses.wrapper(self._draw)

    def _draw(self, screen):
        grid = Grid(self.pattern)
        curses.curs_set(0)
        screen.clear()

        try:
            for _ in range(self.gen):
                screen.addstr(0, 0, grid.as_string(self.bbox))
                screen.refresh()
                curses.napms(1000 // self.fps)
                screen.clear()
                grid.evolve()

        except curses.error:
            raise ValueError(
                f"Error: terminal too small for pattern '{self.pattern.name}'"
            )

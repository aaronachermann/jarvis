import curses
import math
import threading
import time


class RingHUD(threading.Thread):
    """Animated concentric rings displayed with curses."""

    def __init__(self, stdscr: curses.window, inner_steps: int = 12, outer_steps: int = 16,
                 refresh: float = 0.1, text: str = "J.A.R.V.I.S.") -> None:
        super().__init__(daemon=True)
        self.stdscr = stdscr
        self.inner_steps = inner_steps
        self.outer_steps = outer_steps
        self.refresh = refresh
        self.text = text
        self.running = False
        self.active = False
        self.inner_idx = 0
        self.outer_idx = 0
        self.messages: list[str] = []
        curses.curs_set(0)
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_CYAN, -1)

    def run(self) -> None:
        self.running = True
        height, width = self.stdscr.getmaxyx()
        center_y = height // 2 - 2
        center_x = width // 2
        radius_inner = 2
        radius_outer = 4
        while self.running:
            self.stdscr.erase()
            if self.active:
                self._draw_ring(center_y, center_x, radius_inner,
                                self.inner_steps, self.inner_idx)
                self._draw_ring(center_y, center_x, radius_outer,
                                self.outer_steps, self.outer_idx)
                self.inner_idx = (self.inner_idx + 1) % self.inner_steps
                self.outer_idx = (self.outer_idx + 1) % self.outer_steps
            self.stdscr.attron(curses.color_pair(1) | curses.A_BOLD)
            self.stdscr.addstr(center_y, max(0, center_x - len(self.text) // 2), self.text)
            self.stdscr.attroff(curses.color_pair(1) | curses.A_BOLD)
            y = center_y + radius_outer + 2
            for i, msg in enumerate(self.messages[-5:]):
                if y + i < height:
                    self.stdscr.addstr(y + i, 0, msg[:width - 1])
            self.stdscr.refresh()
            time.sleep(self.refresh)
        self.stdscr.erase()
        self.stdscr.refresh()

    def _draw_ring(self, cy: int, cx: int, radius: int, steps: int, active: int) -> None:
        for i in range(steps):
            ang = 2 * math.pi * i / steps
            y = int(round(cy - radius * math.sin(ang)))
            x = int(round(cx + radius * math.cos(ang)))
            char = "\u25C9" if i == active else "\u25CB"  # \u25C9=◉, \u25CB=○
            try:
                self.stdscr.addstr(y, x, char)
            except curses.error:
                pass

    def start_animation(self) -> None:
        self.active = True

    def stop_animation(self) -> None:
        self.active = False

    def log(self, msg: str) -> None:
        self.messages.append(msg)
        if len(self.messages) > 5:
            self.messages.pop(0)


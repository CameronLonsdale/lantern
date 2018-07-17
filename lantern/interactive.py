"""Manage an interactive session"""

import curses
from enum import Enum


KEYS_ENTER = (curses.KEY_ENTER, ord('\n'), ord('\r'))
KEYS_RIGHT = (curses.KEY_RIGHT,)
KEYS_LEFT = (curses.KEY_LEFT,)
KEYS_EXIT = (27,)


class Stage(Enum):
    """Represent which stage the session is in"""

    SELECTION = 1
    REPLACEMENT = 2


class Interactive:
    """A Interactive session.

    Example:
        >>> Interactive("e*xample").start()
    """

    def __init__(self, text, indicator='^', start_index=0, on_change=None):
        """
        Args:
            text: The text to display
            indicator: The symbol to identify the currently selected text symbol
            start_index: The index to start with
            on_change: Function to call when a symbol has been changed by the user
        """
        self.text = text
        self.indicator = indicator
        self.index = start_index
        self.stage = Stage.SELECTION
        self.on_change = on_change

    def get_lines(self):
        """Get the lines to display on the screen"""
        if self.stage == Stage.SELECTION:
            return [self.text, ' ' * self.index + self.indicator, str(self.index)], self.index
        elif self.stage == Stage.REPLACEMENT:
            line = [self.text, ' ' * self.index + self.indicator, str(self.index), 'Enter replacement letter: ']
            return line, self.index

    def draw(self):
        """Draw the curses UI on the screen"""
        self.screen.clear()

        x, y = 1, 1
        max_y, max_x = self.screen.getmaxyx()

        lines, current_line = self.get_lines()

        # TODO: I think scrolling is needed

        for line in lines:
            if type(line) is tuple:
                self.screen.addnstr(y, x, line[0], max_x - 2, line[1])
            else:
                self.screen.addnstr(y, x, line, max_x - 2)
            y += 1

        self.screen.refresh()

    def get_selected(self):
        """Return the currently selected character"""
        return self.text[self.index]

    def move_left(self):
        """Move the cursor left"""
        self.index -= 1
        if self.index < 0:
            self.index = len(self.text) - 1

    def move_right(self):
        """Move the cursor right"""
        self.index += 1
        if self.index >= len(self.text) - 1:
            self.index = 0

    def run_loop(self):
        """Main loop"""
        while True:
            self.draw()
            c = self.screen.getch()
            if self.stage == Stage.SELECTION:
                if c in KEYS_RIGHT:
                    self.move_right()
                elif c in KEYS_LEFT:
                    self.move_left()
                elif c in KEYS_ENTER:
                    self.stage = Stage.REPLACEMENT
                elif c == 27:
                    return

            elif self.stage == Stage.REPLACEMENT:
                self.text = self.on_change_hook(self.index, c)
                self.stage = Stage.SELECTION

    def config_curses(self):
        """Configure curses"""
        curses.use_default_colors()
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_WHITE)

    def _start(self, screen):
        self.screen = screen
        self.config_curses()
        return self.run_loop()

    def start(self):
        """Start the interactive session"""
        return curses.wrapper(self._start)

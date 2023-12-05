# Copyright (C) 2023 liancea
#
# This file is part of ffmpeg-auto-settings.
#
# ffmpeg-auto-settings is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License Version 3 as published by the Free Software Foundation.
#
# ffmpeg-auto-settings is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even
# the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with ffmpeg-auto-settings. If not, see
# <https://www.gnu.org/licenses/>.

from contextlib import contextmanager
from blessings import Terminal


@contextmanager
def offset_terminal_height(bottom_offset):
    # TODO: anchor to starting line, not bottom (also in write_terminal_line)
    term = Terminal()
    with term.location(0, term.height + bottom_offset):
        yield


def write_terminal_line(bottom_offset, print_str):
    # cut off print_str to terminal width, then fill it up with spaces to fully overwrite previous prints in this line
    term = Terminal()
    terminal_width = term.width
    print_str = print_str[:terminal_width]
    print_str = print_str.ljust(terminal_width)
    with offset_terminal_height(bottom_offset):
        print(print_str)

#!/usr/bin/env python3
"""
dotpix - Terminal-based Pixel Art Editor
A simple CLI tool for creating dot pixel art in the terminal.
"""

import curses
import sys
import json
from pathlib import Path

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


class DotpixEditor:
    def __init__(self, stdscr, width=32, height=32):
        self.stdscr = stdscr
        self.width = width
        self.height = height
        self.cursor_x = width // 2
        self.cursor_y = height // 2
        self.current_color = 7  # White
        self.canvas = [[0 for _ in range(width)] for _ in range(height)]
        self.drawing = False
        self.message = ""
        
        # Color palette (curses color pairs)
        self.colors = [
            (0, 0, 0),      # 0: Black
            (128, 0, 0),    # 1: Red
            (0, 128, 0),    # 2: Green
            (128, 128, 0),  # 3: Yellow
            (0, 0, 128),    # 4: Blue
            (128, 0, 128),  # 5: Magenta
            (0, 128, 128),  # 6: Cyan
            (192, 192, 192),# 7: White (default)
            (128, 128, 128),# 8: Gray
            (255, 128, 0),  # 9: Orange
            (128, 64, 0),   # 10: Brown
            (255, 192, 203),# 11: Pink
        ]
        
        self.setup_colors()
        self.setup_screen()
    
    def setup_colors(self):
        curses.start_color()
        curses.use_default_colors()
        for i, (r, g, b) in enumerate(self.colors):
            if curses.can_change_color():
                curses.init_color(i + 100, r * 1000 // 255, g * 1000 // 255, b * 1000 // 255)
                curses.init_pair(i + 1, i + 100, i + 100)
            else:
                curses.init_pair(i + 1, -1, -1)
    
    def setup_screen(self):
        curses.curs_set(0)
        self.stdscr.nodelay(False)
        self.stdscr.timeout(-1)
        self.stdscr.keypad(True)
    
    def draw_interface(self):
        self.stdscr.clear()
        
        # Title
        title = " dotpix - Terminal Pixel Art Editor "
        self.stdscr.attron(curses.A_REVERSE)
        self.stdscr.addstr(0, 0, title.center(self.stdscr.getmaxyx()[1]))
        self.stdscr.attroff(curses.A_REVERSE)
        
        # Canvas
        start_x = 2
        start_y = 2
        cell_height = 2  # 2 lines per row for square-ish cells
        
        for y in range(self.height):
            for x in range(self.width):
                color_val = self.canvas[y][x]
                attr = curses.color_pair(color_val + 1)
                if color_val == 0:
                    attr |= curses.A_DIM
                
                # Draw cell (2 chars wide, 2 lines tall)
                char = "  " if color_val == 0 else "██"
                for row in range(cell_height):
                    try:
                        self.stdscr.addstr(start_y + y * cell_height + row, 
                                         start_x + x * 2, char, attr)
                    except curses.error:
                        pass
        
        # Cursor
        cursor_attr = curses.A_REVERSE
        if self.drawing:
            cursor_attr |= curses.A_BOLD
        try:
            for row in range(cell_height):
                self.stdscr.addstr(start_y + self.cursor_y * cell_height + row,
                                 start_x + self.cursor_x * 2, "  ", cursor_attr)
        except curses.error:
            pass
        
        # Info panel
        info_y = start_y + self.height * cell_height + 1
        self.stdscr.addstr(info_y, 0, f"Pos: ({self.cursor_x}, {self.cursor_y})  ")
        self.stdscr.addstr(f"Color: {self.current_color}  ")
        self.stdscr.addstr(f"Drawing: {'ON' if self.drawing else 'OFF'}  ")
        
        # Message
        if self.message:
            self.stdscr.addstr(info_y + 2, 0, self.message[:self.stdscr.getmaxyx()[1]-1])
        
        # Controls
        controls = [
            "Controls: Arrow=Move, Space=Draw, C=Clear, S=Save, L=Load, Q=Quit"
        ]
        for i, ctrl in enumerate(controls):
            try:
                self.stdscr.addstr(info_y + 3 + i, 0, ctrl[:self.stdscr.getmaxyx()[1]-1])
            except curses.error:
                pass
        
        self.stdscr.refresh()
    
    def set_message(self, msg):
        self.message = msg
    
    def save_canvas(self, filename):
        if filename.endswith('.json'):
            data = {
                'width': self.width,
                'height': self.height,
                'canvas': self.canvas,
                'colors': self.colors
            }
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            self.set_message(f"Saved to {filename}")
        elif filename.endswith('.png') and PIL_AVAILABLE:
            img = Image.new('RGB', (self.width * 8, self.height * 8))
            for y in range(self.height):
                for x in range(self.width):
                    color_idx = self.canvas[y][x]
                    if color_idx < len(self.colors):
                        r, g, b = self.colors[color_idx]
                    else:
                        r, g, b = 0, 0, 0
                    for py in range(8):
                        for px in range(8):
                            img.putpixel((x * 8 + px, y * 8 + py), (r, g, b))
            img.save(filename)
            self.set_message(f"Saved to {filename}")
        else:
            self.set_message("Error: PNG save requires Pillow (pip install Pillow)")
    
    def load_canvas(self, filename):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            self.width = data['width']
            self.height = data['height']
            self.canvas = data['canvas']
            self.cursor_x = self.width // 2
            self.cursor_y = self.height // 2
            self.set_message(f"Loaded {filename}")
        except Exception as e:
            self.set_message(f"Error loading: {e}")
    
    def clear_canvas(self):
        self.canvas = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.set_message("Canvas cleared")
    
    def run(self):
        while True:
            self.draw_interface()
            key = self.stdscr.getch()
            
            if key == ord('q') or key == ord('Q'):
                break
            elif key == curses.KEY_UP:
                self.cursor_y = max(0, self.cursor_y - 1)
            elif key == curses.KEY_DOWN:
                self.cursor_y = min(self.height - 1, self.cursor_y + 1)
            elif key == curses.KEY_LEFT:
                self.cursor_x = max(0, self.cursor_x - 1)
            elif key == curses.KEY_RIGHT:
                self.cursor_x = min(self.width - 1, self.cursor_x + 1)
            elif key == ord(' '):
                self.drawing = not self.drawing
                self.set_message(f"Drawing: {'ON' if self.drawing else 'OFF'}")
            elif key == ord('c') or key == ord('C'):
                self.clear_canvas()
            elif key == ord('s') or key == ord('S'):
                self.stdscr.nodelay(True)
                self.set_message("Enter filename to save: ")
                self.draw_interface()
                curses.echo()
                curses.curs_set(1)
                try:
                    filename = self.stdscr.getstr(
                        self.stdscr.getmaxyx()[0] - 2, 0, 50
                    ).decode('utf-8')
                    if filename:
                        self.save_canvas(filename)
                finally:
                    curses.noecho()
                    curses.curs_set(0)
                    self.stdscr.nodelay(False)
            elif key == ord('l') or key == ord('L'):
                self.stdscr.nodelay(True)
                self.set_message("Enter filename to load: ")
                self.draw_interface()
                curses.echo()
                curses.curs_set(1)
                try:
                    filename = self.stdscr.getstr(
                        self.stdscr.getmaxyx()[0] - 2, 0, 50
                    ).decode('utf-8')
                    if filename:
                        self.load_canvas(filename)
                finally:
                    curses.noecho()
                    curses.curs_set(0)
                    self.stdscr.nodelay(False)
            elif key == ord('1'):
                self.current_color = 0
            elif key == ord('2'):
                self.current_color = 1
            elif key == ord('3'):
                self.current_color = 2
            elif key == ord('4'):
                self.current_color = 3
            elif key == ord('5'):
                self.current_color = 4
            elif key == ord('6'):
                self.current_color = 5
            elif key == ord('7'):
                self.current_color = 6
            elif key == ord('8'):
                self.current_color = 7
            elif key == ord('9'):
                self.current_color = 8
            elif key == ord('0'):
                self.current_color = 9
            
            # Draw if drawing mode is on
            if self.drawing:
                self.canvas[self.cursor_y][self.cursor_x] = self.current_color


def main(stdscr, width=32, height=32):
    editor = DotpixEditor(stdscr, width, height)
    editor.run()


def cli_main():
    import argparse
    parser = argparse.ArgumentParser(description='Terminal Pixel Art Editor')
    parser.add_argument('-w', '--width', type=int, default=32, help='Canvas width (default: 32)')
    parser.add_argument('-H', '--height', type=int, default=32, help='Canvas height (default: 32)')
    args = parser.parse_args()
    
    print("Starting dotpix...")
    print(f"Canvas size: {args.width}x{args.height}")
    print("Press 'q' to quit, 'h' for help")
    print()
    
    curses.wrapper(lambda stdscr: main(stdscr, args.width, args.height))


if __name__ == '__main__':
    cli_main()

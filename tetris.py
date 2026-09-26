import tkinter as tk
import random
import math
import time
from enum import Enum
from tkinter import messagebox

CELL_SIZE = 30
COLUMNS = 10
ROWS =23
DELAY = 500  

colour = "#00FF55"

SHAPES = {
    '/': [[1, 1, 1],
          [0, 0, 1],
          [0, 0, 1]],
    'I': [[1, 1, 1, 1]],
    'O': [[1, 1],
          [1, 1]],
    'T': [[0, 1, 0],
          [1, 1, 1]],
    'S': [[0, 1, 1],
          [1, 1, 0]],
    'Z': [[1, 1, 0],
          [0, 1, 1]],
    'J': [[1, 0, 0],
          [1, 1, 1]],
    'L': [[0, 0, 1],
          [1, 1, 1]],
    'P': [[1, 1, 1, 1, 1]],
    'stickman': [[0,1,0],
                 [1,1,1],
                 [0,1,0],
                 [1,0,1], ],
    '0': [[1, 1, 1],
          [1, 1, 1],
          [1, 1, 1]] ,
    'o' : [[1, 1,],
           [1, 1,],
           [1, 1,]]     

}

COLORS = {
    '/': 'yellow',
    'I': 'cyan',
    'O': colour,
    'T': 'purple',
    'S': 'green',
    'Z': 'red',
    'J': 'blue',
    'L': 'orange',
    'P': 'pink',
    'stickman': 'papaya whip',
    '0': 'gold',
    'o': 'royal blue'
}


class Tetris:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=COLUMNS*CELL_SIZE, height=ROWS*CELL_SIZE, bg='black')
        self.canvas.pack()
        self.board = [[None for _ in range(COLUMNS)] for _ in range(ROWS)]
        self.current_shape = None
        self.current_pos = [0, 3]
        self.game_over = False
        self.paused = False
        self.spawn_shape()
        self.root.bind("<Key>", self.key_press)
        self.tick()

    def spawn_shape(self):
        self.shape_type = random.choice(list(SHAPES.keys()))
        self.current_shape = [row[:] for row in SHAPES[self.shape_type]]
        self.current_pos = [0, COLUMNS // 2 - len(self.current_shape[0]) // 2]
        if self.collision(self.current_shape, self.current_pos):
            self.game_over = True

    def rotate(self, shape):
        return [list(row) for row in zip(*shape[::-1])]

    def collision(self, shape, pos):
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    ny, nx = pos[0] + y, pos[1] + x
                    if nx < 0 or nx >= COLUMNS or ny >= ROWS:
                        return True
                    if ny >= 0 and self.board[ny][nx]:
                        return True
        return False

    def freeze(self):
        for y, row in enumerate(self.current_shape):
            for x, cell in enumerate(row):
                if cell:
                    ny, nx = self.current_pos[0] + y, self.current_pos[1] + x
                    if 0 <= ny < ROWS and 0 <= nx < COLUMNS:
                        self.board[ny][nx] = self.shape_type
        self.clear_lines()
        self.spawn_shape()

    def clear_lines(self):
        new_board = [row for row in self.board if any(cell is None for cell in row)]
        lines_cleared = ROWS - len(new_board)
        for _ in range(lines_cleared):
            new_board.insert(0, [None for _ in range(COLUMNS)])
        self.board = new_board

    def move(self, dy, dx):
        new_pos = [self.current_pos[0] + dy, self.current_pos[1] + dx]
        if not self.collision(self.current_shape, new_pos):
            self.current_pos = new_pos
            return True
        return False

    def drop(self):
        if not self.move(1, 0):
            self.freeze()

    def toggle_pause(self):
        if not self.game_over:
            self.paused = not self.paused

    def reset_game(self):
        # get rid of any concurrent blocks
        self.board = [[None for _ in range(COLUMNS)] for _ in range(ROWS)]
        # start over
        self.game_over = False
        self.paused = False
        # spawn a new shape
        self.spawn_shape()
        # create a new canvas
        self.draw()

    def key_press(self, event):
        # pause toggle first
        if event.keysym in ['space', 'p', 'P']:
            self.toggle_pause()
            self.canvas.create_text(COLUMNS*CELL_SIZE//2, ROWS*CELL_SIZE//2, text="Paws", fill="yellow", font=("Arial", 24))
            return

        if event.keysym == 'Escape':
            self.root.quit()

        if event.keysym == 'R':
            self.reset_game()

        if self.game_over:
            return
            # movein
        if event.keysym in ['Left', 'a', 'A']:
            self.move(0, -1)
        elif event.keysym in ['Right', 'd', 'D']:
            self.move(0, 1)
        elif event.keysym in ['Down', 's', 'S']:
            self.drop()
        elif event.keysym in ['Up', 'w', 'W']:
            rotated = self.rotate(self.current_shape)
            if not self.collision(rotated, self.current_pos):
                self.current_shape = rotated
        self.draw()

    def tick(self):
        if self.paused or self.game_over:
            if not self.game_over:
                self.root.after(DELAY, self.tick)  # continue loop
            else:
                self.canvas.create_text(COLUMNS*CELL_SIZE//2, ROWS*CELL_SIZE//2, text="GAME OVER", fill="white", font=("Arial", 24))
            return
        
        self.drop()
        self.draw()
        self.root.after(DELAY, self.tick)

    def draw(self):
        self.canvas.delete("all")
        # draw board
        for y in range(ROWS):
            for x in range(COLUMNS):
                cell = self.board[y][x]
                if cell:
                    self.draw_cell(x, y, COLORS[cell])
        # make my shape
        for y, row in enumerate(self.current_shape):
            for x, cell in enumerate(row):
                if cell:
                    nx = self.current_pos[1] + x
                    ny = self.current_pos[0] + y
                    if 0 <= nx < COLUMNS and 0 <= ny < ROWS:
                        self.draw_cell(nx, ny, COLORS[self.shape_type])

    def draw_cell(self, x, y, color):
        x1 = x * CELL_SIZE
        y1 = y * CELL_SIZE
        x2 = x1 + CELL_SIZE
        y2 = y1 + CELL_SIZE
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='gray')

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Tetris")
    game = Tetris(root)
    root.mainloop()
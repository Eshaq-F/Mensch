import tkinter as tk
from PIL import ImageTk
from setting import *


class MenschBoard:

    def __init__(self, master):
        self.canvas = tk.Canvas(master, width=Size.BOARD_WIDTH, height=Size.BOARD_HEIGHT, bg=Color.BG,
                                highlightthickness=0)
        self.left_panel = tk.Canvas(master, width=250, height=630, bg=Color.WHITE, highlightthickness=0)
        self.label = tk.Label(self.left_panel, text='Players:', bg=Color.WHITE, font=("Times", "23", "bold italic"))
        self.img = ImageTk.PhotoImage(file='Images/black_hole.jpg')
        self.black_hole = tk.Label(image=self.img, width=115, height=115)
        self.status_bar = tk.Label(master, text=Text.MADE_BY, bd=1, relief=tk.SUNKEN)

    def draw_rectangle(self, x, y, x1, y2, color, width):
        self.canvas.create_rectangle(
            x * Size.PATH_SIZE,
            y * Size.PATH_SIZE,
            x1 * Size.PATH_SIZE,
            y2 * Size.PATH_SIZE,
            fill=color, width=width)

    def path(self):

        self.canvas.place(x=370, y=0)

        for i in range(6, 9):
            for j in range(15):
                if j not in range(6, 9) and (i != 7 or j == 0 or j == 14):
                    self.draw_rectangle(i + 0.5, j + 0.5, i + 1.5, j + 1.5, Color.BG, 1)
                    self.draw_rectangle(j + 0.5, i + 0.5, j + 1.5, i + 1.5, Color.BG, 1)
                else:
                    if j < 6:
                        self.draw_rectangle(i + 0.5, j + 0.5, i + 1.5, j + 1.5, Color.YELLOW, 1)
                        self.draw_rectangle(j + 0.5, i + 0.5, j + 1.5, i + 1.5, Color.GREEN, 1)
                    elif j > 8:
                        self.draw_rectangle(i + 0.5, j + 0.5, i + 1.5, j + 1.5, Color.RED, 1)
                        self.draw_rectangle(j + 0.5, i + 0.5, j + 1.5, i + 1.5, Color.BLUE, 1)

        for i, j in Size.POSITIVE_V:
            if i > j:
                self.draw_rectangle(i + 0.5, j + 0.5, i + 1.5, j + 1.5, Color.YELLOW, 1)
            else:
                self.draw_rectangle(i + 0.5, j + 0.5, i + 1.5, j + 1.5, Color.RED, 1)

        for j, i in Size.POSITIVE_H:
            if i > j:
                self.draw_rectangle(j + 0.5, i + 0.5, j + 1.5, i + 1.5, Color.GREEN, 1)
            else:
                self.draw_rectangle(j + 0.5, i + 0.5, j + 1.5, i + 1.5, Color.BLUE, 1)

    def home(self):

        for i, j in Size.POINTS:

            if i == 0 and j == 0:
                self.draw_rectangle(i * 9 + 0.5, j * 9 + 0.5, i * 9 + 6.5, j * 9 + 6.5, Color.GREEN, 3)
            elif i == 0 and j == 1:
                self.draw_rectangle(i * 9 + 0.5, j * 9 + 0.5, i * 9 + 6.5, j * 9 + 6.5, Color.RED, 3)
            elif i == 1 and j == 0:
                self.draw_rectangle(i * 9 + 0.5, j * 9 + 0.5, i * 9 + 6.5, j * 9 + 6.5, Color.YELLOW, 3)
            else:
                self.draw_rectangle(i * 9 + 0.5, j * 9 + 0.5, i * 9 + 6.5, j * 9 + 6.5, Color.BLUE, 3)

            self.draw_rectangle(i * 9 + 1.25, j * 9 + 1.25, i * 9 + 5.75, j * 9 + 5.75, Color.WHITE, 0)

        for i, j in Size.POINTS:

            if i == 0 and j == 0:
                self.draw_rectangle(i * 9 + 1.65, j * 9 + 1.65, i * 9 + 3.3, j * 9 + 3.3, Color.GREEN, 0)
                self.draw_rectangle(i * 9 + 3.65, j * 9 + 3.65, i * 9 + 5.3, j * 9 + 5.3, Color.GREEN, 0)
                self.draw_rectangle(i * 9 + 1.65, j * 9 + 3.65, i * 9 + 3.3, j * 9 + 5.3, Color.GREEN, 0)
                self.draw_rectangle(i * 9 + 3.65, j * 9 + 1.65, i * 9 + 5.3, j * 9 + 3.3, Color.GREEN, 0)
            elif i == 0 and j == 1:
                self.draw_rectangle(i * 9 + 1.65, j * 9 + 1.65, i * 9 + 3.3, j * 9 + 3.3, Color.RED, 0)
                self.draw_rectangle(i * 9 + 3.65, j * 9 + 3.65, i * 9 + 5.3, j * 9 + 5.3, Color.RED, 0)
                self.draw_rectangle(i * 9 + 1.65, j * 9 + 3.65, i * 9 + 3.3, j * 9 + 5.3, Color.RED, 0)
                self.draw_rectangle(i * 9 + 3.65, j * 9 + 1.65, i * 9 + 5.3, j * 9 + 3.3, Color.RED, 0)
            elif i == 1 and j == 0:
                self.draw_rectangle(i * 9 + 1.65, j * 9 + 1.65, i * 9 + 3.3, j * 9 + 3.3, Color.YELLOW, 0)
                self.draw_rectangle(i * 9 + 3.65, j * 9 + 3.65, i * 9 + 5.3, j * 9 + 5.3, Color.YELLOW, 0)
                self.draw_rectangle(i * 9 + 1.65, j * 9 + 3.65, i * 9 + 3.3, j * 9 + 5.3, Color.YELLOW, 0)
                self.draw_rectangle(i * 9 + 3.65, j * 9 + 1.65, i * 9 + 5.3, j * 9 + 3.3, Color.YELLOW, 0)
            else:
                self.draw_rectangle(i * 9 + 1.65, j * 9 + 1.65, i * 9 + 3.3, j * 9 + 3.3, Color.BLUE, 0)
                self.draw_rectangle(i * 9 + 3.65, j * 9 + 3.65, i * 9 + 5.3, j * 9 + 5.3, Color.BLUE, 0)
                self.draw_rectangle(i * 9 + 1.65, j * 9 + 3.65, i * 9 + 3.3, j * 9 + 5.3, Color.BLUE, 0)
                self.draw_rectangle(i * 9 + 3.65, j * 9 + 1.65, i * 9 + 5.3, j * 9 + 3.3, Color.BLUE, 0)

    def draw_sidebar(self):
        self.left_panel.place(x=0, y=0)
        self.label.place(x=65, y=0)
        self.black_hole.place(x=631, y=261)
        self.left_panel.create_line(249, 0, 249, 630)
        self.left_panel.create_line(3, 280, 246, 280, dash=(4, 2))
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def create(self):
        self.path()
        self.home()
        self.draw_sidebar()

    def get_canvas(self):
        return self.canvas

    def get_frame(self):
        return self.left_panel

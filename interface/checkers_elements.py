import numpy as np
from PyQt5.QtGui import QPixmap, QColor, QPen
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsRectItem
from interface.util import *

# american checkers
class Figure(QGraphicsItem):
    @staticmethod
    def load_figures():
        pink = {"r": QPixmap("interface/assets/red/pink.png").scaled(60, 60)}
        white = {"w": QPixmap("interface/assets/white/white.png").scaled(60, 60)}

        return pink, white

    def __init__(self):
        super().__init__()

        self.figures_board = [[None, 'w', None, 'w', None, 'w', None, 'w'],
                              ['w', None, 'w', None, 'w', None, 'w', None],
                              [None, 'w', None, 'w', None, 'w', None, 'w'],
                              [None, None, None, None, None, None, None, None],
                              [None, None, None, None, None, None, None, None],
                              ['r', None, 'r', None, 'r', None, 'r', None],
                              [None, 'r', None, 'r', None, 'r', None, 'r'],
                              ['r', None, 'r', None, 'r', None, 'r', None]
                              ]

    def change_fig_pos(self, fig: str, idx_x: int, idx_y: int):
        self.figures_board[idx_x][idx_y] = fig

    def get_slot_key(self, idx):
        return self.figures_board[idx[0]][idx[1]]

    def check_table(self):
        board_str = ""
        for row in self.figures_board:
            row_str = " ".join([str(elem) if elem is not None else '.' for elem in row])
            board_str += row_str + "\n"
        print(board_str)

class Board:
    def __init__(self, size):
        self.slots = 8
        self.slot_size = size / self.slots

        # 1 - available
        # 0 - not available
        self.board = np.array([[0, 1, 0, 1, 0, 1, 0, 1],
                               [1, 0, 1, 0, 1, 0, 1, 0],
                               [0, 1, 0, 1, 0, 1, 0, 1],
                               [1, 0, 1, 0, 1, 0, 1, 0],
                               [0, 1, 0, 1, 0, 1, 0, 1],
                               [1, 0, 1, 0, 1, 0, 1, 0],
                               [0, 1, 0, 1, 0, 1, 0, 1],
                               [1, 0, 1, 0, 1, 0, 1, 0]])

    def create_board(self, scene, size):
        # border of plane
        border_item = QGraphicsRectItem(0, 0, size, size)
        border_pen = QPen(QColor(COLOR4))
        border_pen.setWidth(15)
        border_item.setPen(border_pen)
        scene.addItem(border_item)

        color1 = QColor(COLOR1)
        color2 = QColor(COLOR2)

        # slot init
        for i in range(self.slots):
            for j in range(self.slots):
                rect_item = QGraphicsRectItem(0 + i * self.slot_size, 0 + j *  self.slot_size,  self.slot_size,  self.slot_size)

                rect_item.setBrush(color1) if self.board[i][j] == 1 else rect_item.setBrush(color2)
                scene.addItem(rect_item)


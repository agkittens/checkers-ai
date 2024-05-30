from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsItem

#american checkers
class Figure(QGraphicsItem):
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

    @staticmethod
    def load_figures():

        red = {"r": QPixmap("assets/red/red.png").scaled(60,60),
                 "r2": QPixmap("assets/red/red2.png").scaled(60,60),
                 }

        white = {"w": QPixmap("assets/white/white.png").scaled(60,60),
                 "w2": QPixmap("assets/white/white2.png").scaled(60,60),
                 }

        return red, white




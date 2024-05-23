import sys
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem, QApplication
from PyQt5.QtCore import Qt
from figures import  Figure
import numpy as np
from util import *

class Window(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.title = "Checkers"
        self.width = self.height = 600
        self.slots = 8


        self.scene = QGraphicsScene()

        self.board = np.array([[0, 1, 0, 1, 0, 1, 0, 1],
                              [1, 0, 1, 0, 1, 0, 1, 0],
                              [0, 1, 0, 1, 0, 1, 0, 1],
                              [1, 0, 1, 0, 1, 0, 1, 0],
                              [0, 1, 0, 1, 0, 1, 0, 1],
                              [1, 0, 1, 0, 1, 0, 1, 0],
                              [0, 1, 0, 1, 0, 1, 0, 1],
                              [1, 0, 1, 0, 1, 0, 1, 0]])


        self.fig = Figure()
        self.red_img, self.white_img = self.fig.load_figures()
        self.red, self.white = [], []


        self.create_window()


    def create_window(self):
        self.setWindowTitle(self.title)
        self.setGeometry(0,0, self.width, self.height)
        self.setSceneRect(0, 0, self.width, self.height)
        self.setScene(self.scene)

        self.create_board()
        self.place_figures()

        self.show()


    def create_board(self):
        size_w = self.width / self.slots
        size_h = self.height / self.slots

        color1 = QColor(COLOR1)
        color2 = QColor(COLOR2)

        for i in range(self.slots):
            for j in range(self.slots):
                rect_item = QGraphicsRectItem(0 + i * size_w, 0 + j * size_h, size_w, size_h)

                if self.board[i][j] == 0:
                    rect_item.setBrush(color2)
                elif self.board[i][j] == 1:
                    rect_item.setBrush(color1)

                #1 - avaible
                #0 - not avaible
                rect_item.setData(Qt.UserRole, 1)
                self.scene.addItem(rect_item)


    def place_figures(self):
        indices = np.argwhere(self.board == 1)

        for idx in indices:
            key = self.fig.figures_board[idx[0]][idx[1]]

            if key == "r":
                item = self.scene.addPixmap(self.red_img[f'{key}'])
                item.setPos(8 + idx[1] * 75, 8 + idx[0] * 75)
                item.setData(Qt.UserRole, key)
                item.setZValue(1)
                self.red.append(item)

            if key == "w":
                item = self.scene.addPixmap(self.white_img[f'{key}'])
                item.setPos(8 + idx[1] * 75, 8 + idx[0] * 75)
                item.setData(Qt.UserRole, key)
                item.setZValue(1)
                self.white.append(item)


def main():
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())

main()
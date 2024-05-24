import sys
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem, QApplication, QGraphicsPixmapItem
from PyQt5.QtCore import Qt, QPointF
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
        self.drag_item = None
        self.drag_offset = QPointF()
        self.original_pos = QPointF()

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


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            scene_pos = self.mapToScene(event.pos())
            item = self.scene.itemAt(scene_pos, self.transform())

            if item and isinstance(item, QGraphicsPixmapItem):
                self.drag_item = item
                self.original_pos = item.pos()
                self.drag_offset = scene_pos - item.pos()
            else:
                self.drag_item = None

    def mouseMoveEvent(self, event):
        if self.drag_item:
            scene_pos = self.mapToScene(event.pos())
            self.drag_item.setPos(scene_pos - self.drag_offset)

    def mouseReleaseEvent(self, event):
        if self.drag_item:
            scene_pos = self.mapToScene(event.pos())
            grid_size = self.width / self.slots
            grid_x = round((scene_pos.x() - self.drag_offset.x() - 8) / grid_size)
            grid_y = round((scene_pos.y() - self.drag_offset.y() - 8) / grid_size)

            if grid_x in range(0,self.slots+1) and grid_y in range(0,self.slots+1):

                if self.board[grid_y][grid_x] == 1:
                    final_x = grid_x * grid_size + 8
                    final_y = grid_y * grid_size + 8
                    self.drag_item.setPos(final_x, final_y)

                else:
                    self.drag_item.setPos(self.original_pos)
            else:
                self.drag_item.setPos(self.original_pos)

            self.drag_item = None

def main():
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())

main()
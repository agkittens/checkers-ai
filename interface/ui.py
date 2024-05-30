import sys
import threading

from PyQt5.QtGui import QColor, QImage, QPixmap
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem, QApplication, QGraphicsPixmapItem
from PyQt5.QtCore import Qt, QPointF
from figures import Figure
import numpy as np
from util import *

class Window(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.title = "Checkers"
        self.width = self.height = 600
        self.slots = 8

        self.scene = QGraphicsScene()

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
        self.load_bg()

        self.show()

    def load_bg(self):
        self.scene.setBackgroundBrush(QColor(COLOR3))

        background_image = QImage(BG_PATH)

        background_pixmap = QGraphicsPixmapItem(QPixmap.fromImage(background_image))
        background_pixmap.setTransformationMode(Qt.TransformationMode.SmoothTransformation)
        background_pixmap.setPos(-700, -700)
        background_pixmap.setZValue(-1)

        self.scene.addItem(background_pixmap)


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

                self.scene.addItem(rect_item)

    def place_figures(self):
        indices = np.argwhere(self.board == 1)

        for idx in indices:
            key = self.fig.figures_board[idx[0]][idx[1]]

            if key == "r":
                item = self.scene.addPixmap(self.red_img[f'{key}'])
                item.setPos(8 + idx[1] * 75, 8 + idx[0] * 75)
                item.setData(Qt.UserRole, key)
                item.setData(Qt.UserRole+1, (idx[0], idx[1]))
                item.setZValue(1)
                self.red.append(item)

            if key == "w":
                item = self.scene.addPixmap(self.white_img[f'{key}'])
                item.setPos(8 + idx[1] * 75, 8 + idx[0] * 75)
                item.setData(Qt.UserRole, key)
                item.setData(Qt.UserRole+1, (idx[0], idx[1]))
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
                pos = self.drag_item.data(Qt.UserRole+1)
                self.fig.change_fig_pos(None, pos[0], pos[1])
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
                    self.drag_item.setData(Qt.UserRole+1, (grid_y,grid_x))
                    self.fig.change_fig_pos(self.drag_item.data(Qt.UserRole),
                                            grid_y,
                                            grid_x)

                else:
                    self.drag_item.setPos(self.original_pos)
                    pos = self.drag_item.data(Qt.UserRole + 1)
                    self.fig.change_fig_pos(self.drag_item.data(Qt.UserRole),
                                            pos[0],
                                            pos[1])
            else:
                self.drag_item.setPos(self.original_pos)
                pos = self.drag_item.data(Qt.UserRole + 1)

                self.fig.change_fig_pos(self.drag_item.data(Qt.UserRole),
                                        pos[0],
                                        pos[1])

            self.drag_item = None
            self.check_table()

    def check_table(self):
        board_str = ""
        for row in self.fig.figures_board:
            row_str = " ".join([str(elem) if elem is not None else '.' for elem in row])
            board_str += row_str + "\n"
        print(board_str)

    def move_piece_console(self):
        while True:
            try:
                src_x = int(input("Enter source x: "))
                src_y = int(input("Enter source y: "))
                dest_x = int(input("Enter destination x: "))
                dest_y = int(input("Enter destination y: "))

                if self.board[src_y][src_x] == 1 and self.board[dest_y][dest_x] == 1:

                    item_to_move = None

                    for item in self.scene.items():
                        if isinstance(item, QGraphicsPixmapItem):
                            pos = item.data(Qt.UserRole + 1)
                            if pos == (src_y, src_x):
                                item_to_move = item
                                break

                    if item_to_move:
                        self.fig.change_fig_pos(None, src_y, src_x)
                        self.fig.change_fig_pos(item_to_move.data(Qt.UserRole),
                                                dest_y,
                                                dest_x)

                        grid_size = self.width / self.slots
                        final_x = dest_x * grid_size + 8
                        final_y = dest_y * grid_size + 8

                        item_to_move.setPos(final_x, final_y)
                        item_to_move.setData(Qt.UserRole + 1, (dest_y, dest_x))

                        self.check_table()
                        self.refresh_scene()

                    else:
                        print("No piece at the source position.")
                else:
                    print("Invalid move. Please try again.")

            except ValueError:
                print("Invalid input. Please enter integers only.")

    def refresh_scene(self):
        for item in self.scene.items():
            item.update()

def main():
    app = QApplication(sys.argv)
    window = Window()
    threading.Thread(target=window.move_piece_console, daemon=True).start()

    sys.exit(app.exec_())

main()


import time
from PyQt5.QtGui import QColor, QImage, QPixmap, QPen, QFont, QPainterPath, QRegion
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem, QApplication, QGraphicsPixmapItem, \
    QPushButton, QGraphicsDropShadowEffect, QLabel
from PyQt5.QtCore import Qt, QPointF, pyqtSignal, QRectF
import numpy as np
from interface.util import *
from checkers import *
from manager import *
from interface.figures import Figure

# TODO: please add scoring using self.score edict and turn change using self.current_turn (both things already on ui)
# TODO: also consider moving game events to a new file non related to "static" ui objects

class Window(QGraphicsView):
    movePieceSignal = pyqtSignal(int, int, int, int)

    def __init__(self):
        super().__init__()
        self.title = "Checkers"
        self.width = self.height = 600
        self.slots = 8

        self.checkers = initialize_board()
        self.player = "red"
        self.did_capture = False
        self.capturing_piece = None
        self.is_game_over = 0
        self.current_turn = 1
        self.score = {"white": 0, "red": 0}

        self.manager = Manager()

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
        self.movePieceSignal.connect(self.make_move)

    def create_window(self):
        self.setWindowTitle(self.title)
        self.setGeometry(0, 0, self.width, self.height)
        self.setSceneRect(0, 0, self.width, self.height)
        self.setScene(self.scene)

        self.create_board()
        self.place_figures()
        self.load_bg()
        self.add_buttons()
        self.show_turn()
        self.update_turn()
        self.show_scoreboard()
        self.update_scoreboard()
        self.show()

    def load_bg(self):
        self.scene.setBackgroundBrush(QColor(COLOR3))

        background_image = QImage(BG_PATH)

        background_pixmap = QGraphicsPixmapItem(QPixmap.fromImage(background_image))
        background_pixmap.setTransformationMode(Qt.TransformationMode.SmoothTransformation)
        background_pixmap.setPos(-350, -200)
        background_pixmap.setZValue(-1)

        self.scene.addItem(background_pixmap)

    def add_buttons(self):
        self.one_robotK = QPushButton("Player vs Kawasaki", self)
        self.one_robotK.resize(250, 90)
        self.one_robotK.move(40, 200)
        self.one_robotK.clicked.connect(lambda: self.manager.add_robot("kawasaki"))

        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setBlurRadius(15)
        shadow_effect.setColor(QColor(145, 90, 87, 127))
        shadow_effect.setOffset(0, 7)
        self.one_robotK.setGraphicsEffect(shadow_effect)

        self.one_robotM = QPushButton("Player vs Mitsubishi", self)
        self.one_robotM.resize(250, 90)
        self.one_robotM.move(40, 350)
        self.one_robotM.clicked.connect(lambda: self.manager.add_robot("mitsubishi"))

        shadow_effect_1 = QGraphicsDropShadowEffect()
        shadow_effect_1.setBlurRadius(15)
        shadow_effect_1.setColor(QColor(145, 90, 87, 127))
        shadow_effect_1.setOffset(0, 7)
        self.one_robotM.setGraphicsEffect(shadow_effect_1)

        self.two_robots = QPushButton("Kawasaki Vs Mitsubishi", self)
        self.two_robots.resize(250, 90)
        self.two_robots.move(40, 500)
        self.two_robots.clicked.connect(
            lambda: (self.manager.add_robot("mitsubishi"), self.manager.add_robot("kawasaki")))

        shadow_effect_2 = QGraphicsDropShadowEffect()
        shadow_effect_2.setBlurRadius(15)
        shadow_effect_2.setColor(QColor(145, 90, 87, 127))
        shadow_effect_2.setOffset(0, 7)
        self.two_robots.setGraphicsEffect(shadow_effect_2)
        self.setStyleSheet(STYLE)

    def create_board(self):
        size_w = self.width / self.slots
        size_h = self.height / self.slots

        color1 = QColor(COLOR1)
        color2 = QColor(COLOR2)
        color3 = QColor(COLOR4)

        border_item = QGraphicsRectItem(0, 0, self.width, self.height)
        border_pen = QPen(QColor(color3))
        border_pen.setWidth(15)
        border_item.setPen(border_pen)
        self.scene.addItem(border_item)

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
                item.setData(Qt.UserRole + 1, (idx[0], idx[1]))
                item.setZValue(1)
                self.red.append(item)

            if key == "w":
                item = self.scene.addPixmap(self.white_img[f'{key}'])
                item.setPos(8 + idx[1] * 75, 8 + idx[0] * 75)
                item.setData(Qt.UserRole, key)
                item.setData(Qt.UserRole + 1, (idx[0], idx[1]))
                item.setZValue(1)
                self.white.append(item)

    def show_turn(self):
        self.turn = QLabel()
        self.turn.setFont(QFont("Arial", 12, weight=QFont.Bold))
        self.turn.setFixedSize(200, 60)
        self.turn.setAlignment(Qt.AlignCenter)

        self.round_label(self.turn)

        turn = self.scene.addWidget(self.turn)
        turn.setPos(200, -100)

        self.turn.setStyleSheet(STYLE)


    def update_turn(self):
        if self.current_turn % 2 == 0:
            self.turn.setText("WHITE'S TURN")
        elif self.current_turn % 2 == 1:
            self.turn.setText("RED'S TURN")

    def show_scoreboard(self):
        self.sc = QLabel()
        self.sc.setFont(QFont("Arial", 12, weight=QFont.Bold))
        self.sc.setFixedSize(200, 100)
        self.sc.setAlignment(Qt.AlignCenter)

        self.round_label(self.sc)

        sc = self.scene.addWidget(self.sc)
        sc.setPos(970, 0)

        self.sc.setStyleSheet(STYLE)

    def update_scoreboard(self):
        self.sc.setText(f"WHITE: {self.score['white']}\nRED: {self.score['red']}")

    def round_label(self, object):
        object.setAutoFillBackground(True)
        palette = object.palette()
        palette.setColor(object.backgroundRole(), QColor("#e36f70"))
        object.setPalette(palette)

        path = QPainterPath()
        rect = QRectF(object.rect())
        path.addRoundedRect(rect, 10, 10)
        polygon = path.toFillPolygon().toPolygon()
        object.setMask(QRegion(polygon))


    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:

            scene_pos = self.mapToScene(event.pos())
            item = self.scene.itemAt(scene_pos, self.transform())

            if item and isinstance(item, QGraphicsPixmapItem) and self.is_game_over == 0:
                self.drag_item = item
                self.original_pos = item.pos()
                self.drag_offset = scene_pos - item.pos()
                pos = self.drag_item.data(Qt.UserRole + 1)
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

            orig_x = round((self.original_pos.x() - 8) / grid_size)
            orig_y = round((self.original_pos.y() - 8) / grid_size)

            if grid_x in range(0, self.slots + 1) and grid_y in range(0, self.slots + 1):
                move = ((orig_y, orig_x), (grid_y, grid_x))
                self.handle_move(move)

            else:
                self.put_down(None, None, None, False)

            self.drag_item = None
            self.check_table()

    def handle_move(self, move):
        if check_valid_human(self.checkers,self.did_capture,self.capturing_piece,move):
            ((orig_y, orig_x), (grid_y, grid_x)) = move

            self.checkers = make_move(self.checkers, move)

            if abs(orig_y - grid_y) == 2:
                capture_row = (orig_y + grid_y) // 2
                capture_col = (orig_x + grid_x) // 2
                self.delete_item_at(capture_row, capture_col)

            self.put_down(self.drag_item, grid_x, grid_y)

            if get_possible_captures(self.checkers, move[1]):
                self.did_capture = True
                self.capturing_piece = move[1]
                return
            else:
                self.did_capture = False
                self.capturing_piece = None

            self.is_game_over = is_game_over(self.checkers)
            if self.is_game_over:
                return

            self.do_ai_move()
        else:
            self.put_down(None, None, None, False)

    def do_ai_move(self):
        self.player = "white"
        self.current_turn += 1

        src_x, src_y, dest_x, dest_y = ai_logic(self.checkers, self.did_capture, self.capturing_piece)
        self.make_move(src_x, src_y, dest_x, dest_y)

        self.is_game_over = is_game_over(self.checkers)
        if self.is_game_over:
            return

        if can_capture_more(self.checkers, src_x, src_y, dest_x, dest_y):
            self.did_capture = True
            self.capturing_piece = (dest_y,dest_x)
            self.do_ai_move()
        else:
            self.did_capture = False

        self.player = "red"
    def check_table(self):
        board_str = ""
        for row in self.fig.figures_board:
            row_str = " ".join([str(elem) if elem is not None else '.' for elem in row])
            board_str += row_str + "\n"
        print(board_str)

    def type_move(self):
        while True:
            try:
                src_x = int(input("Enter source x: "))
                src_y = int(input("Enter source y: "))
                dest_x = int(input("Enter destination x: "))
                dest_y = int(input("Enter destination y: "))

                if self.board[src_y][src_x] == 1 and self.board[dest_y][dest_x] == 1:
                    self.movePieceSignal.emit(src_x, src_y, dest_x, dest_y)
                else:
                    print("Invalid move. Please try again.")

            except ValueError:
                print("Invalid input. Please enter integers only.")

    def delete_item_at(self, capture_row, capture_col):
        for item in self.scene.items():
            if isinstance(item, QGraphicsPixmapItem):
                pos = item.data(Qt.UserRole + 1)
                if pos == (capture_row, capture_col):
                    self.scene.removeItem(item)
                    self.score[self.player] += 1

    def make_move(self, src_x, src_y, dest_x, dest_y):
        if abs(src_y - dest_y) == 2:
            capture_row = (src_y + dest_y) // 2
            capture_col = (src_x + dest_x) // 2
            self.delete_item_at(capture_row, capture_col)
        item_to_move = None

        for item in self.scene.items():
            if isinstance(item, QGraphicsPixmapItem):
                pos = item.data(Qt.UserRole + 1)
                if pos == (src_y, src_x):
                    item_to_move = item
                    break

        if item_to_move:
            self.fig.change_fig_pos(None, src_y, src_x)
            self.put_down(item_to_move, dest_x, dest_y)

            self.check_table()
            self.refresh_scene()
            self.update_turn()
            self.update_scoreboard()

        else:
            print("No piece at the source position.")

    def put_down(self, item, x, y, correct=True):
        if correct:
            grid_size = self.width / self.slots
            final_x = x * grid_size + 8
            final_y = y * grid_size + 8

            item.setPos(final_x, final_y)
            item.setData(Qt.UserRole + 1, (y, x))
            self.fig.change_fig_pos(item.data(Qt.UserRole),
                                    y,
                                    x)
            self.current_turn += 1
        else:
            self.drag_item.setPos(self.original_pos)
            pos = self.drag_item.data(Qt.UserRole + 1)
            self.fig.change_fig_pos(self.drag_item.data(Qt.UserRole),
                                    pos[0],
                                    pos[1])

    def refresh_scene(self):
        for item in self.scene.items():
            item.update()


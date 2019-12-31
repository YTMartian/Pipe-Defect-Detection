from PyQt5.QtWidgets import QMainWindow, QGraphicsDropShadowEffect, QLabel
from PyQt5.QtCore import pyqtSignal, QPoint
from PyQt5.QtGui import QIcon, QColor, QCursor, QEnterEvent, QPainter, QPen, QPixmap
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
from resources import *
import time
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Pipe Defect Detection')
        self.setWindowIcon(QIcon(':/app_icon'))
        self.setMinimumSize(1280, 720)

        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)  # set background transparent.
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # hide the frame.
        self.setMouseTracking(True)
        self.move_window_flag = False
        self.move_position = None
        self.mouse_position = None

        # below is to resize window.
        self.margin = 2  # can adjust window size when mouse at the margin 5 pixels.
        self.direction = None
        self.pressed = False
        self.margin_top = 0
        self.margin_bottom = 1
        self.margin_left = 2
        self.margin_right = 3
        self.margin_left_top = 4
        self.margin_left_bottom = 5
        self.margin_right_top = 6
        self.margin_right_bottom = 7
        self.installEventFilter(self)

        self.main_widget = QtWidgets.QWidget()  # main window.
        background = QtGui.QPalette()
        background.setBrush(self.main_widget.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(':/background')))
        self.main_widget.setAutoFillBackground(True)
        self.main_widget.setPalette(background)
        self.main_layout = QtWidgets.QGridLayout()  # create main window layout.
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(
            self.margin, self.margin, self.margin, self.margin)  # the margin between layout and main window.
        self.main_widget.setLayout(self.main_layout)  # set main window layout.

        self.top_widget = QtWidgets.QWidget()  # create top part widget.
        self.top_widget.setObjectName('top_widget')
        self.top_layout = QtWidgets.QHBoxLayout()  # create top part layout.
        self.top_layout.setSpacing(10)
        self.top_layout.addStretch()
        self.top_layout.setAlignment(QtCore.Qt.AlignTop)
        self.top_widget.setLayout(self.top_layout)  # set top part layout.
        # self.top_widget.installEventFilter(self)  # bind event filter.

        self.left_widget = QtWidgets.QWidget()  # create left part.
        self.left_widget.setObjectName('left_widget')
        self.left_layout = QtWidgets.QGridLayout()  # create left part layout.
        self.left_layout.setContentsMargins(10, 10, 10, 10)
        self.left_widget.setLayout(self.left_layout)  # set left part layout.
        self.left_widget_shadow = QGraphicsDropShadowEffect()  # set shadow.
        self.left_widget_shadow.setBlurRadius(50)
        self.left_widget_shadow.setColor(QColor(0, 0, 0, 70))
        self.left_widget_shadow.setOffset(10, 0)
        self.left_widget.setGraphicsEffect(self.left_widget_shadow)
        self.left_widget.setFixedWidth(250)
        self.left_widget.setStyleSheet('''
            QWidget#left_widget{
                background-color: rgba(131,148,155,0.25);
            }
        ''')

        self.top_close = QtWidgets.QPushButton()  # close window button.
        self.top_close.setFixedSize(25, 25)
        # self.top_close.setIcon(QIcon(":/close"))
        self.top_close.setToolTip('关闭')
        self.top_close.setCursor(QCursor(QtCore.Qt.PointingHandCursor))  # set cursor when hover.
        self.top_close.setStyleSheet('''
            QPushButton{
                background-color:transparent;
                border-radius:5px;
                color:white;
                padding-bottom:2px;
                background-image:url(:/close);
            }
            QPushButton:hover{
                background-image:url(:/close_hover);
                background-repeat:no-repeat center
            }
        ''')
        self.top_close.clicked.connect(self.top_close_clicked)
        self.top_maximize = QtWidgets.QPushButton()  # enlarge window button.
        # self.top_maximize.setIcon(QIcon(":/maximize"))
        self.top_maximize.setFixedSize(25, 25)
        self.top_maximize.setToolTip('最大化')
        self.top_maximize.setCursor(QCursor(QtCore.Qt.PointingHandCursor))  # set cursor when hover.
        self.top_maximize.setStyleSheet('''
            QPushButton{
                background-image:url(:/maximize);
                border-radius:5px;
                color:white;
                padding-bottom:2px;
            }
            QPushButton:hover{
                background-image:url(:/maximize_hover);
                background-repeat:no-repeat center
            }
        ''')
        self.top_maximize.clicked.connect(self.top_maximize_clicked)
        self.top_minimize = QtWidgets.QPushButton()  # minimize window button.
        self.top_minimize.setFixedSize(25, 25)
        # self.top_minimize.setIcon(QIcon(":/minimize"))
        self.top_minimize.setToolTip('最小化')
        self.top_minimize.setCursor(QCursor(QtCore.Qt.PointingHandCursor))  # set cursor when hover.
        self.top_minimize.setStyleSheet('''
            QPushButton{
                background-color:transparent;
                border-radius:5px;
                color:white;
                background-image:url(:/minimize);
            }
            QPushButton:hover{
                background-image:url(:/minimize_hover);
                background-repeat:no-repeat center
            }
        ''')
        self.top_minimize.clicked.connect(self.showMinimized)

        self.main_layout.addWidget(self.top_widget, 1, 0, 1, 15)  # start from (x1,y1) and occupy (x2,y2)
        self.main_layout.addWidget(self.left_widget, 1, 0, 11, 2)
        self.setCentralWidget(self.main_widget)  # set main window's main widget.

        self.top_layout.addWidget(self.top_minimize)
        self.top_layout.addWidget(self.top_maximize)
        self.top_layout.addWidget(self.top_close)

        self.app = QLabel()
        self.app.setPixmap(QPixmap(':/app'))
        self.app.setContentsMargins(0, 20, 0, 0)
        self.left_layout.addWidget(self.app, 1, 0, 10, 10, QtCore.Qt.AlignTop)
        self.test = QLabel()
        self.test.setText('工程列表')
        self.test.setStyleSheet('''QLabel{}''')
        self.left_layout.addWidget(self.test, 2, 5, 1, 1, QtCore.Qt.AlignCenter)

    @staticmethod
    def top_close_clicked(self):
        time.sleep(0.1)  # so...
        exit()

    def top_maximize_clicked(self):
        if self.isMaximized():
            self.showNormal()
            self.top_maximize.setToolTip('最大化')
        else:
            self.showMaximized()
            self.top_maximize.setToolTip('还原')

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.HoverMove:
            if self.pressed:
                return True
            x = event.pos().x()
            y = event.pos().y()
            # print(x, y)
            if x < self.margin:
                if y < self.margin:
                    self.direction = self.margin_left_top
                    self.setCursor(QtCore.Qt.SizeFDiagCursor)
                elif y > self.height() - self.margin:
                    self.direction = self.margin_left_bottom
                    self.setCursor(QtCore.Qt.SizeBDiagCursor)
                else:
                    self.direction = self.margin_left
                    self.setCursor(QtCore.Qt.SizeHorCursor)
            elif x > self.width() - self.margin:
                if y < self.margin:
                    self.direction = self.margin_right_top
                    self.setCursor(QtCore.Qt.SizeBDiagCursor)
                elif y > self.height() - self.margin:
                    self.direction = self.margin_right_bottom
                    self.setCursor(QtCore.Qt.SizeFDiagCursor)
                else:
                    self.direction = self.margin_right
                    self.setCursor(QtCore.Qt.SizeHorCursor)
            elif y < self.margin and self.direction is None:
                self.direction = self.margin_top
                self.setCursor(QtCore.Qt.SizeVerCursor)
            elif y > self.height() - self.margin and self.direction is None:
                self.direction = self.margin_bottom
                self.setCursor(QtCore.Qt.SizeVerCursor)
            else:
                self.direction = None
                self.setCursor(QtCore.Qt.ArrowCursor)
            return True
        return False

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.pressed = True
            self.mouse_position = event.pos()
        top_widget_height = self.top_widget.size().height()
        now_mouse_y = event.globalPos().y() - self.pos().y()
        if event.button() == QtCore.Qt.LeftButton and now_mouse_y < top_widget_height:
            if self.isMaximized():
                self.showNormal()
                print(event.globalPos().x(), "---", self.move_position.x())
                x1 = event.globalPos().x()
                x2 = self.move_position.x()
                if x1 < x2:
                    self.move(0, event.globalPos().y() - self.move_position.y())
                else:
                    self.move((x1 - x2) / 1.2, event.globalPos().y() - self.move_position.y())
            self.move_window_flag = True
            self.move_position = event.globalPos() - self.pos()  # get mouse position relative to window.
            event.accept()  # it means the event is handled.

    def mouseMoveEvent(self, event):
        super(MainWindow, self).mouseMoveEvent(event)
        if event.buttons() == QtCore.Qt.LeftButton and self.direction is not None:
            if self.isMaximized():
                return
            if self.pressed:
                self.resize_window(self, event.pos())
                return
            x = event.pos().x()
            y = event.pos().y()
            if x < self.margin:
                if y < self.margin:
                    self.direction = self.margin_left_top
                elif y > self.height() - self.margin:
                    self.direction = self.margin_left_bottom
                else:
                    self.direction = self.margin_left
            elif x > self.width() - self.margin:
                if y < self.margin:
                    self.direction = self.margin_right_top
                elif y > self.height() - self.margin:
                    self.direction = self.margin_right_bottom
                else:
                    self.direction = self.margin_right
            elif y < self.margin and self.direction is None:
                self.direction = self.margin_top
            elif y > self.height() - self.margin and self.direction is None:
                self.direction = self.margin_bottom
            elif not self.pressed:
                self.direction = None
            self.resize_window(self, event.pos())
            return
        elif event.buttons() == QtCore.Qt.LeftButton and self.move_window_flag:
            self.move(event.globalPos() - self.move_position)

    def mouseReleaseEvent(self, QMouseEvent):
        self.move_window_flag = False
        self.pressed = False
        self.direction = None

    def mouseDoubleClickEvent(self, event):
        top_widget_height = self.top_widget.size().height()
        now_mouse_y = event.globalPos().y() - self.pos().y()
        if now_mouse_y < top_widget_height:
            if self.isMaximized():
                self.showNormal()
                self.top_maximize.setToolTip('最大化')
            else:
                self.showMaximized()
                self.top_maximize.setToolTip('还原')

    @staticmethod
    def resize_window(self, pos):
        pos_ = pos - self.mouse_position
        pos_x, pos_y = pos_.x(), pos_.y()
        geometry = self.geometry()
        x, y, w, h = geometry.x(), geometry.y(), geometry.width(), geometry.height()
        if self.direction == self.margin_left_top:
            if w - pos_x > self.minimumWidth():
                x += pos_x
                w -= pos_x
            if h - pos_y > self.minimumHeight():
                y += pos_y
                h -= pos_y
        elif self.direction == self.margin_right_bottom:
            if w + pos_x > self.minimumWidth():
                w += pos_x
                self.mouse_position = pos
            if h + pos_y > self.minimumHeight():
                h += pos_y
                self.mouse_position = pos
        elif self.direction == self.margin_right_top:
            if h - pos_y > self.minimumHeight():
                y += pos_y
                h -= pos_y
            if w + pos_x > self.minimumWidth():
                w += pos_x
                self.mouse_position.setX(pos.x())
        elif self.direction == self.margin_left_bottom:
            if w - pos_x > self.minimumWidth():
                x += pos_x
                w -= pos_x
            if h + pos_y > self.minimumHeight():
                h += pos_y
                self.mouse_position.setY(pos.y())
        elif self.direction == self.margin_left:
            if w - pos_x > self.minimumWidth():
                x += pos_x
                w -= pos_x
            else:
                return
        elif self.direction == self.margin_right:
            if w + pos_x > self.minimumWidth():
                w += pos_x
                self.mouse_position = pos
            else:
                return
        elif self.direction == self.margin_top:
            if h - pos_y > self.minimumHeight():
                y += pos_y
                h -= pos_y
            else:
                return
        elif self.direction == self.margin_bottom:
            if h + pos_y > self.minimumHeight():
                h += pos_y
                self.mouse_position = pos
            else:
                return
        self.setGeometry(x, y, w, h)


def main():
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

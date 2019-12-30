from PyQt5.QtWidgets import QMainWindow, QGraphicsDropShadowEffect
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon, QColor
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
        self.setWindowIcon(QIcon(':/app'))
        self.setMinimumSize(1280, 720)
        self.background = QtGui.QPalette()
        self.background.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(':/background')))
        self.setPalette(self.background)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # hide the frame.
        self.setMouseTracking(True)
        self.is_maximized = False

        self.main_widget = QtWidgets.QWidget()  # main window.
        self.main_layout = QtWidgets.QGridLayout()  # create main window layout.
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)  # the margin between layout and main window.
        self.main_widget.setLayout(self.main_layout)  # set main window layout.

        self.top_widget = QtWidgets.QWidget()  # create top part widget.
        self.top_widget.setObjectName('top_widget')
        self.top_layout = QtWidgets.QHBoxLayout()  # create top part layout.
        self.top_layout.setSpacing(10)
        self.top_layout.addStretch()
        self.top_layout.setAlignment(QtCore.Qt.AlignTop)
        self.top_widget.setLayout(self.top_layout)  # set top part layout.

        self.left_widget = QtWidgets.QWidget()  # create left part.
        self.left_widget.setObjectName('left_widget')
        self.left_layout = QtWidgets.QGridLayout()  # create left part layout.
        self.left_layout.setContentsMargins(10, 10, 10, 10)
        self.left_widget.setLayout(self.left_layout)  # set left part layout.
        self.left_widget_shadow = QGraphicsDropShadowEffect()  # set shadow.
        self.left_widget_shadow.setBlurRadius(10)
        self.left_widget_shadow.setColor(QColor(111, 0, 0, 500))
        self.left_widget_shadow.setOffset(5, 5)
        self.left_widget.setGraphicsEffect(self.left_widget_shadow)
        self.left_widget.setStyleSheet('''
            QWidget#left_widget{
                background-color: transparent;
            }
        ''')

        self.top_close = QtWidgets.QPushButton()  # close window button.
        self.top_close.setFixedSize(30, 30)
        self.top_close.setIcon(QIcon(":/close"))
        self.top_close.setToolTip('关闭')
        self.top_close.setStyleSheet('''
            QPushButton{
                background-color:transparent;
                border-radius:5px;
                color:white;
                padding-bottom:2px;
            }
            QPushButton:hover{
                background:red;
            }
        ''')
        self.top_close.clicked.connect(self.top_close_clicked)
        self.top_maximize = QtWidgets.QPushButton()  # enlarge window button.
        self.top_maximize.setIcon(QIcon(":/maximize"))
        self.top_maximize.setFixedSize(30, 30)
        self.top_maximize.setToolTip('最大化')
        self.top_maximize.setStyleSheet('''
            QPushButton{
                background-color:transparent;
                border-radius:5px;
                color:white;
                padding-bottom:2px;
            }
            QPushButton:hover{
                background:#5cce5a;
            }
        ''')
        self.top_maximize.clicked.connect(self.top_maximize_clicked)
        self.top_minimize = QtWidgets.QPushButton()  # minimize window button.
        self.top_minimize.setFixedSize(30, 30)
        self.top_minimize.setIcon(QIcon(":/minimize"))
        self.top_minimize.setToolTip('最小化')
        self.top_minimize.setStyleSheet('''
            QPushButton{
                background-color:transparent;
                border-radius:5px;
                color:white;
            }
            QPushButton:hover{
                background:#efef00;
            }
        ''')
        self.top_minimize.clicked.connect(self.showMinimized)

        self.main_layout.addWidget(self.top_widget, 1, 0, 1, 15)  # start from (x1,y1) and occupy (x2,y2)
        self.main_layout.addWidget(self.left_widget, 1, 0, 11, 2)
        self.setCentralWidget(self.main_widget)  # set main window's main widget.

        self.top_layout.addWidget(self.top_minimize)
        self.top_layout.addWidget(self.top_maximize)
        self.top_layout.addWidget(self.top_close)

    @staticmethod
    def top_close_clicked(self):
        time.sleep(0.1)  # so...
        exit()

    def top_maximize_clicked(self):
        if self.is_maximized:
            self.showNormal()
            self.top_maximize.setToolTip('最大化')
        else:
            self.showMaximized()
            self.top_maximize.setToolTip('还原')
        self.is_maximized = not self.is_maximized


def main():
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

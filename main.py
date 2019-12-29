from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QIcon
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from resources import *
import time
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Pipe Defect Detection')
        self.setWindowIcon(QIcon(":/app"))
        self.setMinimumSize(1280, 720)
        self.setStyleSheet('''background-color:white''')
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # hide the frame.
        self.is_maximized = False
        self.origin_size = self.size()
        self.position = self.pos()

        self.main_widget = QtWidgets.QWidget()  # main window.
        self.main_layout = QtWidgets.QGridLayout()  # create main window layout.
        self.main_layout.setSpacing(0)
        self.main_widget.setLayout(self.main_layout)  # set main window layout.

        self.top_widget = QtWidgets.QWidget()  # create top part widget.
        self.top_widget.setObjectName('top_widget')
        self.top_layout = QtWidgets.QHBoxLayout()  # create top part layout.
        self.top_layout.setSpacing(10)
        self.top_layout.addStretch()
        self.top_layout.setAlignment(QtCore.Qt.AlignTop)
        self.top_widget.setLayout(self.top_layout)  # set top part layout.
        self.top_widget.setStyleSheet('''
            QWidget#top_widget{
                color:#232C51;
                background:#dddddd;
            }
        ''')

        self.left_widget = QtWidgets.QWidget()  # create left part.
        self.left_widget.setObjectName('left_widget')
        self.left_layout = QtWidgets.QGridLayout()  # create left part layout.
        self.left_widget.setLayout(self.left_layout)  # set left part layout.
        self.left_widget.setStyleSheet('''
            QWidget#left_widget{
                color:#232C51;
                background:#dddd00;
            }
        ''')

        self.top_close = QtWidgets.QPushButton('x')  # close window button.
        self.top_close.setFixedSize(25, 25)
        self.top_close.setStyleSheet('''
            QPushButton{
                background:#F76677;
                border-radius:5px;
                color:white;
                padding-bottom:2px;
            }
            QPushButton:hover{
                background:red;
            }
        ''')
        self.top_close.clicked.connect(self.top_close_clicked)
        self.top_maximize = QtWidgets.QPushButton('o')  # enlarge window button.
        self.top_maximize.setFixedSize(25, 25)
        self.top_maximize.setStyleSheet('''
            QPushButton{
                background:#6DDF6D;
                border-radius:5px;
                color:white;
                padding-bottom:2px;
            }
            QPushButton:hover{
                background:#5cce5a;
            }
        ''')
        self.top_maximize.clicked.connect(self.top_maximize_clicked)
        self.top_minimize = QtWidgets.QPushButton('-')  # minimize window button.
        self.top_minimize.setFixedSize(25, 25)
        self.top_minimize.setStyleSheet('''
            QPushButton{
                background:#ffef00;
                border-radius:5px;
                color:white;
                padding-bottom:2px;
            }
            QPushButton:hover{
                background:#efef00;
            }
        ''')
        self.top_minimize.clicked.connect(self.top_minimize_clicked)

        self.main_layout.addWidget(self.top_widget, 0, 10)  # 2 rows, 10 columns
        self.main_layout.addWidget(self.left_widget, 2, 5, 11, 3)
        self.setCentralWidget(self.main_widget)  # set main window's main widget.

        self.top_layout.addWidget(self.top_minimize)
        self.top_layout.addWidget(self.top_maximize)
        self.top_layout.addWidget(self.top_close)

    def top_close_clicked(self):
        time.sleep(0.3)
        self.close()

    def top_minimize_clicked(self):
        self.showMinimized()

    def top_maximize_clicked(self):
        print(self.pos())
        if self.is_maximized:
            self.resize(self.origin_size.width(), self.origin_size.height())
            self.move(self.position.x(), self.position.y())
        else:
            self.origin_size = self.size()
            self.showMaximized()
        self.position = self.pos()
        self.is_maximized = False if self.is_maximized else True


def main():
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

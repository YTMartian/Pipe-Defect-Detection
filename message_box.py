from PyQt5.QtWidgets import QWidget,QPushButton
from resources import *

class MessageBox(QWidget):
    def __init__(self):
        super(MessageBox, self).__init__()
        self.setWindowTitle('提示')
        self.setFixedSize(250,250)
        self.button=QPushButton()
        self.button.move(25,250)

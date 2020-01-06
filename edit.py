from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog


class Edit(QDialog):
    def __init__(self, db, mode, video_id=None, defect_id=None):
        super().__init__()
        self.is_edit_video = 0
        self.is_edit_defect = 1
        self.is_show_project_info = 2
        self.setWindowTitle('Pipe Defect Detection')
        self.setWindowIcon(QIcon(':/app_icon'))
        self.setMinimumSize(1280, 720)
        self.setStyleSheet('''
            Edit{
                background:white;
            }
        ''')
        self.db = db
        self.mode = mode
        self.setAutoFillBackground(True)
        self.main_widget = QtWidgets.QWidget()
        self.main_layout = QtWidgets.QGridLayout()  # create main window layout.
        self.main_layout.setSpacing(0)
        self.main_widget.setLayout(self.main_layout)
        self.main_widget.setStyleSheet('''
            QWidget{
                background:red;
            }
        ''')

        if self.mode == self.is_edit_video:
            self.edit_video(video_id)
        elif self.mode == self.is_edit_defect:
            self.edit_defect(defect_id)

    def edit_video(self, video_id):
        print('编辑视频 ', video_id)

    def edit_defect(self, defect_id):
        print('编辑缺陷 ', defect_id)

    def show_project_info(self):
        print('显示缺陷')

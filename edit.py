from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QScrollArea, QMainWindow, QHBoxLayout, QFormLayout, QLineEdit, \
    QComboBox


class Edit(QMainWindow):
    def __init__(self, db, mode, video_id=None, defect_id=None, main_window=None):
        super(Edit, self).__init__(main_window)

        self.is_edit_video = 0
        self.is_edit_defect = 1
        self.is_show_project_info = 2
        self.video_id = video_id
        self.defect_id = defect_id
        self.main_window = main_window
        self.setWindowTitle(self.main_window.settings.app_name)
        self.setWindowIcon(QIcon(':/app_icon'))
        self.setMinimumSize(1280, 720)
        self.setStyleSheet('''
            Edit{
                background:#f1f1f1;
            }
        ''')
        self.db = db
        self.mode = mode

        self.main_widget = QtWidgets.QWidget(self)  # must add widget to dialog.
        self.main_layout = QtWidgets.QGridLayout(self)
        self.main_layout.setSpacing(0)
        self.main_layout.setSpacing(0)
        self.main_widget.setLayout(self.main_layout)
        self.main_widget.setAutoFillBackground(True)

        self.left_widget = QtWidgets.QWidget(self)
        self.left_layout = QtWidgets.QGridLayout()

        self.left_widget.setLayout(self.left_layout)
        self.left_widget.setStyleSheet('''
            QWidget{
                background:#343434;
            }
        ''')
        self.right_widget = QtWidgets.QWidget(self)
        self.right_layout = QtWidgets.QGridLayout()
        self.right_layout.setSpacing(0)
        self.right_widget.setLayout(self.right_layout)
        self.right_widget.setFixedWidth(370)
        self.main_layout.addWidget(self.left_widget, 0, 0, 1, 2)
        self.main_layout.addWidget(self.right_widget, 0, 2, 1, 1)
        self.right_top_layout = QHBoxLayout()
        self.right_top_layout.setSpacing(5)
        self.right_top_layout.setContentsMargins(0, 0, 0, 10)
        self.right_top_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.edit_video_button = QPushButton()
        self.edit_video_button.setText('检测信息')
        self.edit_video_button.setIcon(QIcon(":/edit_video_button"))
        self.edit_video_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.edit_video_button.clicked.connect(self.edit_video_button_clicked)

        self.edit_defect_button = QPushButton()
        self.edit_defect_button.setText('缺陷记录')
        self.edit_defect_button.setIcon(QIcon(":/edit_defect_button"))
        self.edit_defect_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.edit_defect_button.clicked.connect(self.edit_defect_button_clicked)

        self.project_detailed_button = QPushButton()
        self.project_detailed_button.setText('工程详情')
        self.project_detailed_button.setIcon(QIcon(":/project_detailed_button"))
        self.project_detailed_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.project_detailed_button.clicked.connect(self.project_detailed_button_clicked)

        self.right_top_layout.addWidget(self.edit_video_button)
        self.right_top_layout.addWidget(self.edit_defect_button)
        self.right_top_layout.addWidget(self.project_detailed_button)
        self.right_top_widget = QtWidgets.QWidget()
        self.right_top_widget.setLayout(self.right_top_layout)
        self.right_layout.addWidget(self.right_top_widget, 0, 0, 1, 3)
        self.right_bottom_layout = QHBoxLayout()
        self.right_bottom_layout.setSpacing(5)
        self.right_bottom_layout.setContentsMargins(0, 10, 0, 0)
        self.right_bottom_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.save_button = QPushButton()
        self.save_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.save_button.setText('保存')
        self.save_button.setIcon(QIcon(":/save"))
        self.save_button.clicked.connect(self.save)
        self.save_button.setStyleSheet('''
            QPushButton{
                    font-weight:bold;
                    background-color:#434343;
                    color:#f1f1f1;
                    font-size:20px;
                    border-radius:10px;
                    font-family:"DengXian";
                    padding:10px 10px 10px 10px;
                }
                QPushButton:hover{
                    background-color:#131313;
                }
        ''')
        self.cancel_button = QPushButton()
        self.cancel_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.cancel_button.setText('取消')
        self.cancel_button.setIcon(QIcon(":/cancel"))
        self.cancel_button.clicked.connect(self.cancel)
        self.cancel_button.setStyleSheet('''
            QPushButton{
                    font-weight:bold;
                    background-color:#434343;
                    color:#f1f1f1;
                    font-size:20px;
                    border-radius:10px;
                    font-family:"DengXian";
                    padding:10px 10px 10px 10px;
                }
                QPushButton:hover{
                    background-color:#131313;
                }
        ''')
        self.right_bottom_layout.addWidget(self.save_button)
        self.right_bottom_layout.addWidget(self.cancel_button)
        self.right_bottom_widget = QtWidgets.QWidget()
        self.right_bottom_widget.setLayout(self.right_bottom_layout)
        self.right_layout.addWidget(self.right_bottom_widget, 22, 0, 1, 3)

        # scroll area.
        self.scroll_area_widget = QtWidgets.QWidget()
        self.scroll_area_widget.setStyleSheet('''
            QWidget{
                color:#232323;
                font-size:16px;
                font-family:"Microsoft YaHei";
            }
        ''')
        self.setCentralWidget(self.main_widget)
        self.scroll_area_form = QFormLayout()
        self.labels = [QLabel() for i in range(39)]
        self.buttons = [QComboBox() for i in range(39)]
        for i in range(len(self.labels)):
            self.labels[i].setText("标签" + str(i))
            self.scroll_area_form.addRow(self.labels[i], self.buttons[i])
        self.scroll_area_widget.setLayout(self.scroll_area_form)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.scroll_area_widget)
        self.right_layout.addWidget(self.scroll_area, 2, 0, 20, 3)

        self.set_three_buttons_style()
        self.hide_something()

    def save(self):
        if self.mode == self.is_edit_video:
            print('保存视频信息')
        elif self.mode == self.is_edit_defect:
            print('保存缺陷')

    def cancel(self):
        if self.mode == self.is_edit_video:
            print('取消保存视频信息')
        elif self.mode == self.is_edit_defect:
            print('取消保存缺陷')

    def hide_something(self):
        if self.mode == self.is_show_project_info:
            self.save_button.setVisible(False)
            self.cancel_button.setVisible(False)
        else:
            self.save_button.setVisible(True)
            self.cancel_button.setVisible(True)

    def edit_video_button_clicked(self):
        self.mode = self.is_edit_video
        self.set_three_buttons_style()
        self.hide_something()

    def edit_defect_button_clicked(self):
        self.mode = self.is_edit_defect
        self.set_three_buttons_style()
        self.hide_something()

    def project_detailed_button_clicked(self):
        self.mode = self.is_show_project_info
        self.set_three_buttons_style()
        self.hide_something()

    # set edit_video_button,edit_defect_button and project_detailed_button's style.
    def set_three_buttons_style(self):
        self.edit_video_button.setStyleSheet('''
            QPushButton{
                    font-weight:bold;
                    background-color:#535353;
                    color:#f1f1f1;
                    font-size:16px;
                    border-radius:10px;
                    font-family:"Microsoft YaHei";
                    padding:10px 10px 10px 10px;
                }
                QPushButton:hover{
                    background-color:#131313;
                }
        ''')
        self.edit_defect_button.setStyleSheet('''
            QPushButton{
                    font-weight:bold;
                    background-color:#535353;
                    color:#f1f1f1;
                    font-size:16px;
                    border-radius:10px;
                    font-family:"Microsoft YaHei";
                    padding:10px 10px 10px 10px;
                }
                QPushButton:hover{
                    background-color:#131313;
                }
        ''')
        self.project_detailed_button.setStyleSheet('''
            QPushButton{
                    font-weight:bold;
                    background-color:#535353;
                    color:#f1f1f1;
                    font-size:16px;
                    border-radius:10px;
                    font-family:"Microsoft YaHei";
                    padding:10px 10px 10px 10px;
                }
                QPushButton:hover{
                    background-color:#131313;
                }
        ''')
        if self.mode == self.is_edit_video:
            self.edit_video_button.setStyleSheet('''
                QPushButton{
                        font-weight:bold;
                        background-color:#131313;
                        color:#f1f1f1;
                        font-size:16px;
                        border-radius:10px;
                        font-family:"Microsoft YaHei";
                        padding:10px 10px 10px 10px;
                    }
            ''')
        elif self.mode == self.is_edit_defect:
            self.edit_defect_button.setStyleSheet('''
                QPushButton{
                        font-weight:bold;
                        background-color:#131313;
                        color:#f1f1f1;
                        font-size:16px;
                        border-radius:10px;
                        font-family:"Microsoft YaHei";
                        padding:10px 10px 10px 10px;
                    }
            ''')
        elif self.mode == self.is_show_project_info:
            self.project_detailed_button.setStyleSheet('''
                QPushButton{
                        font-weight:bold;
                        background-color:#131313;
                        color:#f1f1f1;
                        font-size:16px;
                        border-radius:10px;
                        font-family:"Microsoft YaHei";
                        padding:10px 10px 10px 10px;
                    }
            ''')

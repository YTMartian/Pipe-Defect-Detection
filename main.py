import operator

from PyQt5.QtCore import QDate, QUrl, QPoint
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QMainWindow, QGraphicsDropShadowEffect, QLabel, QPushButton, QApplication, QLineEdit, \
    QListView, QHBoxLayout, QRadioButton, QTableWidget, QHeaderView, QTableWidgetItem, QAbstractItemView, QMenu, \
    QComboBox, QCalendarWidget, QDateEdit, QMessageBox
from PyQt5.QtGui import QIcon, QColor, QCursor, QPixmap, QBrush, QIntValidator
from tkinter import filedialog
from PyQt5 import QtWidgets
from torch.autograd import Variable
from mobilenetv2_1 import MobileNetV2_1
from torchvision import transforms
from utils.datasets import *
from utils.utils import *
from PyQt5 import QtGui
from resources import *
from database import *
from tkinter import *
from models import *
from staff import *
from edit import *
from word import *
from PIL import Image
import torchvision
import threading
import datetime
import settings
import torch
import time
import sys
import os

'''
MORE QSS STYLE SEE:https://github.com/ColinDuquesnoy/QDarkStyleSheet/blob/master/qdarkstyle/style.qss
'''


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.settings = settings.Settings()
        self.setWindowTitle(self.settings.app_name)
        self.setWindowIcon(QIcon(':/app_icon'))
        self.setMinimumSize(1280, 720)

        self.db = Database()
        self.word = Word(self.db)
        self.data = []
        self.is_add_project = False
        self.is_edit_project = False
        self.edit_project_id = None
        self.is_edit_video = 0
        self.is_edit_defect = 1

        # DEBUG.
        # edit = Edit(self.db, self.is_edit_video, video_id=53, main_window=self)
        # edit.show()

        # staff = Staff(db=self.db, main_window=self)
        # staff.show()

        # load two models.
        # 0 is abnormal and 1 is normal.
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize((.5, .5, .5), (.5, .5, .5)),
        ])
        self.two_classes_model = MobileNetV2_1(num_classes=2).cuda()
        self.two_classes_model.load_state_dict(torch.load('model/mobilenetv2_1.weight'))
        self.two_classes_model.eval().cuda()

        # load yolov3 model.
        self.img_size = 416
        yolo = 'yolov3-tiny'
        weights = 'model/{}.pt'.format(yolo)
        cfg = 'model/{}.cfg'.format(yolo)
        self.names = 'model/my.names'
        # Initialize model
        self.yolov3_model = Darknet(cfg, self.img_size)

        # Load weights
        attempt_download(weights)
        self.yolov3_model.load_state_dict(torch.load(weights, map_location='cuda:0')['model'])

        # Eval mode
        self.yolov3_model.eval().cuda()

        # Get names and colors
        self.names = load_classes(self.names)
        self.colors = [[random.randint(0, 255) for _ in range(3)] for _ in range(len(self.names))]

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
        self.is_searching = False
        self.sort_order = QtCore.Qt.DescendingOrder

        self.main_widget = QtWidgets.QWidget()  # main window.
        background = QtGui.QPalette()
        if os.path.exists(self.settings.background_image) and str(
                os.path.splitext(self.settings.background_image)[1]).lower() in ['.jpg', '.png']:
            background.setBrush(self.main_widget.backgroundRole(), QBrush(QPixmap(self.settings.background_image)))
        else:
            background.setBrush(self.main_widget.backgroundRole(), QBrush(QPixmap(':/background')))
        self.main_widget.setAutoFillBackground(True)  # in this way the widget would not be transparent.
        self.main_widget.setPalette(background)
        self.main_layout = QtWidgets.QGridLayout()  # create main window layout.
        self.main_layout.setSpacing(0)  # the spacing between two widgets in the layout.
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
        self.left_widget.setObjectName('left_widget')  # object name is the name in qss.
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

        self.top_close = QPushButton()  # close window button.
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
        self.top_maximize = QPushButton()  # enlarge window button.
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
        self.top_minimize = QPushButton()  # minimize window button.
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
        self.top_settings = QPushButton()
        self.top_settings.setFixedSize(25, 25)
        self.top_settings.setToolTip('设置')
        self.top_settings.setCursor(QCursor(QtCore.Qt.PointingHandCursor))  # set cursor when hover.
        self.top_settings.setStyleSheet('''
            QPushButton{
                background-color:transparent;
                border-radius:5px;
                color:white;
                background-image:url(:/settings);
            }
            QPushButton:hover{
                background-image:url(:/settings_hover);
                background-repeat:no-repeat center
            }
        ''')
        self.top_settings.clicked.connect(self.change_settings)

        self.manage_layout = QtWidgets.QGridLayout()
        self.manage_layout.setContentsMargins(10, 10, 10, 10)
        self.manage_widget = QtWidgets.QWidget()  # create manage part.
        self.manage_widget.setObjectName('manage_widget')
        self.manage_widget.setLayout(self.manage_layout)

        self.main_layout.addWidget(self.top_widget, 1, 0, 1, 15)  # start from (x1,y1) and occupy (x2,y2)
        self.main_layout.addWidget(self.left_widget, 1, 0, 12, 2)
        self.main_layout.addWidget(self.manage_widget, 2, 2, 11, 13)
        self.setCentralWidget(self.main_widget)  # set main window's main widget.

        self.top_layout.addWidget(self.top_settings)
        self.top_layout.addWidget(self.top_minimize)
        self.top_layout.addWidget(self.top_maximize)
        self.top_layout.addWidget(self.top_close)

        self.app = QLabel()
        self.app.setPixmap(QPixmap(':/app'))
        self.app.setContentsMargins(0, 20, 0, 0)
        self.left_layout.addWidget(self.app, 1, 0, 10, 10, QtCore.Qt.AlignTop)
        self.managements = [QPushButton() for i in range(4)]
        self.managements[0].setText('工程管理')
        self.managements[1].setText('视频管理')
        self.managements[2].setText('缺陷管理')
        self.managements[3].setText('即时检测')
        self.managements[0].setIcon(QIcon(":/project_management"))  # add icon before text.
        self.managements[1].setIcon(QIcon(":/video_management"))
        self.managements[2].setIcon(QIcon(":/defect_management"))
        self.managements[3].setIcon(QIcon(":/robot"))
        for i in range(4):
            self.managements[i].setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.set_managements_style()
        self.managements[0].clicked.connect(self.all_managements)
        self.managements[1].clicked.connect(self.all_managements)
        self.managements[2].clicked.connect(self.all_managements)
        self.managements[3].clicked.connect(self.all_managements)
        self.left_layout.addWidget(self.managements[0], 3, 5, 1, 1, QtCore.Qt.AlignCenter)
        self.left_layout.addWidget(self.managements[1], 4, 5, 1, 1, QtCore.Qt.AlignCenter)
        self.left_layout.addWidget(self.managements[2], 5, 5, 1, 1, QtCore.Qt.AlignCenter)
        self.left_layout.addWidget(self.managements[3], 6, 5, 1, 1, QtCore.Qt.AlignCenter)
        self.management_flag = 0
        self.project_management_flag = 1
        self.video_management_flag = 2
        self.defect_management_flag = 3
        self.robot_flag = 4

        self.search_input = QLineEdit()
        self.search_input.setToolTip('输入关键字搜索')
        self.search_input.setMaximumWidth(300)
        self.search_input.setMaximumHeight(35)
        self.search_input.setStyleSheet('''
            QLineEdit{
                color:rgba(255,255,255,0.9);
                font-weight:bold;
                background-color:rgba(220,220,220,0.3);
                selection-color:#232323;
                selection-background-color:#F79F1E;
                border-radius:10px;
                font-family:"DengXian";
                font-size:20px;
            }
        ''')
        self.search_input.setPlaceholderText('搜索关键字...')
        self.search_button = QPushButton()
        self.search_button.setFixedSize(30, 30)
        self.search_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.search_button.setStyleSheet('''
            QPushButton{
                border-radius:5px;
                background-image:url(:/search);
            }
            QPushButton:hover{
                background-image:url(:/search_hover);
                background-repeat:no-repeat center
            }
        ''')
        # first add the two widget into a QHBoxLayout and then add the layout to another layout.
        self.search_field = QHBoxLayout()
        self.search_field.addWidget(self.search_input)
        self.search_field.addWidget(self.search_button)
        self.search_field.addStretch()
        self.search_field.setAlignment(QtCore.Qt.AlignTop)
        self.search_field_widget = QtWidgets.QWidget()
        self.search_field_widget.setLayout(self.search_field)
        self.manage_layout.addWidget(self.search_field_widget, 0, 5, 1, 1)
        self.search_button.clicked.connect(self.search)
        self.search_input.returnPressed.connect(self.search)  # press Enter.

        # toggle project detailed view and statistic view.
        self.toggle_project_field = QHBoxLayout()
        self.toggle_project_field.addStretch()
        self.toggle_project_field.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        self.toggle_project_widget = QtWidgets.QWidget()
        self.toggle_project_widget.setLayout(self.toggle_project_field)
        self.toggle_project_detailed_view = QRadioButton('工程详细')
        self.toggle_project_detailed_view.setChecked(True)
        self.toggle_project_detailed_view.toggled.connect(self.toggle_project_view)
        self.toggle_project_statistic_view = QRadioButton('工程统计')
        self.toggle_project_statistic_view.setChecked(False)
        self.toggle_project_statistic_view.toggled.connect(self.toggle_project_view)
        self.toggle_project_widget.setStyleSheet('''
            QWidget{
                font-family:"DengXian";
                font-size:18px;
                font-weight:bold;
                color:#f1f1f1;
        }''')
        self.toggle_project_detailed_view.setStyleSheet('''
            QRadioButton::indicator:checked {
                background-color: rgba(0,220,0,0.9);
                border-radius:7px;
                border:2px solid white;
            }
            QRadioButton::indicator:unchecked {
                background-color: white;
                border-radius:7px;
                border:2px solid white;
        }''')
        self.toggle_project_statistic_view.setStyleSheet('''
            QRadioButton::indicator:checked {
                background-color: rgba(0,220,0,0.9);
                border-radius:7px;
                border:2px solid white;
            }
            QRadioButton::indicator:unchecked {
                background-color: white;
                border-radius:7px;
                border:2px solid white;
        }''')

        self.ensure_button = QPushButton()
        self.ensure_button.setFixedSize(32, 32)
        self.ensure_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.ensure_button.setStyleSheet('''
            QPushButton{
                border-radius:5px;
                background-image:url(:/ensure);
            }
            QPushButton:hover{
                background-image:url(:/ensure_hover);
                background-repeat:no-repeat center
            }
        ''')
        self.ensure_button.clicked.connect(self.ensure_add_project)
        self.cancel_button = QPushButton()
        self.cancel_button.setFixedSize(32, 32)
        self.cancel_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.cancel_button.setStyleSheet('''
            QPushButton{
                border-radius:5px;
                background-image:url(:/cancel);
            }
            QPushButton:hover{
                background-image:url(:/cancel_hover);
                background-repeat:no-repeat center
            }
        ''')
        self.number_of_per_page = 12
        self.current_page = 1
        self.cancel_button.clicked.connect(self.cancel_add_project)
        self.start_time = QDateEdit()
        self.start_time.setCalendarPopup(True)
        self.start_time.setDate(QDate(2020, 1, 1))
        self.start_time.setStyleSheet('''
            QDateEdit {
                border: 2px solid lightgray;
                border-radius: 5px;
                color:#232323;
            }
            
            QTableView{
                background:#ffffff;
                color:#232323;
            }
            
            QDateTimeEdit{
                background:#ffffff;
                color:#232323;
            }
           
            QDateEdit::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 15px;
                border-left-width: 1px;
                border-left-color: darkgray;
                border-left-style: solid;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
            }
             
            QDateEdit::down-arrow {
                image: url(:/drop_down);
            }
        ''')
        self.start_time.dateChanged.connect(self.date_changed)
        self.end_time = QDateEdit()
        self.end_time.setCalendarPopup(True)
        self.end_time.setDate(QDate.currentDate())
        self.end_time.setStyleSheet('''
            QDateEdit {
                border: 2px solid lightgray;
                border-radius: 5px;
                color:#232323;
            }
            
            QTableView{
                background:#ffffff;
                color:#232323;
            }
            
            QDateTimeEdit{
                background:#ffffff;
                color:#232323;
            }
             
            QDateEdit::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 15px;
                border-left-width: 1px;
                border-left-color: darkgray;
                border-left-style: solid;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
            }
             
            QDateEdit::down-arrow {
                image: url(:/drop_down);
            }
        ''')
        self.end_time.dateChanged.connect(self.date_changed)
        self.previous_page = QPushButton()
        self.previous_page.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.previous_page.setIcon(QIcon(":/previous"))
        self.previous_page.clicked.connect(self.previous_table_page)
        self.previous_page.setStyleSheet('''
            QPushButton{
                    font-weight:bold;
                    color:#f1f1f1;
                    font-size:20px;
                    border-radius:5px;
                    font-family:"DengXian";
                    padding:5px 5px 5px 5px;
                }
                QPushButton:hover{
                    background-color:rgba(200,200,200,0.2);
                }
        ''')
        self.next_page = QPushButton()
        self.next_page.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.next_page.setIcon(QIcon(":/next"))
        self.next_page.clicked.connect(self.next_table_page)
        self.next_page.setStyleSheet('''
            QPushButton{
                    font-weight:bold;
                    color:#f1f1f1;
                    font-size:20px;
                    border-radius:5px;
                    font-family:"DengXian";
                    padding:5px 5px 5px 5px;
                }
                QPushButton:hover{
                    background-color:rgba(200,200,200,0.2);
                }
        ''')
        self.page_number = QLineEdit()
        self.page_number.setFixedWidth(40)
        self.page_number.setAlignment(QtCore.Qt.AlignRight)
        self.page_number.setStyleSheet('''
            QLineEdit{
                background:transparent;
                border:none;
                font-weight:bold;
                font-size:20px;
                color:#eeeeee;
                text-align:center;
                border-bottom:3px dotted #0eee8f;
            }
        ''')
        self.page_number.setText('1')
        self.page_number.setValidator(QIntValidator())  # only accept digits.
        self.total_page_number = QLineEdit()
        self.total_page_number.setFixedWidth(40)
        self.total_page_number.setAlignment(QtCore.Qt.AlignLeft)
        self.total_page_number.setEnabled(False)
        self.total_page_number.setStyleSheet('''
            QLineEdit{
                background:transparent;
                border:none;
                font-weight:bold;
                font-size:20px;
                color:#eeeeee;
                text-align:center;
                border-bottom:3px dotted #dd6572;
            }
        ''')
        self.goto_page = QPushButton()
        self.goto_page.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.goto_page.setIcon(QIcon(":/go"))
        self.goto_page.setFixedSize(30, 30)
        self.goto_page.clicked.connect(self.goto_table_page)
        self.goto_page.setStyleSheet('''
            QPushButton{
                font-weight:bold;
                color:#f1f1f1;
                font-size:20px;
                border-radius:5px;
                font-family:"DengXian";
                padding:5px 5px 5px 5px;
            }
            QPushButton:hover{
                background-color:rgba(200,200,200,0.2);
            }
        ''')
        self.toggle_project_field.addWidget(self.start_time)
        self.toggle_project_field.addWidget(self.end_time)
        self.toggle_project_field.addWidget(self.previous_page)
        self.toggle_project_field.addWidget(self.page_number)
        self.toggle_project_field.addWidget(self.total_page_number)
        self.toggle_project_field.addWidget(self.next_page)
        self.toggle_project_field.addWidget(self.goto_page)
        self.toggle_project_field.addWidget(self.ensure_button)
        self.toggle_project_field.addWidget(self.cancel_button)
        self.toggle_project_field.addWidget(self.toggle_project_detailed_view)
        self.toggle_project_field.addWidget(self.toggle_project_statistic_view)
        self.manage_layout.addWidget(self.toggle_project_widget, 3, 5, 10, 1)

        # show table.
        # settings in:https://blog.csdn.net/yekui006/article/details/98211808
        # very useful functions:https://likegeeks.com/pyqt5-tutorial/#Make-QTableWidget-not-editable-read-only
        self.show_table = QTableWidget()

        self.show_table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        # self.show_table.horizontalHeader().setVisible(False)
        self.show_table.verticalHeader().setVisible(True)  # hide teh header.
        self.show_table.horizontalHeader().setStretchLastSection(True)
        self.show_table.setShowGrid(True)
        self.manage_layout.addWidget(self.show_table, 4, 2, 10, 10)
        self.show_table.setCornerButtonEnabled(False)  # set the top-left corner.
        # self.show_table.horizontalHeader().setSectionsClickable(False)
        self.show_table.verticalHeader().setSectionsClickable(False)
        self.show_table.setStyleSheet('''
            QWidget{
                background:white;
                font-family:"DengXian";
                font-size:18px;
                font-weight:bold;
                color:#232323;
                selection-background-color:#8aA0A9;
                selection-color:#ffffff;
                border:none;
            }
            QTableView QTableCornerButton::section {
                background-color:#364A5F;
            }
        ''')
        # change header style:should add ::section.
        self.show_table.horizontalHeader().setStyleSheet('''
        QTableView QHeaderView{	
                background-color:#363A5F;
                font-size:20px;
                height:30px;
                font-weight:bold;
                color:#FFFFFF;
            }
            QTableView QHeaderView::section{	
                background-color:#363A5F;
                font-size:20px;
                height:30px;
                font-weight:bold;
                color:#FFFFFF;
            }
}       ''')
        self.show_table.verticalHeader().setStyleSheet('''
            QTableView QHeaderView::section{	
                background-color:#364A5F;
                font-size:20px;
                width:30px;
                font-weight:bold;
                color:#FFFFFF;
            }
        ''')
        # set the column width auto to fix window width.
        # https://blog.csdn.net/yl_best/article/details/84070231
        self.show_table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive | QHeaderView.Stretch)
        self.show_table.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignLeft)
        self.show_table.horizontalHeader().setStretchLastSection(True)
        self.show_table.verticalHeader().setDefaultSectionSize(60)  # set row margin.
        self.show_table.resizeRowsToContents()
        self.show_table.setWordWrap(False)
        # if choose one grid. then choose the whole row.
        self.show_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.show_table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # set can't edit.
        self.show_table.setSelectionMode(QAbstractItemView.SingleSelection)  # can only select one line.

        # all of the add project widgets.
        self.add_project_widgets = []
        # all of the ids and names in  ComboBox, e.g. the staff_id and staff_name.
        self.add_project_tables = []  # table: staff,detection,move,plugging,drainage,dredging.

        self.browser = QWebEngineView()
        self.manage_layout.addWidget(self.browser, 3, 2, 10, 10)

        self.hide_all()
        # to get the clicked column number.
        self.show_table.horizontalHeader().sectionClicked[int].connect(self.sort_table)

    def __del__(self):
        self.top_close_clicked()

    def yolov3_detect(self, img0):
        # Padded resize
        img = letterbox(img0, new_shape=self.img_size)[0]

        # Convert
        img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
        img = np.ascontiguousarray(img, dtype=np.float32)  # uint8 to fp16/fp32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0

        # Get detections
        img = torch.from_numpy(img).cuda()
        if img.ndimension() == 3:
            img = img.unsqueeze(0)
        pred = self.yolov3_model(img)[0]

        # Apply NMS
        pred = non_max_suppression(pred, conf_thres=0.3)
        count = 0

        # Process detections
        for i, det in enumerate(pred):  # detections per image

            s = '%gx%g ' % img.shape[2:]  # print string
            if det is not None and len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], img0.shape).round()

                # Print results
                for c in det[:, -1].unique():
                    n = (det[:, -1] == c).sum()  # detections per class
                    s += '%g %ss, ' % (n, self.names[int(c)])  # add to string

                # Write results
                for *xyxy, conf, cls in det:
                    label = '%s %.2f' % (self.names[int(cls)], conf)
                    plot_one_box(xyxy, img0, label=label, color=self.colors[int(cls)])
                    count += 1
        return img0, count

    @staticmethod
    def top_close_clicked():
        # use command to kill the django server process and the main window
        # or the software will be stuck.
        result = os.popen('tasklist | findstr python')
        res = result.read()
        for line in res.splitlines():
            line = line.split()
            pid = line[1]
            _ = os.popen('taskkill /pid {} /f'.format(pid))
            print(_)
        exit(0)

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
                if self.move_position is None:
                    self.move_position = event.globalPos()
                    if self.move_position.x() > QApplication.desktop().width() // 2:
                        self.move_position = QtCore.QPoint(self.move_position.x() - QApplication.desktop().width() // 2,
                                                           self.move_position.y())
                # print(event.globalPos().x(), "---", self.move_position.x())
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

    def change_settings(self):
        context_menu = QMenu(self)
        context_menu.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        context_menu.setStyleSheet('''
            QMenu{
                background:rgba(20,20,20,0.8);
                font-weight:bold;
                font-size:17px;
                color:#d6d6d6;
                padding-top:10px;
                border-radius:30px;
                font-family:"Microsoft YaHei";
            }
            QMenu::item::selected{
                color:#f1f1f1;
            }
        ''')
        skin_management = context_menu.addAction("更换皮肤")
        staff_management = context_menu.addAction("人员管理")
        action = context_menu.exec_(
            self.mapToGlobal(QPoint(self.top_settings.pos().x() + 10, self.top_settings.pos().y() + 10)))
        if action == skin_management:
            flag = self.settings.change_background()
            if not flag:
                return
            background = QtGui.QPalette()
            background.setBrush(self.main_widget.backgroundRole(), QBrush(QPixmap(self.settings.background_image)))
            self.main_widget.setPalette(background)
        elif action == staff_management:
            staff = Staff(db=self.db, main_window=self)
            staff.show()

    def set_managements_style(self):
        for i in range(4):
            self.managements[i].setStyleSheet('''
                QPushButton{
                    font-weight:bold;
                    color:#f1f1f1;
                    font-size:20px;
                    border-radius:5px;
                    font-family:"DengXian";
                    padding:10px 10px 10px 10px;
                }
                QPushButton:hover{
                    background-color:rgba(200,200,200,0.2);
                }
            ''')

    def all_managements(self):
        sender = self.sender()
        self.set_managements_style()
        self.current_page = 1
        self.page_number.setText(str(self.current_page))
        sender.setStyleSheet('''
            QPushButton{
                background-color:rgba(200,200,200,0.3);
                font-weight:bold;
                color:#f1f1f1;
                font-size:20px;
                border-radius:5px;
                font-family:"DengXian";
                padding:10px 10px 10px 10px;
            }
        ''')
        if sender == self.managements[0]:
            self.management_flag = self.project_management_flag
            self.project_management()
        elif sender == self.managements[1]:
            self.management_flag = self.video_management_flag
            self.video_management(None)
        elif sender == self.managements[2]:
            self.management_flag = self.defect_management_flag
            self.defect_management(None)
        elif sender == self.managements[3]:
            self.management_flag = self.robot_flag
            self.robot_management()

    def project_management(self):
        self.hide_all()
        self.search_button.setVisible(True)
        self.search_input.setVisible(True)
        self.search_input.setPlaceholderText('搜索工程...')
        self.toggle_project_statistic_view.setVisible(True)
        self.toggle_project_detailed_view.setVisible(True)
        self.show_table.setVisible(True)
        self.toggle_project_view()
        self.start_time.setVisible(True)
        self.end_time.setVisible(True)
        self.page_number.setVisible(True)
        self.total_page_number.setVisible(True)
        self.previous_page.setVisible(True)
        self.next_page.setVisible(True)
        self.goto_page.setVisible(True)

    def video_management(self, project_id):
        self.hide_all()
        self.start_time.setVisible(True)
        self.end_time.setVisible(True)
        self.page_number.setVisible(True)
        self.total_page_number.setVisible(True)
        self.previous_page.setVisible(True)
        self.next_page.setVisible(True)
        self.goto_page.setVisible(True)
        # self.search_button.setVisible(True)
        # self.search_input.setVisible(True)
        self.search_input.setPlaceholderText('搜索视频...')
        self.show_table.setVisible(True)
        self.show_table.setColumnCount(8)
        self.show_table.setHorizontalHeaderLabels(
            ('道路名称', '管道编号', '管道类型', '管道材质', '视频文件', '视频日期', '导入日期', '判读数量'))
        self.resize_table_size_to_contents()
        self.data = self.db.get_video(project_id, time_flag=True, start_time=self.start_time.text(),
                                      end_time=self.end_time.text() + ' 23:59:59')
        self.insert_data_to_table()

    def defect_management(self, video_id):
        self.hide_all()
        self.start_time.setVisible(True)
        self.end_time.setVisible(True)
        self.page_number.setVisible(True)
        self.total_page_number.setVisible(True)
        self.previous_page.setVisible(True)
        self.next_page.setVisible(True)
        self.goto_page.setVisible(True)
        # self.search_button.setVisible(True)
        # self.search_input.setVisible(True)
        self.search_input.setPlaceholderText('搜索缺陷...')
        self.show_table.setVisible(True)
        self.show_table.setColumnCount(11)
        self.show_table.setHorizontalHeaderLabels(
            ('道路名称', '管道编号', '管道类型', '管道材质', '管径(mm)', '缺陷名称', '等级', '缺陷性质', '缺陷位置/帧', '检测日期', '判读日期'))
        self.resize_table_size_to_contents()
        self.data = self.db.get_defect(video_id, time_flag=True, start_time=self.start_time.text(),
                                       end_time=self.end_time.text() + ' 23:59:59')
        self.insert_data_to_table()

    def robot_management(self):
        self.hide_all()
        self.browser.setVisible(True)
        self.browser.load(QUrl('http://127.0.0.1:8000/'))
        self.browser.show()
        if not self.isMaximized():
            self.top_maximize_clicked()

    def hide_all(self):
        self.toggle_project_statistic_view.setVisible(False)
        self.toggle_project_detailed_view.setVisible(False)
        self.ensure_button.setVisible(False)
        self.cancel_button.setVisible(False)
        self.show_table.setVisible(False)
        self.search_input.setVisible(False)
        self.search_button.setVisible(False)
        self.browser.setVisible(False)
        self.browser.load(QUrl(''))
        self.start_time.setVisible(False)
        self.end_time.setVisible(False)
        self.page_number.setVisible(False)
        self.total_page_number.setVisible(False)
        self.previous_page.setVisible(False)
        self.next_page.setVisible(False)
        self.goto_page.setVisible(False)

    def search(self):
        search_text = self.search_input.text()
        if len(search_text) == 0:
            QtWidgets.QMessageBox.information(self, '提示', '输入为空')
            return
        if self.management_flag == self.project_management_flag:  # search in project.
            self.is_searching = True
            self.toggle_project_view()
        elif self.management_flag == self.video_management_flag:  # search in video.
            pass
        elif self.management_flag == self.defect_management_flag:  # search in defect.
            pass
        else:  # search in all.
            pass

    def sort_table(self, column):
        if self.sort_order == QtCore.Qt.AscendingOrder:
            self.sort_order = QtCore.Qt.DescendingOrder
        else:
            self.sort_order = QtCore.Qt.AscendingOrder
        self.data.sort(key=operator.itemgetter(column + 1), reverse=self.sort_order == QtCore.Qt.AscendingOrder)
        self.insert_data_to_table()
        # if self.management_flag == self.project_management_flag:
        #     if self.toggle_project_detailed_view.isChecked():
        #         if column <= 5:
        #             # it sort as string not integer
        #             self.show_table.sortItems(column, self.sort_order)
        #     else:
        #         self.show_table.sortItems(column, self.sort_order)
        # elif self.management_flag == self.video_management_flag:
        #     self.show_table.sortItems(column, self.sort_order)
        # elif self.management_flag == self.defect_management_flag:
        #     self.show_table.sortItems(column, self.sort_order)

    def toggle_project_view(self):
        self.ensure_button.setVisible(False)
        self.cancel_button.setVisible(False)
        self.is_add_project = False
        if self.toggle_project_detailed_view.isChecked():
            self.show_table.setColumnCount(16)
            self.show_table.setHorizontalHeaderLabels((
                '工程编号', '工程名称', '工程地址', '负责人员', '开工日期', '报告编号', '委托单位', '建设单位', '设计单位',
                '施工单位', '监理单位', '检测类型', '移动方式', '封堵方式', '排水方式', '清疏方式'))
            self.resize_table_size_to_contents()
            if self.is_searching:
                self.data = self.db.get_project_detailed(self.search_input.text(), time_flag=True,
                                                         start_time=self.start_time.text(),
                                                         end_time=self.end_time.text() + ' 23:59:59')
            else:
                self.data = self.db.get_project_detailed(time_flag=True, start_time=self.start_time.text(),
                                                         end_time=self.end_time.text() + ' 23:59:59')
            self.is_searching = False
            self.insert_data_to_table()
        else:
            self.show_table.setColumnCount(10)
            self.show_table.setHorizontalHeaderLabels(
                ('工程编号', '工程名称', '工程地址', '负责人员', '开工日期', '视频总数', '管道总数', '里程(KM)', '标内判读', '判读总数'))
            self.resize_table_size_to_contents()
            if self.is_searching:
                self.data = self.db.get_project_statistic(self.search_input.text(), time_flag=True,
                                                          start_time=self.start_time.text(),
                                                          end_time=self.end_time.text() + ' 23:59:59')
            else:
                self.data = self.db.get_project_statistic(time_flag=True, start_time=self.start_time.text(),
                                                          end_time=self.end_time.text() + ' 23:59:59')
            self.is_searching = False
            self.insert_data_to_table()

    def resize_table_size_to_contents(self):
        length = self.show_table.columnCount()
        for i in range(length):
            self.show_table.horizontalHeader().resizeSection(i, QHeaderView.ResizeToContents)

    def insert_data_to_table(self):
        total_page_number = (len(self.data) + self.number_of_per_page - 1) // self.number_of_per_page
        self.total_page_number.setText('/ ' + str(total_page_number))
        self.show_table.setRowCount(0)
        self.show_table.setRowCount(self.number_of_per_page)
        count = 0
        start_number = self.number_of_per_page * (self.current_page - 1)
        for row in range(start_number, len(self.data)):
            if count == self.number_of_per_page:
                break
            # the first item is id, we will use it to determine which row we choose to find it in database.
            data = self.data[row]
            if self.management_flag == self.defect_management_flag:
                data = data[:-2]  # because there is more items than the table column.
            for column in range(1, len(data)):

                try:
                    cell = MyTableWidgetItem()
                    try:
                        # to sort the integer.
                        # if this data is integer...
                        d = int(self.data[row][column])
                        cell.setData(QtCore.Qt.EditRole, d)
                    except:
                        cell.setData(QtCore.Qt.EditRole, self.data[row][column])
                    # so, in this way, when hover the mouse it will show the whole text.
                    # fantastic.
                    cell.setToolTip(str(self.data[row][column]))
                    self.show_table.setItem(row - start_number, column - 1, cell)
                except:
                    pass
            count += 1

    # right click menu.
    def contextMenuEvent(self, event):
        if self.is_add_project:
            return
        # get current selected row number, start from 0.
        current_row_number = self.show_table.currentRow()
        context_menu = QMenu(self)
        context_menu.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        context_menu.setStyleSheet('''
            QMenu{
                background:rgba(20,20,20,0.8);
                font-weight:bold;
                font-size:17px;
                color:#d6d6d6;
                padding-top:10px;
                border-radius:30px;
                font-family:"Microsoft YaHei";
            }
            QMenu::item::selected{
                color:#f1f1f1;
            }
        ''')
        if self.management_flag == self.project_management_flag:
            video_management = ''
            add_project = ''
            edit_project = ''
            delete_project = ''
            generate_document = ''
            add_video = ''
            if current_row_number != -1:  # if select one row.
                video_management = context_menu.addAction("视频管理")
            # can only do these in detailed project view.
            if self.toggle_project_detailed_view.isChecked():
                add_project = context_menu.addAction("添加工程")
                if current_row_number != -1:  # if select one row.
                    edit_project = context_menu.addAction("编辑工程")
            if current_row_number != -1:  # if select one row.
                delete_project = context_menu.addAction("删除工程")
                generate_document = context_menu.addAction("生成报告")
                add_video = context_menu.addAction("添加视频")
            action = context_menu.exec_(self.mapToGlobal(event.pos()))
            if action == video_management:
                self.management_flag = self.video_management_flag
                self.set_managements_style()
                self.set_single_management_style(1)
                self.video_management(self.data[current_row_number][0])  # get current project_id's videos.
            elif action == add_project:
                self.add_project()
            elif action == edit_project:
                self.add_project(current_row_number)
            elif action == delete_project:
                self.delete_project(self.data[current_row_number][0])
            elif action == generate_document:
                self.generate_report(self.data[current_row_number][0])
            elif action == add_video:
                self.add_video(self.data[current_row_number][0])
        elif self.management_flag == self.video_management_flag:
            defect_management = ''
            add_defect = ''
            edit_video = ''
            delete_video = ''
            if current_row_number != -1:  # if select one row.
                defect_management = context_menu.addAction("缺陷管理")
                edit_video = context_menu.addAction("检测信息")
                delete_video = context_menu.addAction("删除视频")
            action = context_menu.exec_(self.mapToGlobal(event.pos()))
            if action == defect_management:
                self.management_flag = self.defect_management_flag
                self.set_managements_style()
                self.set_single_management_style(2)
                self.defect_management(self.data[current_row_number][0])  # video_id
            elif action == edit_video:
                # open another dialog.
                edit = Edit(self.db, self.is_edit_video, video_id=self.data[current_row_number][0], main_window=self)
                edit.show()
            elif action == delete_video:
                self.delete_video(self.data[current_row_number][0])
        elif self.management_flag == self.defect_management_flag:
            edit_defect = ''
            delete_defect = ''
            if current_row_number != -1:  # if select one row.
                edit_defect = context_menu.addAction("编辑缺陷")
                delete_defect = context_menu.addAction("删除缺陷")
            action = context_menu.exec_(self.mapToGlobal(event.pos()))
            if action == edit_defect:
                edit = Edit(self.db, self.is_edit_defect, defect_id=self.data[current_row_number][0], main_window=self)
                edit.show()
            elif action == delete_defect:
                self.delete_defect(self.data[current_row_number][0])  # defect_id.

    def set_single_management_style(self, index):
        self.managements[index].setStyleSheet('''
            QPushButton{
                background-color:rgba(200,200,200,0.3);
                font-weight:bold;
                color:#f1f1f1;
                font-size:20px;
                border-radius:5px;
                font-family:"DengXian";
                padding:10px 10px 10px 10px;
            }
        ''')

    # if current_row_number is None, then it is add project,or it is edit project.
    def add_project(self, current_row_number=None):
        row = current_row_number
        if current_row_number is None:
            self.is_edit_project = False
            self.edit_project_id = None
            # self.show_table.setRowCount(self.show_table.rowCount() + 1)  # add new row.
            row = len(self.data)
        else:
            self.is_edit_project = True
            self.edit_project_id = self.data[current_row_number][0]
        self.is_add_project = True
        self.ensure_button.setVisible(True)
        self.cancel_button.setVisible(True)
        self.show_table.selectRow(row)  # set select row.
        self.add_project_widgets.clear()
        self.add_project_widgets.append(QLineEdit())  # project_no.
        self.add_project_widgets[0].setPlaceholderText('工程编号...')
        self.show_table.setCellWidget(row, 0, self.add_project_widgets[0])
        self.add_project_widgets.append(QLineEdit())  # project_name.
        self.add_project_widgets[1].setPlaceholderText('工程名称...')
        self.show_table.setCellWidget(row, 1, self.add_project_widgets[1])
        self.add_project_widgets.append(QLineEdit())  # project_address.
        self.add_project_widgets[2].setPlaceholderText('工程地址...')
        self.show_table.setCellWidget(row, 2, self.add_project_widgets[2])
        self.add_project_widgets.append(QComboBox())  # staff_name.
        self.add_project_widgets[3].setStyleSheet('''
            QComboBox {
                border: 2px solid lightgray;
                border-radius: 5px;
            }
             
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 15px;
                border-left-width: 1px;
                border-left-color: darkgray;
                border-left-style: solid;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
            }
             
            QComboBox::down-arrow {
                image: url(:/drop_down);
            }
        ''')
        staff = self.db.get_one_table('staff')
        self.add_project_tables.append(staff)
        for i in staff:
            self.add_project_widgets[3].addItem(i[1])
        self.show_table.setCellWidget(row, 3, self.add_project_widgets[3])
        self.add_project_widgets.append(QDateEdit())  # start_date
        self.add_project_widgets[4].setDate(QDate.currentDate())
        self.add_project_widgets[4].setCalendarPopup(True)
        self.add_project_widgets[4].setStyleSheet('''
            QDateEdit {
                border: 2px solid lightgray;
                border-radius: 5px;
            }
             
            QDateEdit::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 15px;
                border-left-width: 1px;
                border-left-color: darkgray;
                border-left-style: solid;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
            }
             
            QDateEdit::down-arrow {
                image: url(:/drop_down);
            }
        ''')
        self.show_table.setCellWidget(row, 4, self.add_project_widgets[4])
        self.add_project_widgets.append(QLineEdit())  # report_no.
        self.add_project_widgets[5].setPlaceholderText('报告编号...')
        self.show_table.setCellWidget(row, 5, self.add_project_widgets[5])
        self.add_project_widgets.append(QLineEdit())  # requester_unit.
        self.add_project_widgets[6].setPlaceholderText('委托单位...')
        self.show_table.setCellWidget(row, 6, self.add_project_widgets[6])
        self.add_project_widgets.append(QLineEdit())  # construction_unit.
        self.add_project_widgets[7].setPlaceholderText('建设单位...')
        self.show_table.setCellWidget(row, 7, self.add_project_widgets[7])
        self.add_project_widgets.append(QLineEdit())  # design_unit.
        self.add_project_widgets[8].setPlaceholderText('设计单位...')
        self.show_table.setCellWidget(row, 8, self.add_project_widgets[8])
        self.add_project_widgets.append(QLineEdit())  # build_unit.
        self.add_project_widgets[9].setPlaceholderText('施工单位...')
        self.show_table.setCellWidget(row, 9, self.add_project_widgets[9])
        self.add_project_widgets.append(QLineEdit())  # supervisory_unit.
        self.add_project_widgets[10].setPlaceholderText('监理单位...')
        self.show_table.setCellWidget(row, 10, self.add_project_widgets[10])
        self.add_project_widgets.append(QComboBox())  # detection_method.
        detection = self.db.get_one_table('detection')
        self.add_project_tables.append(detection)
        for i in detection:
            self.add_project_widgets[11].addItem(i[1])
        self.show_table.setCellWidget(row, 11, self.add_project_widgets[11])
        self.add_project_widgets.append(QComboBox())  # move_method.
        move = self.db.get_one_table('move')
        self.add_project_tables.append(move)
        for i in move:
            self.add_project_widgets[12].addItem(i[1])
        self.show_table.setCellWidget(row, 12, self.add_project_widgets[12])
        self.add_project_widgets.append(QComboBox())  # plugging_method.
        plugging = self.db.get_one_table('plugging')
        self.add_project_tables.append(plugging)
        for i in plugging:
            self.add_project_widgets[13].addItem(i[1])
        self.show_table.setCellWidget(row, 13, self.add_project_widgets[13])
        self.add_project_widgets.append(QComboBox())  # drainage_method.
        drainage = self.db.get_one_table('drainage')
        self.add_project_tables.append(drainage)
        for i in drainage:
            self.add_project_widgets[14].addItem(i[1])
        self.show_table.setCellWidget(row, 14, self.add_project_widgets[14])
        self.add_project_widgets.append(QComboBox())  # dredging _method.
        dredging = self.db.get_one_table('dredging')
        self.add_project_tables.append(dredging)
        # once there is a BUG, I wrote drainage here too...
        for i in dredging:
            self.add_project_widgets[15].addItem(i[1])
        self.show_table.setCellWidget(row, 15, self.add_project_widgets[15])
        # set all of the combo boxes' style.
        for i in range(11, 16):
            self.add_project_widgets[i].setStyleSheet('''
            QComboBox {
                border: 2px solid lightgray;
                border-radius: 5px;
            }
             
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 15px;
                border-left-width: 1px;
                border-left-color: darkgray;
                border-left-style: solid;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
            }
             
            QComboBox::down-arrow {
                image: url(:/drop_down);
            }
        ''')
        if self.is_edit_project:
            data = self.db.get_one_project_detailed(self.edit_project_id)
            self.add_project_widgets[0].setText(data[1])
            self.add_project_widgets[1].setText(data[2])
            self.add_project_widgets[2].setText(data[3])
            index = 0
            for i in self.add_project_tables[0]:
                if i == data[4]:
                    break
                index += 1
            self.add_project_widgets[3].setCurrentIndex(index)
            self.add_project_widgets[4].setDate(datetime.datetime.strptime(data[5], "%Y-%m-%d"))
            for i in range(5, 11):
                self.add_project_widgets[i].setText(data[i + 1])
            for i in range(11, 16):
                index = 0
                for j in self.add_project_tables[i - 10]:
                    if j == data[i + 1]:
                        break
                    index += 1
                self.add_project_widgets[i].setCurrentIndex(index)

    def ensure_add_project(self):
        data = []
        project_no = self.add_project_widgets[0].text()
        if len(project_no) == 0:
            QtWidgets.QMessageBox.information(self, '提示', '工程编号不能为空')
            return
        data.append(project_no)
        project_name = self.add_project_widgets[1].text()
        if len(project_name) == 0:
            QtWidgets.QMessageBox.information(self, '提示', '工程名称不能为空')
            return
        data.append(project_name)
        project_address = self.add_project_widgets[2].text()
        if len(project_address) == 0:
            QtWidgets.QMessageBox.information(self, '提示', '工程地址不能为空')
            return
        data.append(project_address)
        staff_id = self.add_project_tables[0][self.add_project_widgets[3].currentIndex()][0]
        data.append(staff_id)
        start_date = self.add_project_widgets[4].date().toString(QtCore.Qt.ISODate)
        data.append(start_date)
        report_no = self.add_project_widgets[5].text()
        data.append(report_no)
        requester_unit = self.add_project_widgets[6].text()
        data.append(requester_unit)
        construction_unit = self.add_project_widgets[7].text()
        data.append(construction_unit)
        design_unit = self.add_project_widgets[8].text()
        data.append(design_unit)
        build_unit = self.add_project_widgets[9].text()
        data.append(build_unit)
        supervisory_unit = self.add_project_widgets[10].text()
        data.append(supervisory_unit)
        detection_id = self.add_project_tables[1][self.add_project_widgets[11].currentIndex()][0]
        data.append(detection_id)
        move_id = self.add_project_tables[2][self.add_project_widgets[12].currentIndex()][0]
        data.append(move_id)
        plugging_id = self.add_project_tables[3][self.add_project_widgets[13].currentIndex()][0]
        data.append(plugging_id)
        drainage_id = self.add_project_tables[4][self.add_project_widgets[14].currentIndex()][0]
        data.append(drainage_id)
        dredging_id = self.add_project_tables[5][self.add_project_widgets[15].currentIndex()][0]
        data.append(dredging_id)

        self.ensure_button.setVisible(False)
        self.cancel_button.setVisible(False)
        self.is_add_project = False
        self.db.add_project(data, self.edit_project_id)
        self.project_management()

    def cancel_add_project(self):
        self.ensure_button.setVisible(False)
        self.cancel_button.setVisible(False)
        self.show_table.setRowCount(self.show_table.rowCount() - 1)  # delete the last row.
        self.is_add_project = False
        self.project_management()

    def add_video(self, project_id):
        self.management_flag = self.video_management_flag
        self.set_managements_style()
        self.set_single_management_style(1)
        root = Tk()
        root.withdraw()
        video_name = filedialog.askopenfilename(filetypes=[("video", "*.mp4 *.avi")], )
        self.db.add_video(project_id, video_name)
        self.video_management(project_id)

    def delete_project(self, project_id):
        reply = QMessageBox.question(self, '提示', '删除工程会删除所有相关联的视频和缺陷，是否确定删除？',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.No:
            return
        self.db.delete_project(project_id)
        current_row_number = self.show_table.currentRow()
        self.show_table.removeRow(current_row_number)

    def delete_video(self, video_id):
        reply = QMessageBox.question(self, '提示', '删除视频会删除所有相关联的缺陷，是否确定删除？',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.No:
            return
        self.db.delete_video(video_id)
        current_row_number = self.show_table.currentRow()
        self.show_table.removeRow(current_row_number)

    def delete_defect(self, defect_id):
        reply = QMessageBox.question(self, '提示', '是否确定删除缺陷？',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.No:
            return
        current_row_number = self.show_table.currentRow()
        self.show_table.removeRow(current_row_number)
        self.db.delete_defect(defect_id)

    def generate_report(self, project_id):
        flag = self.word.generate(project_id)
        QtWidgets.QMessageBox.information(self, '提示', '生成成功' if flag else '生成失败')

    def previous_table_page(self):
        if self.current_page == 1:
            return
        self.current_page -= 1
        self.page_number.setText(str(self.current_page))
        self.insert_data_to_table()

    def next_table_page(self):
        total_page_number = (len(self.data) + self.number_of_per_page - 1) // self.number_of_per_page
        if self.current_page == total_page_number:
            return
        self.current_page += 1
        self.page_number.setText(str(self.current_page))
        self.insert_data_to_table()

    def goto_table_page(self):
        total_page_number = (len(self.data) + self.number_of_per_page - 1) // self.number_of_per_page
        go = int(self.page_number.text())
        if go > total_page_number:
            self.current_page = total_page_number
        elif go < 1:
            self.current_page = 1
        else:
            self.current_page = go
        self.page_number.setText(str(self.current_page))
        self.insert_data_to_table()

    def date_changed(self):
        if self.management_flag == self.project_management_flag:
            self.project_management()
        elif self.management_flag == self.video_management_flag:
            self.video_management(None)
        elif self.management_flag == self.defect_management_flag:
            self.defect_management(None)


def run_django():
    os.system('python ./server/manage.py runserver')


class DjangoThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.running = True

    def run(self):
        if self.running:
            run_django()
        self.running = False
        time.sleep(1)


# the default tableWidgetItem use the sort :1<10<11<12<2<20<21...
# https://stackoverflow.com/questions/11938459/sorting-in-pyqt-tablewidget
class MyTableWidgetItem(QTableWidgetItem):
    # custom sorting.
    def __lt__(self, other):
        if isinstance(other, QTableWidgetItem):
            x = self.data(QtCore.Qt.EditRole)
            y = other.data(QtCore.Qt.EditRole)

            if isinstance(x, int) and isinstance(y, int):
                return x < y
            else:
                return str(x) < str(y)

        return super(MyTableWidgetItem, self).__lt__(other)


def main():
    app = QtWidgets.QApplication(sys.argv)
    splash = QtWidgets.QSplashScreen(QtGui.QPixmap(':/launch'))  # launch interface.
    splash.show()
    QtWidgets.qApp.processEvents()
    server = DjangoThread()
    server.start()
    win = MainWindow()
    win.show()
    splash.finish(win)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

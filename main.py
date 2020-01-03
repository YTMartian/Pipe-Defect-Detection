from PyQt5.QtWidgets import QMainWindow, QGraphicsDropShadowEffect, QLabel, QPushButton, QApplication, QLineEdit, \
    QListView, QHBoxLayout, QRadioButton, QTableWidget, QHeaderView
from PyQt5.QtGui import QIcon, QColor, QCursor, QPixmap, QBrush
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from resources import *
import settings
import time
import sys
import os


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Pipe Defect Detection')
        self.setWindowIcon(QIcon(':/app_icon'))
        self.setMinimumSize(1280, 720)
        self.settings = settings.Settings()

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
        if os.path.exists(self.settings.background_image) and str(
                os.path.splitext(self.settings.background_image)[1]).lower() in ['.jpg', '.png']:
            background.setBrush(self.main_widget.backgroundRole(), QBrush(QPixmap(self.settings.background_image)))
        else:
            background.setBrush(self.main_widget.backgroundRole(), QBrush(QPixmap(':/background')))
        self.main_widget.setAutoFillBackground(True)  # in this way the widget would not be transparent.
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
                background-image:url(:/skin);
            }
            QPushButton:hover{
                background-image:url(:/skin_hover);
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
        self.managements = [QPushButton() for i in range(3)]
        self.managements[0].setText('工程管理')
        self.managements[1].setText('视频管理')
        self.managements[2].setText('缺陷管理')
        self.managements[0].setIcon(QIcon(":/project_management"))  # add icon before text.
        self.managements[1].setIcon(QIcon(":/video_management"))
        self.managements[2].setIcon(QIcon(":/defect_management"))
        for i in range(3):
            self.managements[i].setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.set_managements_style()
        self.managements[0].clicked.connect(self.all_managements)
        self.managements[1].clicked.connect(self.all_managements)
        self.managements[2].clicked.connect(self.all_managements)
        self.left_layout.addWidget(self.managements[0], 3, 5, 1, 1, QtCore.Qt.AlignCenter)
        self.left_layout.addWidget(self.managements[1], 4, 5, 1, 1, QtCore.Qt.AlignCenter)
        self.left_layout.addWidget(self.managements[2], 5, 5, 1, 1, QtCore.Qt.AlignCenter)
        self.management_flag = 0
        self.project_management_flag = 1
        self.video_management_flag = 2
        self.defect_management_flag = 3

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
        self.toggle_project_field.addWidget(self.toggle_project_detailed_view)
        self.toggle_project_field.addWidget(self.toggle_project_statistic_view)
        self.manage_layout.addWidget(self.toggle_project_widget, 5, 5, 10, 1)
        self.toggle_project_widget.setStyleSheet('''
            QWidget{
                font-family:"DengXian";
                font-size:18px;
                font-weight:bold;
                color:#f1f1f1;
        }''')

        # show table.
        # settings in:https://blog.csdn.net/yekui006/article/details/98211808
        # very useful functions:https://likegeeks.com/pyqt5-tutorial/#Make-QTableWidget-not-editable-read-only
        self.show_table = QTableWidget()

        self.show_table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        # self.show_table.horizontalHeader().setVisible(False)
        self.show_table.verticalHeader().setVisible(False)  # hide teh header.
        self.show_table.horizontalHeader().setStretchLastSection(True)
        self.show_table.setShowGrid(False)
        self.manage_layout.addWidget(self.show_table, 6, 2, 10, 10)
        self.show_table.setStyleSheet('''
            QWidget{
                background:transparent;
                font-family:"DengXian";
                font-size:14px;
                font-weight:bold;
                color:#f1f1f1;
                selection-background-color:rgba(220,220,220,0.2);
                border:none;
        }''')
        self.show_table.horizontalHeader().setStyleSheet('''''')
        # set the column width auto to fix window width.
        # https://blog.csdn.net/yl_best/article/details/84070231
        self.show_table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive | QHeaderView.Stretch)
        self.show_table.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignCenter)

        self.hide_all()

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
        flag = self.settings.change_background()
        if not flag:
            return
        background = QtGui.QPalette()
        background.setBrush(self.main_widget.backgroundRole(), QBrush(QPixmap(self.settings.background_image)))
        self.main_widget.setPalette(background)

    def set_managements_style(self):
        for i in range(3):
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
        self.hide_all()
        if sender == self.managements[0]:
            self.management_flag = self.project_management_flag
            self.project_management()
        elif sender == self.managements[1]:
            self.management_flag = self.video_management_flag
            self.video_management()
        else:
            self.management_flag = self.defect_management_flag
            self.defect_management()

    def project_management(self):
        self.hide_all()
        self.search_input.setPlaceholderText('搜索工程...')
        self.toggle_project_statistic_view.setVisible(True)
        self.toggle_project_detailed_view.setVisible(True)
        self.show_table.setVisible(True)
        if self.toggle_project_detailed_view.isChecked():
            self.show_table.setColumnCount(16)
            self.show_table.setHorizontalHeaderLabels((
                '工程\n编号', '工程\n名称', '工程\n地址', '负责\n人员', '开工\n日期', '报告\n编号', '委托\n单位', '建设\n单位', '设计\n单位',
                '施工\n单位', '监理\n单位', '检测\n类型', '移动\n方式', '封堵\n方式', '排水\n方式', '清疏\n方式'))
        else:
            self.show_table.setColumnCount(10)
            self.show_table.setHorizontalHeaderLabels(
                ('工程编号', '工程名称', '工程地址', '负责人员', '开工日期', '视频总数', '管道总数', '里程(KM)', '标内判读', '判读总数'))

    def video_management(self):
        self.hide_all()
        self.search_input.setPlaceholderText('搜索视频...')
        self.show_table.setVisible(True)
        self.show_table.setColumnCount(8)
        self.show_table.setHorizontalHeaderLabels(
            ('道路名称', '管道编号', '管道类型', '管道材质', '视频文件', '视频日期', '导入日期', '判读数量'))

    def defect_management(self):
        self.hide_all()
        self.search_input.setPlaceholderText('搜索缺陷...')
        self.show_table.setVisible(True)
        self.show_table.setColumnCount(11)
        self.show_table.setHorizontalHeaderLabels(
            ('道路名称', '管道编号', '管道类型', '管道材质', '管径(mm)', '缺陷名称', '等级', '缺陷性质', '缺陷位置', '检测日期', '判读日期'))

    def hide_all(self):
        self.toggle_project_statistic_view.setVisible(False)
        self.toggle_project_detailed_view.setVisible(False)
        self.show_table.setVisible(False)

    def search(self):
        search_text = self.search_input.text()
        if len(search_text) == 0:
            QtWidgets.QMessageBox.information(self, '提示', '输入为空')
            return
        if self.management_flag == self.project_management_flag:  # search in project.
            pass
        elif self.management_flag == self.video_management_flag:  # search in video.
            pass
        elif self.management_flag == self.defect_management_flag:  # search in defect.
            pass
        else:  # search in all.
            pass

    def toggle_project_view(self):
        sender = self.sender()
        if sender == self.toggle_project_detailed_view:
            self.show_table.setColumnCount(16)
            self.show_table.setHorizontalHeaderLabels((
                '工程\n编号', '工程\n名称', '工程\n地址', '负责\n人员', '开工\n日期', '报告\n编号', '委托\n单位', '建设\n单位', '设计\n单位',
                '施工\n单位', '监理\n单位', '检测\n类型', '移动\n方式', '封堵\n方式', '排水\n方式', '清疏\n方式'))
        else:
            self.show_table.setColumnCount(10)
            self.show_table.setHorizontalHeaderLabels(
                ('工程编号', '工程名称', '工程地址', '负责人员', '开工日期', '视频总数', '管道总数', '里程(KM)', '标内判读', '判读总数'))


def main():
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

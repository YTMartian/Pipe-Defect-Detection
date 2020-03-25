from PyQt5.QtCore import QPoint, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QFormLayout, QLabel, QLineEdit, QGridLayout, QPushButton, QHBoxLayout, \
    QScrollArea, QMenu
from PyQt5.QtGui import QIcon, QCursor, QPixmap
from PyQt5 import QtWidgets, QtCore


class Staff(QMainWindow):
    def __init__(self, db, main_window=None):
        super(Staff, self).__init__(main_window)
        self.main_window = main_window
        self.setWindowTitle('人员管理')
        self.setWindowIcon(QIcon(':/app_icon'))
        self.setFixedSize(460, 700)
        self.setStyleSheet('''
            Edit{
                background:#f1f1f1;
            }
        ''')
        self.db = db
        self.main_widget = QtWidgets.QWidget(self)  # must add widget to dialog.
        self.main_layout = QtWidgets.QGridLayout(self)
        self.main_layout.setSpacing(0)
        self.main_layout.setSpacing(0)
        self.main_widget.setLayout(self.main_layout)
        self.main_widget.setAutoFillBackground(True)
        self.setCentralWidget(self.main_widget)
        self.scroll_area_widget = QtWidgets.QWidget()
        self.scroll_area = QScrollArea()
        self.bottom_widget = QtWidgets.QWidget()
        self.bottom_form = QHBoxLayout()
        self.bottom_form.setSpacing(5)
        self.bottom_form.setContentsMargins(0, 10, 0, 0)
        self.bottom_form.setAlignment(QtCore.Qt.AlignCenter)
        self.add_button = QPushButton()
        self.add_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.add_button.setText('添加')
        self.add_button.setIcon(QIcon(":/add"))
        self.add_button.setStyleSheet('''
            QPushButton{
                    font-weight:bold;
                    background-color:#827ae1;
                    color:#f1f1f1;
                    font-size:20px;
                    border-radius:10px;
                    font-family:"DengXian";
                    padding:10px 10px 10px 10px;
                }
                QPushButton:hover{
                    background-color:#5246e2;
                }
        ''')
        self.add_button.clicked.connect(self.add_staff)
        self.cancel_button = QPushButton()
        self.cancel_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.cancel_button.setText('取消')
        # self.delete_button.setIcon(QIcon(":/delete"))
        self.cancel_button.setStyleSheet('''
            QPushButton{
                    font-weight:bold;
                    background-color:#827ae1;
                    color:#f1f1f1;
                    font-size:20px;
                    border-radius:10px;
                    font-family:"DengXian";
                    padding:10px 10px 10px 10px;
                }
                QPushButton:hover{
                    background-color:#5246e2;
                }
        ''')
        self.cancel_button.clicked.connect(self.cancel)
        self.cancel_button.setVisible(False)
        self.bottom_form.addWidget(self.add_button)
        self.bottom_form.addWidget(self.cancel_button)
        self.bottom_widget.setLayout(self.bottom_form)
        self.main_layout.addWidget(self.bottom_widget, 9, 0, 1, 10)

        self.scroll_area.setFixedWidth(470)
        self.scroll_area.setAlignment(QtCore.Qt.AlignCenter)
        self.scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.main_layout.addWidget(self.scroll_area, 0, 0, 9, 9)

        self.show_staff()
        self.flag = 0
        self.is_add = 1

    def add_staff(self):
        if self.flag == 0:
            self.flag = self.is_add
            self.add_button.setText('确定')
            self.add_button.setIcon(QIcon())
            self.cancel_button.setVisible(True)

            scroll_area_form = QFormLayout()
            name_label = QLabel('姓名')
            name_widget = QLineEdit()
            scroll_area_form.addRow(name_label, name_widget)
            self.scroll_area_widget.setLayout(scroll_area_form)
            # self.scroll_area.setWidget(self.scroll_area_widget)
        elif self.flag == 1:
            self.flag = 0
            self.add_button.setText('添加')
            self.add_button.setIcon(QIcon(':/add'))
            self.cancel_button.setVisible(False)

            self.show_staff()

    def cancel(self):
        self.flag = 0
        self.add_button.setText('添加')
        self.add_button.setIcon(QIcon(':/add'))
        self.cancel_button.setVisible(False)
        self.show_staff()

    def show_staff(self):
        scroll_area_form = QFormLayout()
        staff = self.db.get_all_staffs()
        for i in range(0, len(staff), 2):
            one = Combination(staff[i][0], staff[i][1], staff[i][2], staff[i][3], db=self.db)
            one.label.signal.connect(self.show_staff)
            if i < len(staff) - 1:
                two = Combination(staff[i + 1][0], staff[i + 1][1], staff[i + 1][2], staff[i + 1][3], db=self.db)
                two.label.signal.connect(self.show_staff)
                scroll_area_form.addRow(one.widget, two.widget)
            else:
                scroll_area_form.addRow(one.widget, Combination(flag=False).widget)
        self.scroll_area_widget.setLayout(scroll_area_form)
        self.scroll_area.setWidget(self.scroll_area_widget)


class Combination:
    def __init__(self, staff_id=0, text1='', text2='', text3='', flag=True, db=None):
        self.layout = QGridLayout()
        self.widget = QtWidgets.QWidget()
        self.label = MyLabel(staff_id, db)
        self.label.setPixmap(QPixmap(":/staff"))
        if not flag:
            self.label.setVisible(False)
        self.text1 = QLabel()
        self.text2 = QLabel()
        self.text3 = QLabel()
        if flag:
            self.text1.setText("姓名：" + text1)
            self.text2.setText("职务：" + text2)
            self.text3.setText("证号" + text3)
        self.text1.setStyleSheet('''
            QLabel{
                color:232323;
                font-size:15px;
                font-family:"DengXian";
                margin-top:-5px;
            }
        ''')
        self.text2.setStyleSheet('''
            QLabel{
                color:232323;
                font-size:15px;
                font-family:"DengXian";
                margin-top:-5px;
            }
        ''')
        self.text3.setStyleSheet('''
            QLabel{
                color:232323;
                font-size:15px;
                font-family:"DengXian";
                margin-top:-5px;
            }
        ''')
        self.layout.addWidget(self.label, 1, 0, 1, 1)
        self.layout.addWidget(self.text1, 0, 1, 1, 1)
        self.layout.addWidget(self.text2, 1, 1, 1, 1)
        self.layout.addWidget(self.text3, 2, 1, 1, 1)
        self.widget.setLayout(self.layout)


class MyLabel(QLabel):
    signal=pyqtSignal()
    def __init__(self, staff_id, db):
        super(MyLabel, self).__init__()
        self.staff_id = staff_id
        self.db = db

    def mousePressEvent(self, event):
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
        edit = context_menu.addAction("编辑")
        delete = context_menu.addAction("删除")
        action = context_menu.exec_(self.mapToGlobal(QPoint(self.pos().x(), self.pos().y())))
        if action == edit:
            print('编辑')
        elif action == delete:
            flag = self.db.delete_staff(self.staff_id)
            QtWidgets.QMessageBox.information(self, '提示', '删除成功' if flag else '删除失败')
            self.signal.emit()

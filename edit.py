from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QScrollArea, QMainWindow, QHBoxLayout, QFormLayout, QLineEdit, \
    QComboBox, QDateEdit, QTextEdit, QSpinBox, QDoubleSpinBox, QDateTimeEdit, QSlider, QStyle
from PyQt5.QtGui import QIcon, QCursor, QPixmap, QImage
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QDate, QMutexLocker, QObject, QThread
import functools
import random
import time
import cv2


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
        self.video_data = None
        self.defect_data = None
        self.is_playing = False
        self.video_frame_width = 0
        self.video_frame_height = 0

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
        self.right_widget.setFixedWidth(400)
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
        self.delete_button = QPushButton()
        self.delete_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.delete_button.setText('删除')
        self.delete_button.setIcon(QIcon(":/delete"))
        self.delete_button.clicked.connect(self.delete_defect)
        self.delete_button.setStyleSheet('''
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
        self.next_defect_button = QPushButton()
        self.next_defect_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.next_defect_button.setIcon(QIcon(":/forward"))
        self.next_defect_button.clicked.connect(self.next_defect)
        self.next_defect_button.setStyleSheet('''
            QPushButton{
                background-color:#434343;
                border-radius:10px;
                padding:10px 10px 10px 10px;
            }
            QPushButton:hover{
                background-color:#131313;
            }
        ''')
        self.previous_defect_button = QPushButton()
        self.previous_defect_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.previous_defect_button.setIcon(QIcon(":/backward"))
        self.previous_defect_button.clicked.connect(self.previous_defect)
        self.previous_defect_button.setStyleSheet('''
            QPushButton{
                background-color:#434343;
                border-radius:10px;
                padding:10px 10px 10px 10px;
            }
            QPushButton:hover{
                background-color:#131313;
            }
        ''')

        self.right_bottom_layout.addWidget(self.previous_defect_button)
        self.right_bottom_layout.addWidget(self.save_button)
        self.right_bottom_layout.addWidget(self.cancel_button)
        self.right_bottom_layout.addWidget(self.delete_button)
        self.right_bottom_layout.addWidget(self.next_defect_button)
        self.right_bottom_widget = QtWidgets.QWidget()
        self.right_bottom_widget.setLayout(self.right_bottom_layout)
        self.right_layout.addWidget(self.right_bottom_widget, 22, 0, 1, 3)

        # scroll area.
        self.edit_video_scroll_area_widget = QtWidgets.QWidget()
        self.edit_defect_scroll_area_widget = QtWidgets.QWidget()
        self.project_detailed_scroll_area_widget = QtWidgets.QWidget()
        self.edit_video_scroll_area_widget.setStyleSheet('''
            QWidget{
                color:#232323;
                font-size:18px;
                font-weight:bold;
                font-family:"DengXian";
            }
        ''')
        self.edit_defect_scroll_area_widget.setStyleSheet('''
            QWidget{
                color:#232323;
                font-size:18px;
                font-weight:bold;
                font-family:"DengXian";
            }
        ''')
        self.project_detailed_scroll_area_widget.setStyleSheet('''
            QWidget{
                color:#232323;
                font-size:18px;
                font-weight:bold;
                font-family:"DengXian";
            }
        ''')
        self.setCentralWidget(self.main_widget)
        self.edit_video_scroll_area_form = QFormLayout()
        self.edit_defect_scroll_area_form = QFormLayout()
        self.project_detailed_scroll_area_form = QFormLayout()

        """
        all of the labels and widgets in edit_video.
        """
        self.video_name_label, self.video_name_widget = QLabel(), QLineEdit()
        self.video_name_label.setText('视频文件名')
        self.video_name_widget.setReadOnly(True)
        self.edit_video_scroll_area_form.addRow(self.video_name_label, self.video_name_widget)
        self.staff_label, self.staff_widget = QLabel(), QComboBox()
        self.staff_label.setText('检测人员')
        self.edit_video_scroll_area_form.addRow(self.staff_label, self.staff_widget)
        self.record_date_label, self.record_date_widget = QLabel(), QLineEdit()
        self.record_date_label.setText('检测日期')
        self.record_date_widget.setReadOnly(True)
        self.edit_video_scroll_area_form.addRow(self.record_date_label, self.record_date_widget)
        self.import_date_label, self.import_date_widget = QLabel(), QLineEdit()
        self.import_date_label.setText('导入日期')
        self.import_date_widget.setReadOnly(True)
        self.edit_video_scroll_area_form.addRow(self.import_date_label, self.import_date_widget)
        self.road_name_label, self.road_name_widget = QLabel(), QLineEdit()
        self.road_name_label.setText('道路名称')
        self.edit_video_scroll_area_form.addRow(self.road_name_label, self.road_name_widget)
        self.start_manhole_no_label, self.start_manhole_no_widget = QLabel(), QLineEdit()
        self.start_manhole_no_label.setText('起始井编号')
        self.edit_video_scroll_area_form.addRow(self.start_manhole_no_label, self.start_manhole_no_widget)
        self.start_manhole_type_label, self.start_manhole_type_widget = QLabel(), QComboBox()
        self.start_manhole_type_label.setText('起始井类型')
        self.edit_video_scroll_area_form.addRow(self.start_manhole_type_label, self.start_manhole_type_widget)
        self.start_manhole_material_label, self.start_manhole_material_widget = QLabel(), QComboBox()
        self.start_manhole_material_label.setText('起始井材质')
        self.edit_video_scroll_area_form.addRow(self.start_manhole_material_label, self.start_manhole_material_widget)
        self.start_manhole_cover_label, self.start_manhole_cover_widget = QLabel(), QComboBox()
        self.start_manhole_cover_label.setText('起始井盖材质')
        self.edit_video_scroll_area_form.addRow(self.start_manhole_cover_label, self.start_manhole_cover_widget)
        self.start_manhole_internal_defect_label, self.start_manhole_internal_defect_widget = QLabel(), QLineEdit()
        self.start_manhole_internal_defect_label.setText('起始井内部缺陷')
        self.edit_video_scroll_area_form.addRow(self.start_manhole_internal_defect_label,
                                                self.start_manhole_internal_defect_widget)
        self.start_manhole_external_defect_label, self.start_manhole_external_defect_widget = QLabel(), QLineEdit()
        self.start_manhole_external_defect_label.setText('起始井外部缺陷')
        self.edit_video_scroll_area_form.addRow(self.start_manhole_external_defect_label,
                                                self.start_manhole_external_defect_widget)
        self.start_manhole_longitude_label, self.start_manhole_longitude_widget = QLabel(), QDoubleSpinBox()
        self.start_manhole_longitude_label.setText('起始井经度坐标')
        self.start_manhole_longitude_widget.setMaximum(180)  # [-180,180]
        self.start_manhole_longitude_widget.setMinimum(-180)
        self.edit_video_scroll_area_form.addRow(self.start_manhole_longitude_label, self.start_manhole_longitude_widget)
        self.start_manhole_latitude_label, self.start_manhole_latitude_widget = QLabel(), QDoubleSpinBox()
        self.start_manhole_latitude_label.setText('起始井纬度坐标')
        self.start_manhole_latitude_widget.setMaximum(90)  # [-90,90]
        self.start_manhole_latitude_widget.setMinimum(-90)
        self.edit_video_scroll_area_form.addRow(self.start_manhole_latitude_label, self.start_manhole_latitude_widget)
        self.start_manhole_pipe_elevation_label, self.start_manhole_pipe_elevation_widget = QLabel(), QDoubleSpinBox()
        self.start_manhole_pipe_elevation_label.setText('起始井高程')
        self.edit_video_scroll_area_form.addRow(self.start_manhole_pipe_elevation_label,
                                                self.start_manhole_pipe_elevation_widget)
        self.end_manhole_no_label, self.end_manhole_no_widget = QLabel(), QLineEdit()
        self.end_manhole_no_label.setText('结束井编号')
        self.edit_video_scroll_area_form.addRow(self.end_manhole_no_label, self.end_manhole_no_widget)
        self.end_manhole_type_label, self.end_manhole_type_widget = QLabel(), QComboBox()
        self.end_manhole_type_label.setText('结束井类型')
        self.edit_video_scroll_area_form.addRow(self.end_manhole_type_label, self.end_manhole_type_widget)
        self.end_manhole_material_label, self.end_manhole_material_widget = QLabel(), QComboBox()
        self.end_manhole_material_label.setText('结束井材质')
        self.edit_video_scroll_area_form.addRow(self.end_manhole_material_label, self.end_manhole_material_widget)
        self.end_manhole_cover_label, self.end_manhole_cover_widget = QLabel(), QComboBox()
        self.end_manhole_cover_label.setText('结束井盖材质')
        self.edit_video_scroll_area_form.addRow(self.end_manhole_cover_label, self.end_manhole_cover_widget)
        self.end_manhole_internal_defect_label, self.end_manhole_internal_defect_widget = QLabel(), QLineEdit()
        self.end_manhole_internal_defect_label.setText('结束井内部缺陷')
        self.edit_video_scroll_area_form.addRow(self.end_manhole_internal_defect_label,
                                                self.end_manhole_internal_defect_widget)
        self.end_manhole_external_defect_label, self.end_manhole_external_defect_widget = QLabel(), QLineEdit()
        self.end_manhole_external_defect_label.setText('结束井外部缺陷')
        self.edit_video_scroll_area_form.addRow(self.end_manhole_external_defect_label,
                                                self.end_manhole_external_defect_widget)
        self.end_manhole_longitude_label, self.end_manhole_longitude_widget = QLabel(), QDoubleSpinBox()
        self.end_manhole_longitude_label.setText('结束井经度坐标')
        self.end_manhole_longitude_widget.setMaximum(180)  # [-180,180]
        self.end_manhole_longitude_widget.setMinimum(-180)
        self.edit_video_scroll_area_form.addRow(self.end_manhole_longitude_label, self.end_manhole_longitude_widget)
        self.end_manhole_latitude_label, self.end_manhole_latitude_widget = QLabel(), QDoubleSpinBox()
        self.end_manhole_latitude_label.setText('结束井纬度坐标')
        self.end_manhole_latitude_widget.setMaximum(90)  # [-180,180]
        self.end_manhole_latitude_widget.setMinimum(-90)
        self.edit_video_scroll_area_form.addRow(self.end_manhole_latitude_label, self.end_manhole_latitude_widget)
        self.end_manhole_pipe_elevation_label, self.end_manhole_pipe_elevation_widget = QLabel(), QDoubleSpinBox()
        self.end_manhole_pipe_elevation_label.setText('结束井高程')
        self.edit_video_scroll_area_form.addRow(self.end_manhole_pipe_elevation_label,
                                                self.end_manhole_pipe_elevation_widget)
        self.pipe_type_label, self.pipe_type_widget = QLabel(), QComboBox()
        self.pipe_type_label.setText('管道类型')
        self.edit_video_scroll_area_form.addRow(self.pipe_type_label, self.pipe_type_widget)
        self.section_shape_label, self.section_shape_widget = QLabel(), QComboBox()
        self.section_shape_label.setText('截面形状')
        self.edit_video_scroll_area_form.addRow(self.section_shape_label, self.section_shape_widget)
        self.joint_form_label, self.joint_form_widget = QLabel(), QComboBox()
        self.joint_form_label.setText('接口形式')
        self.edit_video_scroll_area_form.addRow(self.joint_form_label, self.joint_form_widget)
        self.pipe_material_label, self.pipe_material_widget = QLabel(), QComboBox()
        self.pipe_material_label.setText('管道材质')
        self.edit_video_scroll_area_form.addRow(self.pipe_material_label, self.pipe_material_widget)
        self.pipe_diameter_label, self.pipe_diameter_widget = QLabel(), QDoubleSpinBox()
        self.pipe_diameter_label.setText('管道直径(mm)')
        self.edit_video_scroll_area_form.addRow(self.pipe_diameter_label, self.pipe_diameter_widget)
        self.start_pipe_depth_label, self.start_pipe_depth_widget = QLabel(), QDoubleSpinBox()
        self.start_pipe_depth_label.setText('起点埋深(m)')
        self.edit_video_scroll_area_form.addRow(self.start_pipe_depth_label, self.start_pipe_depth_widget)
        self.end_pipe_depth_label, self.end_pipe_depth_widget = QLabel(), QDoubleSpinBox()
        self.end_pipe_depth_label.setText('终点埋深(m)')
        self.edit_video_scroll_area_form.addRow(self.end_pipe_depth_label, self.end_pipe_depth_widget)
        self.pipe_length_label, self.pipe_length_widget = QLabel(), QDoubleSpinBox()
        self.pipe_length_label.setText('管道长度(m)')
        self.edit_video_scroll_area_form.addRow(self.pipe_length_label, self.pipe_length_widget)
        self.detection_length_label, self.detection_length_widget = QLabel(), QDoubleSpinBox()
        self.detection_length_label.setText('检测长度(m)')
        self.edit_video_scroll_area_form.addRow(self.detection_length_label, self.detection_length_widget)
        self.detection_direction_label, self.detection_direction_widget = QLabel(), QComboBox()
        self.detection_direction_label.setText('检测方向')
        self.edit_video_scroll_area_form.addRow(self.detection_direction_label, self.detection_direction_widget)
        self.construction_year_label, self.construction_year_widget = QLabel(), QDateEdit()
        self.construction_year_label.setText('铺设年代')
        self.construction_year_widget.setDate(QDate.currentDate())
        self.construction_year_widget.setCalendarPopup(True)
        self.edit_video_scroll_area_form.addRow(self.construction_year_label, self.construction_year_widget)
        self.regional_importance_label, self.regional_importance_widget = QLabel(), QComboBox()
        self.regional_importance_label.setText('地区重要性')
        self.edit_video_scroll_area_form.addRow(self.regional_importance_label, self.regional_importance_widget)
        self.soil_label, self.soil_widget = QLabel(), QComboBox()
        self.soil_label.setText('土质影响')
        self.edit_video_scroll_area_form.addRow(self.soil_label, self.soil_widget)
        self.video_remark_label, self.video_remark_widget = QLabel(), QTextEdit()
        self.video_remark_label.setText('备注信息')
        self.video_remark_widget.setFixedWidth(190)
        self.edit_video_scroll_area_form.addRow(self.video_remark_label, self.video_remark_widget)

        """
        all of the labels and widgets in edit_defect.
        """
        self.defect_type_label, self.defect_type_widget = QLabel(), QComboBox()
        self.defect_type_label.setText('缺陷类别')
        self.defect_type_widget.currentIndexChanged.connect(self.defect_type_changed)
        self.edit_defect_scroll_area_form.addRow(self.defect_type_label, self.defect_type_widget)
        self.defect_attribute_label, self.defect_attribute_widget = QLabel(), QLineEdit()
        self.defect_attribute_label.setText('缺陷性质')
        self.edit_defect_scroll_area_form.addRow(self.defect_attribute_label, self.defect_attribute_widget)
        self.defect_grade_label, self.defect_grade_widget = QLabel(), QComboBox()
        self.defect_grade_label.setText('缺陷级别')
        self.edit_defect_scroll_area_form.addRow(self.defect_grade_label, self.defect_grade_widget)
        self.defect_distance_label, self.defect_distance_widget = QLabel(), QDoubleSpinBox()
        self.defect_distance_label.setText('缺陷距离(m)')
        self.defect_distance_widget.setMaximum(1 << 30)
        self.edit_defect_scroll_area_form.addRow(self.defect_distance_label, self.defect_distance_widget)
        self.defect_length_label, self.defect_length_widget = QLabel(), QDoubleSpinBox()
        self.defect_length_label.setText('缺陷长度(m)')
        self.defect_length_widget.setMaximum(1 << 30)
        self.edit_defect_scroll_area_form.addRow(self.defect_length_label, self.defect_length_widget)
        self.clock_start_label, self.clock_start_widget = QLabel(), QSpinBox()
        self.clock_start_label.setText('环向起点')
        self.clock_start_widget.setMinimum(1)
        self.clock_start_widget.setMaximum(12)
        self.edit_defect_scroll_area_form.addRow(self.clock_start_label, self.clock_start_widget)
        self.clock_end_label, self.clock_end_widget = QLabel(), QSpinBox()
        self.clock_end_label.setText('环向终点')
        self.clock_end_widget.setMinimum(1)
        self.clock_start_widget.setMaximum(12)
        self.edit_defect_scroll_area_form.addRow(self.clock_end_label, self.clock_end_widget)
        self.defect_date_label, self.defect_date_widget = QLabel(), QLineEdit()
        self.defect_date_label.setText('判读日期')
        self.defect_date_widget.setReadOnly(True)
        self.edit_defect_scroll_area_form.addRow(self.defect_date_label, self.defect_date_widget)
        self.defect_time_in_video_label, self.defect_time_in_video_widget = QLabel(), QLineEdit()
        self.defect_time_in_video_label.setText('视频中位置(帧)')
        self.defect_time_in_video_widget.setReadOnly(True)
        self.edit_defect_scroll_area_form.addRow(self.defect_time_in_video_label, self.defect_time_in_video_widget)
        self.defect_remark_label, self.defect_remark_widget = QLabel(), QTextEdit()
        self.defect_remark_label.setText('备注信息')
        self.defect_remark_widget.setFixedWidth(235)
        self.edit_defect_scroll_area_form.addRow(self.defect_remark_label, self.defect_remark_widget)
        """
        all of the labels and widgets in project_detailed.
        """
        self.project_no_label, self.project_no_widget = QLabel(), QLineEdit()
        self.project_no_label.setText('工程编号')
        self.project_no_widget.setReadOnly(True)
        self.project_detailed_scroll_area_form.addRow(self.project_no_label, self.project_no_widget)
        self.project_name_label, self.project_name_widget = QLabel(), QLineEdit()
        self.project_name_label.setText('工程名称')
        self.project_name_widget.setReadOnly(True)
        self.project_detailed_scroll_area_form.addRow(self.project_name_label, self.project_name_widget)
        self.project_address_label, self.project_address_widget = QLabel(), QLineEdit()
        self.project_address_label.setText('工程地址')
        self.project_address_widget.setReadOnly(True)
        self.project_detailed_scroll_area_form.addRow(self.project_address_label, self.project_address_widget)
        self.project_staff_label, self.project_staff_widget = QLabel(), QLineEdit()
        self.project_staff_label.setText('负责人')
        self.project_staff_widget.setReadOnly(True)
        self.project_detailed_scroll_area_form.addRow(self.project_staff_label, self.project_staff_widget)
        self.project_start_date_label, self.project_start_date_widget = QLabel(), QLineEdit()
        self.project_start_date_label.setText('开工日期')
        self.project_start_date_widget.setReadOnly(True)
        self.project_detailed_scroll_area_form.addRow(self.project_start_date_label, self.project_start_date_widget)
        self.project_report_no_label, self.project_report_no_widget = QLabel(), QLineEdit()
        self.project_report_no_label.setText('报告编号')
        self.project_report_no_widget.setReadOnly(True)
        self.project_detailed_scroll_area_form.addRow(self.project_report_no_label, self.project_report_no_widget)
        self.project_requester_unit_label, self.project_requester_unit_widget = QLabel(), QLineEdit()
        self.project_requester_unit_label.setText('委托单位')
        self.project_requester_unit_widget.setReadOnly(True)
        self.project_detailed_scroll_area_form.addRow(self.project_requester_unit_label,
                                                      self.project_requester_unit_widget)
        self.project_construction_unit_label, self.project_construction_unit_widget = QLabel(), QLineEdit()
        self.project_construction_unit_label.setText('建设单位')
        self.project_construction_unit_widget.setReadOnly(True)
        self.project_detailed_scroll_area_form.addRow(self.project_construction_unit_label,
                                                      self.project_construction_unit_widget)
        self.project_design_unit_label, self.project_design_unit_widget = QLabel(), QLineEdit()
        self.project_design_unit_label.setText('设计单位')
        self.project_design_unit_widget.setReadOnly(True)
        self.project_detailed_scroll_area_form.addRow(self.project_design_unit_label,
                                                      self.project_design_unit_widget)
        self.project_build_unit_label, self.project_build_unit_widget = QLabel(), QLineEdit()
        self.project_build_unit_label.setText('施工单位')
        self.project_build_unit_widget.setReadOnly(True)
        self.project_detailed_scroll_area_form.addRow(self.project_build_unit_label,
                                                      self.project_build_unit_widget)
        self.project_supervisory_unit_label, self.project_supervisory_unit_widget = QLabel(), QLineEdit()
        self.project_supervisory_unit_label.setText('监理单位')
        self.project_supervisory_unit_widget.setReadOnly(True)
        self.project_detailed_scroll_area_form.addRow(self.project_supervisory_unit_label,
                                                      self.project_supervisory_unit_widget)
        self.project_detection_label, self.project_detection_widget = QLabel(), QLineEdit()
        self.project_detection_label.setText('检测类型')
        self.project_detection_widget.setReadOnly(True)
        self.project_detailed_scroll_area_form.addRow(self.project_detection_label, self.project_detection_widget)
        self.project_move_label, self.project_move_widget = QLabel(), QLineEdit()
        self.project_move_label.setText('移动方式')
        self.project_move_widget.setReadOnly(True)
        self.project_detailed_scroll_area_form.addRow(self.project_move_label, self.project_move_widget)
        self.project_plugging_label, self.project_plugging_widget = QLabel(), QLineEdit()
        self.project_plugging_label.setText('封堵方式')
        self.project_plugging_widget.setReadOnly(True)
        self.project_detailed_scroll_area_form.addRow(self.project_plugging_label, self.project_plugging_widget)
        self.project_drainage_label, self.project_drainage_widget = QLabel(), QLineEdit()
        self.project_drainage_label.setText('排水方式')
        self.project_drainage_widget.setReadOnly(True)
        self.project_detailed_scroll_area_form.addRow(self.project_drainage_label, self.project_drainage_widget)
        self.project_dredging_label, self.project_dredging_widget = QLabel(), QLineEdit()
        self.project_dredging_label.setText('清疏方式')
        self.project_dredging_widget.setReadOnly(True)
        self.project_detailed_scroll_area_form.addRow(self.project_dredging_label, self.project_dredging_widget)

        self.edit_video_scroll_area_widget.setLayout(self.edit_video_scroll_area_form)
        self.edit_defect_scroll_area_widget.setLayout(self.edit_defect_scroll_area_form)
        self.project_detailed_scroll_area_widget.setLayout(self.project_detailed_scroll_area_form)
        self.edit_video_scroll_area = QScrollArea()
        self.edit_defect_scroll_area = QScrollArea()
        self.project_detailed_scroll_area = QScrollArea()
        self.edit_video_scroll_area.setWidget(self.edit_video_scroll_area_widget)
        self.edit_defect_scroll_area.setWidget(self.edit_defect_scroll_area_widget)
        self.project_detailed_scroll_area.setWidget(self.project_detailed_scroll_area_widget)
        self.right_layout.addWidget(self.edit_video_scroll_area, 2, 0, 20, 3)
        self.right_layout.addWidget(self.edit_defect_scroll_area, 2, 0, 20, 3)
        self.right_layout.addWidget(self.project_detailed_scroll_area, 2, 0, 20, 3)

        self.set_three_buttons_style()
        self.all_defects = None
        self.hide_something()
        self.set_project_info()
        self.set_video_info()

        """
        play the video.
        """
        self.video_frame = QLabel()  # show video frame.
        self.play_button = QPushButton()
        self.play_button.setIcon(QIcon(':/play'))
        self.play_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.play_button.clicked.connect(self.play_video)
        self.play_button.setStyleSheet('''
            QPushButton{
                border-radius:5px;
                padding:10px 10px 10px 10px;
            }
            QPushButton:hover{
                background-color:rgba(200,200,200,0.2);
            }
        ''')
        self.previous_frame_button = QPushButton()
        self.previous_frame_button.setIcon(QIcon(':/previous'))
        self.previous_frame_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.previous_frame_button.clicked.connect(self.previous_frame)
        self.previous_frame_button.setStyleSheet('''
            QPushButton{
                border-radius:5px;
                padding:10px 10px 10px 10px;
            }
            QPushButton:hover{
                background-color:rgba(200,200,200,0.2);
            }
        ''')
        self.next_frame_button = QPushButton()
        self.next_frame_button.setIcon(QIcon(':/next'))
        self.next_frame_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.next_frame_button.clicked.connect(self.next_frame)
        self.next_frame_button.setStyleSheet('''
            QPushButton{
                border-radius:5px;
                padding:10px 10px 10px 10px;
            }
            QPushButton:hover{
                background-color:rgba(200,200,200,0.2);
            }
        ''')
        self.manual_button = QPushButton()
        self.manual_button.setIcon(QIcon(':/manual'))
        self.manual_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.manual_button.clicked.connect(self.manual)
        self.manual_button.setText('手动标记')
        self.manual_button.setStyleSheet('''
            QPushButton{
                font-weight:bold;
                color:#f1f1f1;
                font-size:18px;
                border-radius:5px;
                font-family:"DengXian";
                padding:10px 10px 10px 10px;
            }
            QPushButton:hover{
                background-color:rgba(200,200,200,0.2);
            }
        ''')
        self.auto_button = QPushButton()
        self.auto_button.setIcon(QIcon(':/auto'))
        self.auto_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.auto_button.clicked.connect(self.auto)
        self.auto_button.setText('自动检测')
        self.auto_button.setStyleSheet('''
            QPushButton{
                font-weight:bold;
                color:#f1f1f1;
                font-size:18px;
                border-radius:5px;
                font-family:"DengXian";
                padding:10px 10px 10px 10px;
            }
            QPushButton:hover{
                background-color:rgba(200,200,200,0.2);
            }
        ''')
        self.slider = QSlider(QtCore.Qt.Horizontal)
        self.slider.valueChanged.connect(self.slide_frame)
        self.slider.setSingleStep(1)
        self.slider.setCursor((QCursor(QtCore.Qt.PointingHandCursor)))
        self.show_frame_label = QLabel()
        self.show_frame_label.setAlignment(QtCore.Qt.AlignRight)
        self.show_frame_label.setStyleSheet('''
            QLabel{
                font-weight:bold;
                color:#f1f1f1;
                font-size:18px;
                font-family:"DengXian";
            }
        ''')
        self.draw_field = QLabel()
        self.draw_field.setFixedHeight(20)

        self.left_layout.addWidget(self.video_frame, 0, 0, 10, 10)
        self.left_layout.addWidget(self.slider, 11, 0, 1, 10)
        self.left_layout.addWidget(self.draw_field, 12, 0, 1, 10)
        self.left_layout.addWidget(self.previous_frame_button, 13, 0, 1, 1)
        self.left_layout.addWidget(self.play_button, 13, 1, 1, 1)
        self.left_layout.addWidget(self.next_frame_button, 13, 2, 1, 1)
        self.left_layout.addWidget(self.manual_button, 13, 3, 1, 2)
        self.left_layout.addWidget(self.auto_button, 13, 5, 1, 2)
        self.left_layout.addWidget(self.show_frame_label, 13, 8, 1, 2)
        self.left_layout.setAlignment(QtCore.Qt.AlignCenter)
        # record this image to determine the frame size after changing the window size.
        self.image_to_determine_frame_size = None
        self.new_frame_width = 0
        self.new_frame_height = 0
        self.current_frame_number = 1
        self.total_frame_number = 1
        self.video = None
        self.fps = 1
        # use another thread to change the frame label.
        self.timer = VideoTimer()
        self.timer.timeSignal.signal[str].connect(self.show_one_frame)
        self.initialize_video()
        self.sort_defects_by_time()
        self.draw_all_defects()

        # to just solve a bug...
        if self.mode == self.is_edit_defect:
            # find the defect_id's index in all_defects.
            index = 0
            for i in self.all_defects:
                if str(self.defect_id) == str(i['defect_id']):
                    break
                index += 1
            self.current_frame_number = int(self.all_defects[index]['time_in_video'])
            self.show_one_frame()

    def save(self):
        if self.mode == self.is_edit_video:
            self.save_video_info()
        elif self.mode == self.is_edit_defect:
            self.save_defect_info()

    def cancel(self):
        if self.mode == self.is_edit_video:
            self.set_video_info()
        elif self.mode == self.is_edit_defect:
            self.set_defect_info()

    def hide_something(self):
        if self.mode == self.is_show_project_info:
            self.save_button.setVisible(False)
            self.cancel_button.setVisible(False)
            self.next_defect_button.setVisible(False)
            self.previous_defect_button.setVisible(False)
            self.delete_button.setVisible(False)
            self.edit_video_scroll_area.setVisible(False)
            self.edit_defect_scroll_area.setVisible(False)
            self.project_detailed_scroll_area.setVisible(True)
        elif self.mode == self.is_edit_video:
            self.save_button.setVisible(True)
            self.cancel_button.setVisible(True)
            self.next_defect_button.setVisible(False)
            self.previous_defect_button.setVisible(False)
            self.delete_button.setVisible(False)
            self.edit_video_scroll_area.setVisible(True)
            self.edit_defect_scroll_area.setVisible(False)
            self.project_detailed_scroll_area.setVisible(False)
        elif self.mode == self.is_edit_defect:
            self.save_button.setVisible(True)
            self.cancel_button.setVisible(True)
            self.next_defect_button.setVisible(True)
            self.previous_defect_button.setVisible(True)
            self.delete_button.setVisible(True)
            self.edit_video_scroll_area.setVisible(False)
            self.edit_defect_scroll_area.setVisible(True)
            self.project_detailed_scroll_area.setVisible(False)
            if self.defect_id is None and self.all_defects is not None and len(self.all_defects) != 0:
                self.defect_id = int(self.all_defects[0]['defect_id'])
            self.set_defect_info()

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

    # set all the labels and widgets' style in edit_video.
    def set_edit_video_labels_and_widgets_style(self):
        pass

    # set all the labels and widgets' style in edit_defect.
    def set_edit_defect_labels_and_widgets_style(self):
        pass

    # set all the labels and widgets' style in project_detailed.
    def set_project_detailed_labels_and_widgets_style(self):
        pass

    def set_project_info(self):
        # if no video_id.
        if self.video_id is None:
            data = self.main_window.db.get_project_by_defect_id(self.defect_id)
        else:
            data = self.main_window.db.get_project_by_video_id(self.video_id)
        if data is None:
            return
        self.project_no_widget.setText(data[1])
        self.project_name_widget.setText(data[2])
        self.project_address_widget.setText(data[3])
        self.project_staff_widget.setText(data[4])
        self.project_start_date_widget.setText(data[5])
        self.project_report_no_widget.setText(data[6])
        self.project_requester_unit_widget.setText(data[7])
        self.project_construction_unit_widget.setText(data[8])
        self.project_design_unit_widget.setText(data[9])
        self.project_build_unit_widget.setText(data[10])
        self.project_supervisory_unit_widget.setText(data[11])
        self.project_detection_widget.setText(data[12])
        self.project_move_widget.setText(data[13])
        self.project_plugging_widget.setText(data[14])
        self.project_drainage_widget.setText(data[15])
        self.project_dredging_widget.setText(data[16])

    def set_video_info(self):
        # if no video_id.
        if self.video_id is None:
            data = self.main_window.db.get_video_by_defect_id(self.defect_id)
        else:
            data = self.main_window.db.get_video_by_video_id(self.video_id)
        self.video_data = data
        if data is None:
            return
        self.video_id = int(data['video_id'])
        if self.all_defects is None:
            self.all_defects = self.main_window.db.get_all_defects(self.video_id)

        self.video_name_widget.setText(data['video_name'])
        self.video_name_widget.setToolTip(data['video_name'])
        self.staff_widget.clear()
        for i in data['staff']:
            self.staff_widget.addItem(i[1])
        index = 0
        for i in data['staff']:
            if str(i[0]) == str(data['staff_id']):
                break
            index += 1
        self.staff_widget.setCurrentIndex(index)
        self.record_date_widget.setText(data['record_date'])
        self.import_date_widget.setText(data['import_date'])
        self.road_name_widget.setText(data['road_name'])
        self.start_manhole_no_widget.setText(data['start_manhole_no'])
        self.start_manhole_type_widget.clear()
        for i in data['manhole_type']:
            self.start_manhole_type_widget.addItem(i[1])
        index = 0
        for i in data['manhole_type']:
            if str(i[0]) == str(data['start_manhole_type_id']):
                break
            index += 1
        self.start_manhole_type_widget.setCurrentIndex(index)
        self.start_manhole_material_widget.clear()
        for i in data['manhole_material']:
            self.start_manhole_material_widget.addItem(i[1])
        index = 0
        for i in data['manhole_material']:
            if str(i[0]) == str(data['start_manhole_material_id']):
                break
            index += 1
        self.start_manhole_material_widget.setCurrentIndex(index)
        self.start_manhole_cover_widget.clear()
        for i in data['manhole_cover']:
            self.start_manhole_cover_widget.addItem(i[1])
        index = 0
        for i in data['manhole_cover']:
            if str(i[0]) == str(data['start_manhole_cover_id']):
                break
            index += 1
        self.start_manhole_cover_widget.setCurrentIndex(index)
        self.start_manhole_internal_defect_widget.setText(data['start_internal_defect'])
        self.start_manhole_external_defect_widget.setText(data['start_external_defect'])
        self.start_manhole_longitude_widget.setValue(data['start_manhole_longitude'])
        self.start_manhole_latitude_widget.setValue(data['start_manhole_latitude'])
        self.start_manhole_pipe_elevation_widget.setValue(data['start_pipe_elevation'])
        self.end_manhole_no_widget.setText(data['end_manhole_no'])
        self.end_manhole_type_widget.clear()
        for i in data['manhole_type']:
            self.end_manhole_type_widget.addItem(i[1])
        index = 0
        for i in data['manhole_type']:
            if str(i[0]) == str(data['end_manhole_type_id']):
                break
            index += 1
        self.end_manhole_type_widget.setCurrentIndex(index)
        self.end_manhole_material_widget.clear()
        for i in data['manhole_material']:
            self.end_manhole_material_widget.addItem(i[1])
        index = 0
        for i in data['manhole_material']:
            if str(i[0]) == str(data['end_manhole_material_id']):
                break
            index += 1
        self.end_manhole_material_widget.setCurrentIndex(index)
        self.end_manhole_cover_widget.clear()
        for i in data['manhole_cover']:
            self.end_manhole_cover_widget.addItem(i[1])
        index = 0
        for i in data['manhole_cover']:
            if str(i[0]) == str(data['end_manhole_cover_id']):
                break
            index += 1
        self.end_manhole_cover_widget.setCurrentIndex(index)
        self.end_manhole_internal_defect_widget.setText(data['end_internal_defect'])
        self.end_manhole_external_defect_widget.setText(data['end_external_defect'])
        self.end_manhole_longitude_widget.setValue(data['end_manhole_longitude'])
        self.end_manhole_latitude_widget.setValue(data['end_manhole_latitude'])
        self.end_manhole_pipe_elevation_widget.setValue(data['end_pipe_elevation'])
        self.pipe_type_widget.clear()
        for i in data['pipe_type']:
            self.pipe_type_widget.addItem(i[1])
        index = 0
        for i in data['pipe_type']:
            if str(i[0]) == str(data['pipe_type_id']):
                break
            index += 1
        self.pipe_type_widget.setCurrentIndex(index)
        self.section_shape_widget.clear()
        for i in data['section_shape']:
            self.section_shape_widget.addItem(i[1])
        index = 0
        for i in data['section_shape']:
            if str(i[0]) == str(data['section_shape_id']):
                break
            index += 1
        self.section_shape_widget.setCurrentIndex(index)
        self.joint_form_widget.clear()
        for i in data['joint_form']:
            self.joint_form_widget.addItem(i[1])
        index = 0
        for i in data['joint_form']:
            if str(i[0]) == str(data['joint_form_id']):
                break
            index += 1
        self.joint_form_widget.setCurrentIndex(index)
        self.pipe_material_widget.clear()
        for i in data['pipe_material']:
            self.pipe_material_widget.addItem(i[1])
        index = 0
        for i in data['pipe_material']:
            if str(i[0]) == str(data['pipe_material_id']):
                break
            index += 1
        self.pipe_material_widget.setCurrentIndex(index)
        self.pipe_diameter_widget.setValue(data['pipe_diameter'])
        self.start_pipe_depth_widget.setValue(data['start_pipe_depth'])
        self.end_pipe_depth_widget.setValue(data['end_pipe_depth'])
        self.pipe_length_widget.setValue(data['pipe_length'])
        self.detection_length_widget.setValue(data['detection_length'])
        self.detection_direction_widget.clear()
        self.detection_direction_widget.addItem('顺流')
        self.detection_direction_widget.addItem('逆流')
        self.detection_direction_widget.setCurrentIndex(data['detection_direction'])
        if data['construction_year'] is not None:
            self.construction_year_widget.setDate(data['construction_year'])
        self.regional_importance_widget.clear()
        for i in data['regional']:
            self.regional_importance_widget.addItem(i[1])
        index = 0
        for i in data['regional']:
            if str(i[0]) == str(data['regional_importance_id']):
                break
            index += 1
        self.regional_importance_widget.setCurrentIndex(index)
        self.soil_widget.clear()
        for i in data['soil']:
            self.soil_widget.addItem(i[1])
        index = 0
        for i in data['soil']:
            if str(i[0]) == str(data['soil_id']):
                break
            index += 1
        self.soil_widget.setCurrentIndex(index)
        self.video_remark_widget.setText(data['video_remark'])

    def set_defect_info(self):
        if self.defect_id is None:
            self.defect_type_widget.clear()
            self.defect_grade_widget.clear()
            self.defect_attribute_widget.clear()
            self.defect_distance_widget.clear()
            self.defect_length_widget.clear()
            self.clock_start_widget.clear()
            self.clock_end_widget.clear()
            self.defect_date_widget.clear()
            self.defect_time_in_video_widget.clear()
            self.defect_remark_widget.clear()
            return
        data = self.main_window.db.get_defect_by_defect_id(self.defect_id)
        self.defect_data = data
        if data is None:
            return
        self.video_id = data['video_id']
        if self.all_defects is None:
            self.all_defects = self.main_window.db.get_all_defects(self.video_id)
        # find the defect_id's index in all_defects.
        index = 0
        for i in self.all_defects:
            if str(self.defect_id) == str(i['defect_id']):
                break
            index += 1
        self.current_frame_number = int(self.all_defects[index]['time_in_video'])
        try:
            self.show_one_frame()
        except:
            pass

        self.defect_type_widget.clear()
        for i in data['defect_type']:
            self.defect_type_widget.addItem(i[1])
        index = 0
        for i in data['defect_type']:
            if str(i[0]) == str(data['defect_type_id']):
                break
            index += 1
        self.defect_type_widget.setCurrentIndex(index)
        self.defect_attribute_widget.setText(data['defect_attribute'])
        self.defect_distance_widget.setValue(data['defect_distance'])
        self.defect_length_widget.setValue(data['defect_length'])
        self.clock_start_widget.setValue(data['clock_start'])
        self.clock_end_widget.setValue(data['clock_end'])
        self.defect_date_widget.setText(str(data['defect_date']))
        self.defect_time_in_video_widget.setText(str(data['time_in_video']))
        self.defect_remark_widget.setText(data['defect_remark'])

    def save_video_info(self):
        data = {}
        data['video_id'] = self.video_id
        data['staff_id'] = self.video_data['staff'][self.staff_widget.currentIndex()][0]
        data['road_name'] = self.road_name_widget.text()
        data['start_manhole_no'] = self.start_manhole_no_widget.text()
        data['start_manhole_type_id'] = self.video_data['manhole_type'][self.start_manhole_type_widget.currentIndex()][
            0]
        data['start_manhole_material_id'] = \
            self.video_data['manhole_material'][self.start_manhole_material_widget.currentIndex()][0]
        data['start_manhole_cover_id'] = \
            self.video_data['manhole_cover'][self.start_manhole_cover_widget.currentIndex()][0]
        data['start_internal_defect'] = self.start_manhole_internal_defect_widget.text()
        data['start_external_defect'] = self.start_manhole_external_defect_widget.text()
        data['start_manhole_longitude'] = self.start_manhole_longitude_widget.text()
        data['start_manhole_latitude'] = self.start_manhole_latitude_widget.text()
        data['start_pipe_elevation'] = self.start_manhole_pipe_elevation_widget.text()
        data['end_manhole_no'] = self.end_manhole_no_widget.text()
        data['end_manhole_type_id'] = self.video_data['manhole_type'][self.end_manhole_type_widget.currentIndex()][
            0]
        data['end_manhole_material_id'] = \
            self.video_data['manhole_material'][self.end_manhole_material_widget.currentIndex()][0]
        data['end_manhole_cover_id'] = self.video_data['manhole_cover'][self.end_manhole_cover_widget.currentIndex()][0]
        data['end_internal_defect'] = self.end_manhole_internal_defect_widget.text()
        data['end_external_defect'] = self.end_manhole_external_defect_widget.text()
        data['end_manhole_longitude'] = self.end_manhole_longitude_widget.text()
        data['end_manhole_latitude'] = self.end_manhole_latitude_widget.text()
        data['end_pipe_elevation'] = self.end_manhole_pipe_elevation_widget.text()
        data['pipe_type_id'] = self.video_data['pipe_type'][self.pipe_type_widget.currentIndex()][0]
        data['section_shape_id'] = self.video_data['section_shape'][self.section_shape_widget.currentIndex()][0]
        data['joint_form_id'] = self.video_data['joint_form'][self.joint_form_widget.currentIndex()][0]
        data['pipe_material_id'] = self.video_data['pipe_material'][self.pipe_material_widget.currentIndex()][0]
        data['pipe_diameter'] = self.pipe_diameter_widget.text()
        data['start_pipe_depth'] = self.start_pipe_depth_widget.text()
        data['end_pipe_depth'] = self.end_pipe_depth_widget.text()
        data['pipe_length'] = self.pipe_length_widget.text()
        data['detection_length'] = self.detection_length_widget.text()
        data['detection_direction'] = self.detection_direction_widget.currentIndex()
        data['construction_year'] = self.construction_year_widget.text()
        data['regional_importance_id'] = self.video_data['regional'][self.regional_importance_widget.currentIndex()][0]
        data['soil_id'] = self.video_data['soil'][self.soil_widget.currentIndex()][0]
        data['video_remark'] = self.video_remark_widget.toPlainText()
        flag = self.main_window.db.save_video(data)
        QtWidgets.QMessageBox.information(self, '提示', '保存成功' if flag else '保存失败')
        self.set_video_info()

    def save_defect_info(self):
        if self.defect_id is None:
            return
        data = {}
        data['defect_id'] = self.defect_id
        data['time_in_video'] = self.defect_time_in_video_widget.text()
        data['defect_type_id'] = self.defect_data['defect_type'][self.defect_type_widget.currentIndex()][0]
        data['defect_attribute'] = self.defect_attribute_widget.text()
        defect_grade_id_name = self.defect_grade_widget.currentText()
        data['defect_grade_id'] = 1
        for i in self.defect_data['defect_grade']:
            if i[1] == defect_grade_id_name:
                data['defect_grade_id'] = i[0]
        data['defect_distance'] = self.defect_distance_widget.text()
        data['defect_length'] = self.defect_length_widget.text()
        data['clock_start'] = self.clock_start_widget.text()
        data['clock_end'] = self.clock_end_widget.text()
        data['defect_date'] = self.defect_date_widget.text()
        data['defect_remark'] = self.defect_remark_widget.toPlainText()

        flag = self.main_window.db.save_defect(data)
        QtWidgets.QMessageBox.information(self, '提示', '保存成功' if flag else '保存失败')

    # choose different defect_type then get the corresponding defect_grade.
    def defect_type_changed(self):
        current_index = self.defect_type_widget.currentIndex()
        if len(self.defect_data['defect_type']) <= current_index:
            return
        defect_type_id = self.defect_data['defect_type'][current_index][0]
        # get defect_grade in current defect_type_id.
        current_defect_grade = [i for i in self.defect_data['defect_grade'] if str(i[2]) == str(defect_type_id)]
        self.defect_grade_widget.clear()
        for i in current_defect_grade:
            self.defect_grade_widget.addItem(i[1])
        index = 0
        for i in current_defect_grade:
            if str(i[0]) == str(self.defect_data['defect_grade_id']):
                break
            index += 1
        if index == len(current_defect_grade):
            index = 0
        self.defect_grade_widget.setCurrentIndex(index)

    # change window size event.
    def resizeEvent(self, event):
        image = self.image_to_determine_frame_size

        # set the image size to fit it width to the left_layout width.
        current_left_widget_width = self.width() - self.right_widget.width()  # the left widget width.
        self.new_frame_width = current_left_widget_width
        self.new_frame_height = current_left_widget_width / image.width() * image.height()
        self.show_one_frame()

    def play_video(self):
        self.is_playing = not self.is_playing
        if not self.is_playing:
            self.play_button.setIcon(QIcon(':/play'))
            self.timer.stop()
        else:
            self.play_button.setIcon(QIcon(':/pause'))
            self.timer.start()

    def previous_frame(self):
        if self.current_frame_number > 1:
            self.current_frame_number -= 1
        self.show_one_frame()

    def next_frame(self):
        if self.current_frame_number < self.total_frame_number:
            self.current_frame_number += 1
        self.show_one_frame()

    def next_defect(self):
        index = 0
        # find the defect_id's index in all_defects.
        for i in self.all_defects:
            if str(self.defect_id) == str(i['defect_id']):
                break
            index += 1
        # if didn't find the defect_id in all_defects.
        if index == len(self.all_defects):
            return
        index += 1
        if index == len(self.all_defects):
            index = 0
        self.defect_id = int(self.all_defects[index]['defect_id'])
        self.current_frame_number = int(self.all_defects[index]['time_in_video'])
        self.show_one_frame()
        self.set_defect_info()

    def previous_defect(self):
        index = 0
        for i in self.all_defects:
            if str(self.defect_id) == str(i['defect_id']):
                break
            index += 1
        # if didn't find the defect_id in all_defects.
        if index == len(self.all_defects):
            return
        index -= 1
        if index == -1:
            index = len(self.all_defects) - 1
        self.defect_id = int(self.all_defects[index]['defect_id'])
        self.current_frame_number = int(self.all_defects[index]['time_in_video'])
        self.show_one_frame()
        self.set_defect_info()

    def delete_defect(self):
        if self.defect_id is None:
            return
        flag = self.main_window.db.delete_defect(self.defect_id)
        if flag:
            QtWidgets.QMessageBox.information(self, '提示', '删除成功')
            # delete the defect in all_defects.
            index = 0
            for i in self.all_defects:
                if str(self.defect_id) == str(i['defect_id']):
                    break
                index += 1
            del self.all_defects[index]
            if len(self.all_defects) == 0:
                self.defect_id = None
            else:
                if index == len(self.all_defects):
                    index = 0
                self.defect_id = self.all_defects[index]['defect_id']
            self.set_defect_info()
        else:
            QtWidgets.QMessageBox.information(self, '提示', '删除失败')

    def initialize_video(self):
        try:
            self.video = cv2.VideoCapture()
            self.video.open(self.video_data['video_name'])
            self.total_frame_number = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))
            self.fps = self.video.get(cv2.CAP_PROP_FPS)
            self.timer.set_fps(self.fps)
            self.slider.setMinimum(1)
            self.slider.setMaximum(self.total_frame_number)

            self.image_to_determine_frame_size = self.get_current_frame()
            self.resizeEvent(None)
            self.show_one_frame()
        except:
            print('initialize video failed.')

    def get_current_frame(self):
        # get the current frame.
        self.video.set(cv2.CAP_PROP_POS_FRAMES, self.current_frame_number)
        flag, img = self.video.read()  # if read successful, then flag is True.
        height, width = img.shape[:2]
        if img.ndim == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        elif img.ndim == 2:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        img = QImage(img.data, width, height, QImage.Format_RGB888)
        # when fromImage(),there is a bug when load image from some videos.
        # for now, we can play avi and some mp4,other mp4 can not play.
        # don't know why.
        return QPixmap.fromImage(img, QtCore.Qt.AutoColor)

    def show_one_frame(self):
        self.slider.setValue(self.current_frame_number)
        hour_minute_second = self.int_to_time(self.current_frame_number) + '/' + self.int_to_time(
            self.total_frame_number)
        self.show_frame_label.setText(
            str(self.current_frame_number) + '/' + str(self.total_frame_number) + '帧' + '\n' + hour_minute_second)
        if self.current_frame_number == self.total_frame_number:
            self.current_frame_number = 1
            self.play_video()
            return
        image = self.get_current_frame()
        image = image.scaled(self.new_frame_width, self.new_frame_height)
        self.video_frame.setPixmap(image)
        if self.is_playing and self.current_frame_number < self.total_frame_number:
            self.current_frame_number += 1

    def slide_frame(self):
        self.current_frame_number = self.slider.value()
        if not self.is_playing:
            self.show_one_frame()

    def int_to_time(self, number):
        seconds = int(number / self.fps)
        hours = seconds // 3600
        seconds -= hours * 3600
        minutes = seconds // 60
        seconds -= minutes * 60
        return "%02d:%02d:%02d" % (hours, minutes, seconds)

    def sort_defects_by_time(self):
        def cmp(x, y):
            if x['time_in_video'] < y['time_in_video']:
                return -1
            return 0

        self.all_defects = sorted(self.all_defects, key=functools.cmp_to_key(cmp))

    def draw_all_defects(self):
        pass

    def manual(self):
        if self.is_playing:
            self.play_video()
        current_frame_number = self.current_frame_number
        self.edit_defect_button_clicked()
        self.current_frame_number = current_frame_number
        self.show_one_frame()
        data = {}
        data['video_id'] = self.video_id
        data['time_in_video'] = self.current_frame_number
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        data['defect_date'] = current_time
        self.defect_date_widget.setText(data['defect_date'])
        self.defect_time_in_video_widget.setText(str(data['time_in_video']))
        new_defect = self.main_window.db.add_defect(data)
        if new_defect is None:
            QtWidgets.QMessageBox.information(self, '提示', '标记缺陷失败')
            return
        self.all_defects.append(new_defect)
        self.sort_defects_by_time()

    def auto(self):
        # the detection method should return a list which each item in it represents a defect frame.
        print(sorted([random.randint(1, self.total_frame_number) for i in range(10)]))


"""
Reference:
https://blog.csdn.net/aaa_a_b_c/article/details/80367147
https://blog.csdn.net/qq_28622733/article/details/101426120
"""


class Communicate(QObject):
    signal = QtCore.pyqtSignal(str)


class VideoTimer(QThread):

    def __init__(self, fps=24):
        QThread.__init__(self)
        self.stopped = False
        self.fps = fps
        self.timeSignal = Communicate()
        self.mutex = QtCore.QMutex()

    def run(self):
        with QMutexLocker(self.mutex):
            self.stopped = False
        while True:
            if self.stopped:
                return
            self.timeSignal.signal.emit('')
            time.sleep(1 / self.fps)

    def stop(self):
        with QMutexLocker(self.mutex):
            self.stopped = True

    def is_stopped(self):
        with QMutexLocker(self.mutex):
            return self.stopped

    def set_fps(self, fps):
        self.fps = fps

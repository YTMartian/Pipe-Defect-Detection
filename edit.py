from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QScrollArea, QMainWindow, QHBoxLayout, QFormLayout, QLineEdit, \
    QComboBox, QDateEdit, QTextEdit, QSpinBox, QDoubleSpinBox


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
        self.right_widget.setFixedWidth(390)
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
        self.edit_video_scroll_area_form.addRow(self.record_date_label, self.record_date_widget)
        self.import_date_label, self.import_date_widget = QLabel(), QLineEdit()
        self.import_date_label.setText('导入日期')
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
        self.edit_video_scroll_area_form.addRow(self.start_manhole_longitude_label, self.start_manhole_longitude_widget)
        self.start_manhole_latitude_label, self.start_manhole_latitude_widget = QLabel(), QDoubleSpinBox()
        self.start_manhole_latitude_label.setText('起始井纬度坐标')
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
        self.edit_video_scroll_area_form.addRow(self.end_manhole_longitude_label, self.end_manhole_longitude_widget)
        self.end_manhole_latitude_label, self.end_manhole_latitude_widget = QLabel(), QDoubleSpinBox()
        self.end_manhole_latitude_label.setText('结束井纬度坐标')
        self.edit_video_scroll_area_form.addRow(self.end_manhole_latitude_label, self.end_manhole_latitude_widget)
        self.end_manhole_pipe_elevation_label, self.end_manhole_pipe_elevation_widget = QLabel(), QDoubleSpinBox()
        self.end_manhole_pipe_elevation_label.setText('结束井高程')
        self.edit_video_scroll_area_form.addRow(self.end_manhole_pipe_elevation_label,
                                                self.end_manhole_pipe_elevation_widget)
        self.pipe_type_label, self.pipe_type_widget = QLabel(), QComboBox()
        self.pipe_type_label.setText('管道类型')
        self.edit_video_scroll_area_form.addRow(self.pipe_type_label, self.pipe_type_widget)
        self.section_shape_label, self.section_shape_widget = QLabel(), QLineEdit()
        self.section_shape_label.setText('截面形状')
        self.edit_video_scroll_area_form.addRow(self.section_shape_label, self.section_shape_widget)
        self.joint_form_label, self.joint_form_widget = QLabel(), QLineEdit()
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
        self.edit_defect_scroll_area_form.addRow(self.defect_type_label, self.defect_type_widget)
        self.defect_attribute_label, self.defect_attribute_widget = QLabel(), QLineEdit()
        self.defect_attribute_label.setText('缺陷性质')
        self.edit_defect_scroll_area_form.addRow(self.defect_attribute_label, self.defect_attribute_widget)
        self.defect_grade_label, self.defect_grade_widget = QLabel(), QComboBox()
        self.defect_grade_label.setText('缺陷级别')
        self.edit_defect_scroll_area_form.addRow(self.defect_grade_label, self.defect_grade_widget)
        self.defect_distance_label, self.defect_distance_widget = QLabel(), QDoubleSpinBox()
        self.defect_distance_label.setText('缺陷距离(m)')
        self.edit_defect_scroll_area_form.addRow(self.defect_distance_label, self.defect_distance_widget)
        self.defect_length_label, self.defect_length_widget = QLabel(), QDoubleSpinBox()
        self.defect_length_label.setText('缺陷长度(m)')
        self.edit_defect_scroll_area_form.addRow(self.defect_length_label, self.defect_length_widget)
        self.clock_start_label, self.clock_start_widget = QLabel(), QSpinBox()
        self.clock_start_label.setText('环向起点')
        self.edit_defect_scroll_area_form.addRow(self.clock_start_label, self.clock_start_widget)
        self.clock_end_label, self.clock_end_widget = QLabel(), QSpinBox()
        self.clock_end_label.setText('环向终点')
        self.edit_defect_scroll_area_form.addRow(self.clock_end_label, self.clock_end_widget)
        self.defect_date_label, self.defect_date_widget = QLabel(), QDateEdit()
        self.defect_date_label.setText('判读日期')
        self.edit_defect_scroll_area_form.addRow(self.defect_date_label, self.defect_date_widget)
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
        self.project_staff_widget.setReadOnly(True)
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
        self.hide_something()
        self.set_project_info()

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
            self.edit_video_scroll_area.setVisible(False)
            self.edit_defect_scroll_area.setVisible(False)
            self.project_detailed_scroll_area.setVisible(True)
        elif self.mode == self.is_edit_video:
            self.save_button.setVisible(True)
            self.cancel_button.setVisible(True)
            self.edit_video_scroll_area.setVisible(True)
            self.edit_defect_scroll_area.setVisible(False)
            self.project_detailed_scroll_area.setVisible(False)
        elif self.mode == self.is_edit_defect:
            self.save_button.setVisible(True)
            self.cancel_button.setVisible(True)
            self.edit_video_scroll_area.setVisible(False)
            self.edit_defect_scroll_area.setVisible(True)
            self.project_detailed_scroll_area.setVisible(False)

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

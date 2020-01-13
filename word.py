from docxtpl import DocxTemplate
from tkinter import filedialog
from tkinter import *
import datetime
import time


class Word:
    def __init__(self, db):
        self.db = db
        self.doc = DocxTemplate('template.docx')
        self.path = str(time.time()) + '.docx'

    def generate(self, project_id):
        try:
            self.generate_word(project_id)
            return True
        except:
            print('generate word failed.')
            return False

    def generate_word(self, project_id):
        root = Tk()
        root.withdraw()
        self.path = filedialog.asksaveasfilename(title=u'保存文件', filetypes=[("Word文档", ".docx")])
        self.path = self.path + '.docx'
        project_detailed_data = self.db.get_one_project_detailed(project_id)
        all_tables = self.db.get_all_tables()
        all_videos = self.db.get_video(project_id)
        current_year = datetime.date.today().year
        current_month = '%02d' % datetime.date.today().month
        current_day = '%02d' % datetime.date.today().day
        # find the staff_name.
        staff_name = [i[1] for i in all_tables['staff'] if i[0] == project_detailed_data[4]][0]
        # get start_record_date and end_record_date.
        record_dates = [i[6].split(' ')[0] for i in all_videos]
        record_dates = sorted(record_dates)
        start_record_date = record_dates[0]
        end_record_date = record_dates[len(record_dates) - 1]
        # get project_statistic.
        all_project_statistic = self.db.get_project_statistic()
        project_statistic = [i for i in all_project_statistic if i[0] == project_id][0]
        detection_method = [i[1] for i in all_tables['detection'] if i[0] == project_detailed_data[12]][0]
        move_method = [i[1] for i in all_tables['move'] if i[0] == project_detailed_data[13]][0]
        plugging_method = [i[1] for i in all_tables['plugging'] if i[0] == project_detailed_data[14]][0]
        drainage_method = [i[1] for i in all_tables['drainage'] if i[0] == project_detailed_data[15]][0]
        dredging_method = [i[1] for i in all_tables['dredging'] if i[0] == project_detailed_data[16]][0]
        pipes = project_statistic[-1]
        manholes = self.db.get_all_manholes_in_project(project_id)
        pipe_defect_summary = self.db.get_pipe_defect_summary(project_id)
        videos = self.db.get_videos(project_id)
        context = {
            'project_name': project_detailed_data[2],
            'project_no': project_detailed_data[1],
            'project_address': project_detailed_data[3],
            'requester_unit': project_detailed_data[7],
            'supervisory_unit': project_detailed_data[11],
            'construction_unit': project_detailed_data[8],
            'design_unit': project_detailed_data[9],
            'build_unit': project_detailed_data[10],
            'report_no': project_detailed_data[6],
            'staff_name': staff_name,
            'current_year': current_year,
            'current_month': current_month,
            'current_day': current_day,
            'start_record_date': start_record_date,
            'end_record_date': end_record_date,
            'video_amount': project_statistic[6],
            'pipe_amount': project_statistic[7],
            'pipe_total_length': project_statistic[8],
            'pipe_total_detection_length':project_statistic[11],
            'detection_method': detection_method,
            'detection_equipment': project_detailed_data[17],
            'move_method': move_method,
            'plugging_method': plugging_method,
            'drainage_method': drainage_method,
            'dredging_method': dredging_method,
            'pipes': pipes,
            'manholes': manholes,
            'pipe_defect_summary': pipe_defect_summary,
            'videos': videos
        }
        self.doc.render(context)
        self.doc.save(self.path)

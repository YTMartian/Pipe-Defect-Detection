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
        current_year = datetime.date.today().year
        current_month = '%02d' % datetime.date.today().month
        current_day = '%02d' % datetime.date.today().day
        context = {
            'project_name': project_detailed_data[2],
            'project_no': project_detailed_data[1],
            'project_address': project_detailed_data[3],
            'requester_unit': project_detailed_data[7],
            'supervisory_unit': project_detailed_data[11],
            'report_no': project_detailed_data[6],
            'staff_name': project_detailed_data[4],
            'current_year': current_year,
            'current_month': current_month,
            'current_day': current_day
        }
        self.doc.render(context)
        self.doc.save(self.path)

from docxtpl import DocxTemplate, InlineImage
from matplotlib import font_manager as fm
import matplotlib.pyplot as plt
from tkinter import filedialog
from docx.shared import Mm
from matplotlib import cm
from tkinter import *
import numpy as np
import matplotlib
import datetime
import shutil
import time
import cv2
import os

'''
auto update content table:https://blog.csdn.net/weixin_42670653/article/details/81476147
'''

font = {
    'family': 'SimHei',
    'weight': 'bold',
    'size': 12
}
matplotlib.rc("font", **font)


class Word:
    def __init__(self, db):
        self.db = db
        self.doc = DocxTemplate('template2.docx')
        self.path = str(time.time()) + '.docx'
        self.pic_path = './images/'

    def generate(self, project_id):
        try:
            return self.generate_word(project_id)
        except Exception as e:
            print('generate word failed.')
            print(e)
            return False

    def generate_word(self, project_id):
        root = Tk()
        root.withdraw()
        self.path = filedialog.asksaveasfilename(title=u'保存文件', filetypes=[("Word文档", ".docx")])
        if len(self.path) == 0:
            return False
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
        # save the pictures.
        if os.path.exists(self.pic_path):
            shutil.rmtree(self.pic_path, True)
        # em...just to give computer some time to delete the images.
        # or it will not find the path...
        time.sleep(1)
        os.mkdir(self.pic_path)
        for video in videos:
            cap = cv2.VideoCapture()
            cap.open(video['video_name'])
            for defect in video['defects']:
                cap.set(cv2.CAP_PROP_POS_FRAMES, int(defect['time_in_video']))
                flag, img = cap.read()  # if read successful, then flag is True.
                if not flag:
                    print('save image {} failed.'.format(video['video_file_name'] + '-' + defect['time_in_video']))
                    continue
                # print(self.pic_path + video['video_file_name'] + '-' + defect['time_in_video'])
                cv2.imwrite(self.pic_path + video['video_file_name'] + '-' + defect['time_in_video'] + '.jpg', img)
            cap.release()

        # generate pipe_defect_summary statistic chart.
        structure_defect_names = ['支管暗接', '变形', '错口', '异物穿入', '腐蚀', '破裂', '起伏', '渗漏', '脱节', '接口材料脱落']
        structure_defect_count = [pipe_defect_summary['defects_count']['AJtotal'],
                                  pipe_defect_summary['defects_count']['BXtotal'],
                                  pipe_defect_summary['defects_count']['CKtotal'],
                                  pipe_defect_summary['defects_count']['CRtotal'],
                                  pipe_defect_summary['defects_count']['FStotal'],
                                  pipe_defect_summary['defects_count']['PLtotal'],
                                  pipe_defect_summary['defects_count']['QFtotal'],
                                  pipe_defect_summary['defects_count']['SLtotal'],
                                  pipe_defect_summary['defects_count']['TJtotal'],
                                  pipe_defect_summary['defects_count']['TLtotal']]
        labels = []
        sizes = []
        total = sum(structure_defect_count)
        for i in range(len(structure_defect_names)):
            if structure_defect_count[i] == 0:
                continue
            labels.append(structure_defect_names[i])
            sizes.append(structure_defect_count[i] / total)
        fig, axes = plt.subplots(figsize=(10, 7), ncols=2)  # 1000x500
        ax1, ax2 = axes.ravel()
        colors = cm.rainbow(np.arange(len(sizes)) / len(sizes))  # colormaps: Paired, autumn, rainbow, gray,spring,Darks
        patches, texts, autotexts = ax1.pie(sizes, labels=labels, autopct='%1.0f%%',
                                            shadow=False, startangle=170, colors=colors)
        ax1.axis('equal')
        proptease = fm.FontProperties()
        proptease.set_size('medium')
        # font size include: ‘xx-small’,x-small’,'small’,'medium’,‘large’,‘x-large’,‘xx-large’ or number, e.g. '12'
        plt.setp(autotexts, fontproperties=proptease)
        plt.setp(texts, fontproperties=proptease)

        ax2.axis('off')
        ax2.legend(patches, labels, loc='center')

        plt.tight_layout()
        plt.savefig(self.pic_path + 'structure_defect_summary_statistic.png')

        def get_structure_grade_total(i):
            i = str(i)
            return sum(
                [pipe_defect_summary['defects_count']['AJ' + i],
                 pipe_defect_summary['defects_count']['BX' + i],
                 pipe_defect_summary['defects_count']['CK' + i],
                 pipe_defect_summary['defects_count']['CR' + i],
                 pipe_defect_summary['defects_count']['FS' + i],
                 pipe_defect_summary['defects_count']['PL' + i],
                 pipe_defect_summary['defects_count']['QF' + i],
                 pipe_defect_summary['defects_count']['SL' + i],
                 pipe_defect_summary['defects_count']['TJ' + i],
                 pipe_defect_summary['defects_count']['TL' + i]])

        pipe_defect_summary['defects_count']['structure_grade1_total'] = get_structure_grade_total(1)
        pipe_defect_summary['defects_count']['structure_grade2_total'] = get_structure_grade_total(2)
        pipe_defect_summary['defects_count']['structure_grade3_total'] = get_structure_grade_total(3)
        pipe_defect_summary['defects_count']['structure_grade4_total'] = get_structure_grade_total(4)
        pipe_defect_summary['defects_count']['structure_grade_total'] = sum(
            [pipe_defect_summary['defects_count']['structure_grade{}_total'.format(i)] for i in range(1, 5)])
        function_defect_names = ['沉积', '残墙、坝根', '浮渣', '结垢', '树根', '障碍物']
        function_defect_count = [pipe_defect_summary['defects_count']['CJtotal'],
                                 pipe_defect_summary['defects_count']['CQtotal'],
                                 pipe_defect_summary['defects_count']['FZtotal'],
                                 pipe_defect_summary['defects_count']['JGtotal'],
                                 pipe_defect_summary['defects_count']['SGtotal'],
                                 pipe_defect_summary['defects_count']['ZWtotal']]
        labels.clear()
        sizes.clear()
        total = sum(function_defect_count)
        for i in range(len(function_defect_names)):
            if function_defect_count[i] == 0:
                continue
            labels.append(function_defect_names[i])
            sizes.append(function_defect_count[i] / total)
        fig, axes = plt.subplots(figsize=(10, 7), ncols=2)  # 1000x500
        ax1, ax2 = axes.ravel()
        colors = cm.rainbow(np.arange(len(sizes)) / len(sizes))  # colormaps: Paired, autumn, rainbow, gray,spring,Darks
        patches, texts, autotexts = ax1.pie(sizes, labels=labels, autopct='%1.0f%%',
                                            shadow=False, startangle=170, colors=colors)
        ax1.axis('equal')
        proptease = fm.FontProperties()
        proptease.set_size('medium')
        # font size include: ‘xx-small’,x-small’,'small’,'medium’,‘large’,‘x-large’,‘xx-large’ or number, e.g. '12'
        plt.setp(autotexts, fontproperties=proptease)
        plt.setp(texts, fontproperties=proptease)

        ax2.axis('off')
        ax2.legend(patches, labels, loc='center')

        plt.tight_layout()
        plt.savefig(self.pic_path + 'function_defect_summary_statistic.png')

        def get_function_grade_total(i):
            i = str(i)
            return sum(
                [pipe_defect_summary['defects_count']['CJ' + i],
                 pipe_defect_summary['defects_count']['CQ' + i],
                 pipe_defect_summary['defects_count']['FZ' + i],
                 pipe_defect_summary['defects_count']['JG' + i],
                 pipe_defect_summary['defects_count']['SG' + i],
                 pipe_defect_summary['defects_count']['ZW' + i],
                 pipe_defect_summary['defects_count']['QF' + i],
                 pipe_defect_summary['defects_count']['SL' + i],
                 pipe_defect_summary['defects_count']['TJ' + i],
                 pipe_defect_summary['defects_count']['TL' + i]])

        pipe_defect_summary['defects_count']['function_grade1_total'] = get_function_grade_total(1)
        pipe_defect_summary['defects_count']['function_grade2_total'] = get_function_grade_total(2)
        pipe_defect_summary['defects_count']['function_grade3_total'] = get_function_grade_total(3)
        pipe_defect_summary['defects_count']['function_grade4_total'] = get_function_grade_total(4)
        pipe_defect_summary['defects_count']['function_grade_total'] = sum(
            [pipe_defect_summary['defects_count']['function_grade{}_total'.format(i)] for i in range(1, 5)])

        structure_defect_summary_statistic = InlineImage(self.doc,
                                                         self.pic_path + 'structure_defect_summary_statistic.png',
                                                         height=Mm(120))
        function_defect_summary_statistic = InlineImage(self.doc,
                                                        self.pic_path + 'function_defect_summary_statistic.png',
                                                        height=Mm(120))

        for i in range(len(videos)):
            videos[i]['images'] = []
            temp = {}
            for j in range(0, len(videos[i]['defects']), 2):
                temp['left_number'] = j + 1
                temp['left_image'] = videos[i]['video_file_name'] + '-' + videos[i]['defects'][j][
                    'time_in_video'] + '.jpg'
                # add image.
                # https://docxtpl.readthedocs.io/en/latest/
                temp['left_image'] = InlineImage(self.doc, os.getcwd() + self.pic_path[1:] + temp['left_image'],
                                                 height=Mm(60))
                if j + 1 < len(videos[i]['defects']):
                    temp['right_image'] = videos[i]['video_file_name'] + '-' + videos[i]['defects'][j + 1][
                        'time_in_video'] + '.jpg'
                    temp['right_image'] = InlineImage(self.doc, os.getcwd() + self.pic_path[1:] + temp['right_image'],
                                                      height=Mm(60))
                else:
                    temp['right_image'] = ''
                temp['right_number'] = j + 2
                videos[i]['images'].append(temp.copy())

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
            'pipe_total_detection_length': project_statistic[11],
            'detection_method': detection_method,
            'detection_equipment': project_detailed_data[17],
            'move_method': move_method,
            'plugging_method': plugging_method,
            'drainage_method': drainage_method,
            'dredging_method': dredging_method,
            'pipes': pipes,
            'manholes': manholes,
            'pipe_defect_summary': pipe_defect_summary,
            'videos': videos,
            'structure_defect_summary_statistic': structure_defect_summary_statistic,
            'function_defect_summary_statistic': function_defect_summary_statistic
        }
        self.doc.render(context)
        self.doc.save(self.path)
        return True

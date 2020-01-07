from datetime import datetime

import pymysql
import time
import os


class Database:
    def __init__(self):
        self.conn = None
        self.host = 'localhost'
        self.port = 3306
        self.user = 'root'
        self.password = 'root'
        self.database = 'pipe_defect_detection_system'
        try:
            self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password,
                                        database=self.database)
        except:
            print('error code 2')
        print('connect database successful.')

    def __del__(self):
        try:
            self.conn.close()
        except Exception as e:
            print(e)

    # get name behind the id.
    def get_name(self, table, id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM {0} WHERE {0}_id = {1}".format(table, id))
        self.conn.commit()
        data = cursor.fetchall()
        return data[0][1]

    def get_value(self, sql):
        cursor = self.conn.cursor()
        cursor.execute(sql)
        self.conn.commit()
        data = cursor.fetchall()
        return data[0][0]

    def get_project_detailed(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM project")
        self.conn.commit()
        data = cursor.fetchall()
        cursor.close()
        res = []
        for i in data:
            temp = [str(i[j]) for j in range(0, 12)]  # the first item is project_id, we need to record it.
            detection_id = i[12]
            move_id = i[13]
            plugging_id = i[14]
            drainage_id = i[15]
            dredging_id = i[16]
            staff_id = temp[4]
            temp.append(self.get_name('detection', detection_id))
            temp.append(self.get_name('move', move_id))
            temp.append(self.get_name('plugging', plugging_id))
            temp.append(self.get_name('drainage', drainage_id))
            temp.append(self.get_name('dredging', dredging_id))
            temp[4] = self.get_name('staff', staff_id)
            res.append(temp.copy())
        return res

    def get_one_project_detailed(self, project_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM project WHERE project_id = {}".format(project_id))
        self.conn.commit()
        data = cursor.fetchall()
        cursor.close()
        res = []
        res = [str(data[0][i]) for i in range(0, 16)]
        return res

    def get_project_statistic(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM project")
        self.conn.commit()
        data = cursor.fetchall()
        cursor.close()
        res = []
        for i in data:
            temp = [str(i[j]) for j in range(0, 6)]  # the first item is project_id, we need to record it.
            staff_id = temp[4]
            project_id = str(i[0])
            temp[4] = self.get_name('staff', staff_id)
            # get video amount.
            video_amount = self.get_value("SELECT COUNT(*) FROM project_video WHERE project_id={}".format(project_id))
            temp.append(str(video_amount))
            # get pipe amount.
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM project_video WHERE project_id={}".format(project_id))
            self.conn.commit()
            data = cursor.fetchall()
            video_ids = [i[1] for i in data]  # get now project's all video's id.
            pipe_amount = 0
            for video_id in video_ids:
                cursor.execute("SELECT start_manhole_id,end_manhole_id FROM video WHERE video_id={}".format(video_id))
                self.conn.commit()
                data = cursor.fetchall()
                start_manhole_id = data[0][0]
                end_manhole_id = data[0][1]
                cursor.execute("SELECT manhole_no FROM manhole WHERE manhole_id in ({},{})".format(start_manhole_id,
                                                                                                   end_manhole_id))
                self.conn.commit()
                data = cursor.fetchall()
                start_manhole_no = data[0][0]
                end_manhole_no = data[1][0]
                if start_manhole_no is None or end_manhole_no is None:
                    continue
                pipe_amount += 1
            temp.append(str(pipe_amount))
            # get pipe total length.
            pipe_total_length = self.get_value(
                "SELECT SUM(pipe_length) FROM  video WHERE video_id IN (SELECT video_id FROM project_video WHERE project_id = {})".format(
                    project_id))
            if pipe_total_length is None:
                pipe_total_length = 0
            temp.append(str(pipe_total_length))
            # get standard sum.
            standard_sum = self.get_value(
                "SELECT COUNT(*) FROM  defect WHERE video_id IN (SELECT video_id FROM project_video WHERE project_id = {}) ".format(
                    project_id))
            temp.append(str(standard_sum))
            # get defect sum.
            defect_sum = standard_sum  # maybe they are the same things?
            temp.append(str(defect_sum))
            res.append(temp.copy())
        return res

    def get_video(self, project_id):
        cursor = self.conn.cursor()
        if project_id is None:
            cursor.execute(
                "SELECT video_id,road_name,start_manhole_id,end_manhole_id,pipe_type_id,pipe_material_id,video_name,record_date,import_date FROM video")
        else:
            cursor.execute(
                "SELECT video_id,road_name,start_manhole_id,end_manhole_id,pipe_type_id,pipe_material_id,video_name,record_date,import_date FROM video WHERE video_id IN (SELECT video_id FROM project_video WHERE project_id = {})".format(
                    project_id))
        self.conn.commit()
        data = cursor.fetchall()
        cursor.close()
        res = []
        for i in data:
            temp = []
            print(len(i))
            temp.append(str(i[0]))  # video_id.
            temp.append(str(i[1]))  # road_name.
            start_manhole_id = str(i[2])
            end_manhole_id = str(i[3])
            start_manhole_no = self.get_name('manhole', start_manhole_id)
            end_manhole_no = self.get_name('manhole', end_manhole_id)
            temp.append(str(start_manhole_no) + '~' + str(end_manhole_no))  # pipe number.
            temp.append(str(i[4]))  # pipe_type_id.
            temp.append(str(i[5]))  # pipe_material_id.
            temp.append(str(i[6]))  # video_name.
            temp.append(str(i[7]))  # record_date.
            temp.append(str(i[8]))  # import_date.
            temp[3] = self.get_name('pipe_type', temp[3])
            temp[4] = self.get_name('pipe_material', temp[4])
            defect_amount = self.get_value("SELECT COUNT(*) FROM defect WHERE video_id = {}".format(temp[0]))
            temp.append(str(defect_amount))

            res.append(temp.copy())
        return res

    def get_defect(self, video_id):
        cursor = self.conn.cursor()
        if video_id is None:
            cursor.execute("SELECT * FROM defect")
        else:
            cursor.execute("SELECT * FROM defect WHERE video_id = {}".format(video_id))
        self.conn.commit()
        data = cursor.fetchall()
        cursor.close()
        res = []
        for i in data:
            temp = []
            temp.append(str(i[0]))  # defect_id.
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM video WHERE video_id = {}".format(str(i[1])))
            self.conn.commit()
            video_data = cursor.fetchall()
            temp.append(str(video_data[0][3]))  # road_name.
            temp.append(str(video_data[0][4]) + ' ~ ' + str(video_data[0][13]))  # pipe number.
            temp.append(str(video_data[0][24]))  # pipe_type_id.
            temp.append(str(video_data[0][27]))  # pipe_material_id.
            temp.append(str(video_data[0][28]))  # pipe_diameter.
            temp.append(str(i[3]))  # defect_type_id.
            temp.append(str(i[8]))  # defect_grade_id.
            temp.append(str(i[11]))  # defect_attribute.
            temp.append(str(i[2]))  # time_in_video.
            temp.append(str(video_data[0][2]))  # record_date.
            temp.append(str(i[10]))  # interpretation_date.

            temp[3] = self.get_name('pipe_type', temp[3])
            temp[4] = self.get_name('pipe_material', temp[4])
            temp[6] = self.get_name('defect_type', temp[6])
            temp[7] = self.get_name('defect_grade', temp[7])

            res.append(temp.copy())
        return res

    # get id and name of staff,detection,move,plugging,drainage,dredging.
    def get_add_project_tables(self, table):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM {}".format(table))
        self.conn.commit()
        data = cursor.fetchall()
        cursor.close()
        res = []
        for i in data:
            temp = []
            temp.append(str(i[0]))  # id.
            temp.append(str(i[1]))  # name.
            res.append(temp.copy())
        return res

    # if project_id is None, then it is add project,or it is edit project.
    def add_project(self, data, project_id):
        if project_id is not None:
            sql = "UPDATE project SET project_no='{}',project_name='{}',project_address='{}',staff_id={},start_date='{}',report_no='{}',requester_unit='{}',construction_unit='{}',design_unit='{}',build_unit='{}',supervisory_unit='{}',detection_id={},move_id={},plugging_id={},drainage_id={},dredging_id={} WHERE project_id={}".format(
                data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10],
                data[11], data[12], data[13], data[14], data[15], project_id)
        else:
            sql = "INSERT INTO project(project_no,project_name,project_address,staff_id,start_date,report_no,requester_unit,construction_unit,design_unit,build_unit,supervisory_unit,detection_id,move_id,plugging_id,drainage_id,dredging_id) VALUES('{}','{}','{}',{},'{}','{}','{}','{}','{}','{}','{}',{},{},{},{},{})".format(
                data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10],
                data[11], data[12], data[13], data[14], data[15])
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            self.conn.commit()
            cursor.close()
            if project_id is None:
                print('insert into project successful.')
            else:
                print('update project successful.')
        except:
            if project_id is None:
                print('insert into project failed.')
            else:
                print('update project failed.')

    def delete_project(self, project_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT video_id FROM project_video WHERE project_id={}".format(project_id))
            self.conn.commit()
            data = cursor.fetchall()
            video_ids = [i[0] for i in data]
            cursor.close()
            for video_id in video_ids:
                self.delete_video(video_id)
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM project WHERE project_id={}".format(project_id))
            self.conn.commit()
            cursor.close()
            print('delete project successful.')
        except:
            print('delete project failed.')

    def delete_defect(self, defect_id):
        sql = "DELETE FROM defect WHERE defect_id={}".format(defect_id)
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            self.conn.commit()
            cursor.close()
            print('delete defect successful.')
        except:
            print('delete defect failed.')

    def add_video(self, project_id, video_name):
        try:
            record_date = os.path.getmtime(video_name)  # get file modified time.
        except:
            print('import video failed.')
            return
        # should add start and end manholes to manhole table.
        try:
            cursor = self.conn.cursor()
            cursor.execute('INSERT INTO manhole VALUES()')
            start_manhole_id = cursor.lastrowid  # get the latest manhole id.
            cursor.execute('INSERT INTO manhole VALUES()')
            end_manhole_id = cursor.lastrowid
            self.conn.commit()
            cursor.close()
            print('insert into manhole successful.')
        except:
            print('insert into manhole failed.')

        record_date = time.localtime(record_date)
        record_date = time.strftime("%Y-%m-%d %H:%M:%S", record_date)
        import_date = time.time()
        import_date = time.localtime(import_date)
        import_date = time.strftime("%Y-%m-%d %H:%M:%S", import_date)
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO video(record_date,import_date,video_name,start_manhole_id,end_manhole_id) VALUES('{}','{}','{}',{},{})".format(
                    record_date,
                    import_date,
                    video_name, start_manhole_id, end_manhole_id))
            self.conn.commit()
            video_id = cursor.lastrowid  # get latest id.
            cursor.execute("INSERT INTO project_video VALUES({},{})".format(project_id, video_id))
            self.conn.commit()
            cursor.close()
            print('insert into video successful.')
        except:
            print('insert into video failed.')

    def delete_video(self, video_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT start_manhole_id,end_manhole_id FROM video WHERE video_id={}".format(video_id))
            self.conn.commit()
            data = cursor.fetchall()
            start_manhole_id = data[0][0]
            end_manhole_id = data[0][1]
            cursor.execute(
                "DELETE FROM manhole WHERE manhole_id={} OR manhole_id={}".format(start_manhole_id, end_manhole_id))
            self.conn.commit()
            cursor.execute("DELETE FROM video WHERE video_id={}".format(video_id))
            self.conn.commit()
            cursor.close()
            print('delete video successful.')
        except:
            print('delete video failed.')

    def update_video(self, video_id, data):
        pass

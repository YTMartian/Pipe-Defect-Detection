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
        res = [str(data[0][i]) for i in range(0, 17)]
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
            cursor.execute(
                "SELECT road_name,start_manhole_id,end_manhole_id,pipe_type_id,pipe_material_id,pipe_diameter,record_date FROM video WHERE video_id = {}".format(
                    str(i[1])))
            self.conn.commit()
            video_data = cursor.fetchall()
            temp.append(str(video_data[0][0]))  # road_name.
            start_manhole_id = str(video_data[0][1])
            end_manhole_id = str(video_data[0][2])
            start_manhole_no = self.get_name('manhole', start_manhole_id)
            end_manhole_no = self.get_name('manhole', end_manhole_id)
            temp.append(str(start_manhole_no) + '~' + str(end_manhole_no))  # pipe number.
            temp.append(str(video_data[0][3]))  # pipe_type_id.
            temp.append(str(video_data[0][4]))  # pipe_material_id.
            temp.append(str(video_data[0][5]))  # pipe_diameter.
            temp.append(str(i[3]))  # defect_type_id.
            temp.append(str(i[8]))  # defect_grade_id.
            temp.append(str(i[11]))  # defect_attribute.
            temp.append(str(i[2]))  # time_in_video.
            temp.append(str(video_data[0][6]))  # record_date.
            temp.append(str(i[10]))  # interpretation_date.

            temp[3] = self.get_name('pipe_type', temp[3])
            temp[4] = self.get_name('pipe_material', temp[4])
            temp[6] = self.get_name('defect_type', temp[6])
            temp[7] = self.get_name('defect_grade', temp[7])

            res.append(temp.copy())
        return res

    # get id and name of staff,detection,move,plugging,drainage,dredging.
    # also tables in video.
    def get_one_table(self, table):
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
            if len(i) > 2:
                temp.append(str(i[2]))  # for defect_type and defect_grade tables.
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

    def get_project_by_video_id(self, video_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT project_id FROM project_video WHERE video_id={}".format(video_id))
            data = cursor.fetchall()
            project_id = str(data[0][0])
            res = self.get_one_project_detailed(project_id=project_id)
            staff_id = res[4]
            detection_id = res[12]
            move_id = res[13]
            plugging_id = res[14]
            drainage_id = res[15]
            dredging_id = res[16]
            cursor.execute("SELECT staff_name FROM staff WHERE staff_id={}".format(staff_id))
            data = cursor.fetchall()
            res[4] = data[0][0]
            cursor.execute("SELECT detection_method FROM detection WHERE detection_id={}".format(detection_id))
            data = cursor.fetchall()
            res[12] = data[0][0]
            cursor.execute("SELECT move_method FROM move WHERE move_id={}".format(move_id))
            data = cursor.fetchall()
            res[13] = data[0][0]
            cursor.execute("SELECT plugging_method FROM plugging WHERE plugging_id={}".format(plugging_id))
            data = cursor.fetchall()
            res[14] = data[0][0]
            cursor.execute("SELECT drainage_method FROM drainage WHERE drainage_id={}".format(drainage_id))
            data = cursor.fetchall()
            res[15] = data[0][0]
            cursor.execute("SELECT dredging_method FROM dredging WHERE dredging_id={}".format(dredging_id))
            data = cursor.fetchall()
            res[16] = data[0][0]
            self.conn.commit()
            return res
        except:
            print('get project by video_id failed.')
            return None

    def get_project_by_defect_id(self, defect_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT video_id FROM defect WHERE defect_id={}".format(defect_id))
            data = cursor.fetchall()
            self.conn.commit()
            video_id = str(data[0][0])
            return self.get_project_by_video_id(video_id=video_id)
        except:
            print('get video_id by defect_id failed.')
            return None

    def get_video_by_video_id(self, video_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM video WHERE video_id={}".format(video_id))
            data = cursor.fetchall()
            res = {}
            res['staff_id'] = data[0][1]
            res['record_date'] = str(data[0][2])
            res['road_name'] = data[0][3]
            res['start_manhole_id'] = data[0][4]
            res['end_manhole_id'] = data[0][5]
            res['pipe_type_id'] = data[0][6]
            res['section_shape_id'] = data[0][7]
            res['joint_form_id'] = data[0][8]
            res['pipe_material_id'] = data[0][9]
            res['pipe_diameter'] = data[0][10] if data[0][10] is not None else 0
            res['start_pipe_depth'] = data[0][11] if data[0][11] is not None else 0
            res['end_pipe_depth'] = data[0][12] if data[0][12] is not None else 0
            res['pipe_length'] = data[0][13] if data[0][13] is not None else 0
            res['detection_length'] = data[0][14] if data[0][14] is not None else 0
            res['detection_direction'] = data[0][15] if data[0][15] is not None else 0
            res['construction_year'] = data[0][16]
            res['regional_importance_id'] = data[0][17]
            res['soil_id'] = data[0][18]
            res['video_remark'] = data[0][19]
            res['video_name'] = data[0][20]
            res['import_date'] = str(data[0][21])
            res['staff'] = self.get_one_table('staff')
            res['pipe_type'] = self.get_one_table('pipe_type')
            res['section_shape'] = self.get_one_table('section_shape')
            res['joint_form'] = self.get_one_table('joint_form')
            res['pipe_material'] = self.get_one_table('pipe_material')
            res['regional'] = self.get_one_table('regional')
            res['soil'] = self.get_one_table('soil')
            res['manhole_cover'] = self.get_one_table('manhole_cover')
            res['manhole_type'] = self.get_one_table('manhole_type')
            res['manhole_material'] = self.get_one_table('manhole_material')
            cursor.execute("SELECT * FROM manhole WHERE manhole_id={}".format(res['start_manhole_id']))
            data = cursor.fetchall()
            res['start_manhole_no'] = data[0][1]
            res['start_manhole_type_id'] = data[0][2]
            res['start_manhole_material_id'] = data[0][3]
            res['start_manhole_cover_id'] = data[0][4]
            res['start_manhole_construction_year'] = str(data[0][5])
            res['start_manhole_longitude'] = data[0][6] if data[0][6] is not None else 0
            res['start_manhole_latitude'] = data[0][7] if data[0][7] is not None else 0
            res['start_internal_defect'] = data[0][8]
            res['start_external_defect'] = data[0][9]
            res['start_pipe_invert'] = data[0][10] if data[0][10] is not None else 0
            res['start_pipe_elevation'] = data[0][11] if data[0][11] is not None else 0
            cursor.execute("SELECT * FROM manhole WHERE manhole_id={}".format(res['end_manhole_id']))
            data = cursor.fetchall()
            res['end_manhole_no'] = data[0][1]
            res['end_manhole_type_id'] = data[0][2]
            res['end_manhole_material_id'] = data[0][3]
            res['end_manhole_cover_id'] = data[0][4]
            res['end_manhole_construction_year'] = str(data[0][5])
            res['end_manhole_longitude'] = data[0][6] if data[0][6] is not None else 0
            res['end_manhole_latitude'] = data[0][7] if data[0][7] is not None else 0
            res['end_internal_defect'] = data[0][8]
            res['end_external_defect'] = data[0][9]
            res['end_pipe_invert'] = data[0][10] if data[0][10] is not None else 0
            res['end_pipe_elevation'] = data[0][11] if data[0][11] is not None else 0
            return res
        except:
            print('get video by video_id failed.')
            return None

    def get_video_by_defect_id(self, defect_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT video_id FROM defect WHERE defect_id={}".format(defect_id))
            data = cursor.fetchall()
            self.conn.commit()
            video_id = str(data[0][0])
            return self.get_video_by_video_id(video_id=video_id)
        except:
            print('get video by defect_id failed.')
            return None

    def get_defect_by_defect_id(self, defect_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM defect WHERE defect_id={}".format(defect_id))
            data = cursor.fetchall()
            res = {}
            res['video_id']=data[0][1]
            res['time_in_video'] = data[0][2]
            res['defect_type_id'] = data[0][3]
            res['defect_distance'] = data[0][4] if data[0][4] is not None else 0
            res['defect_length'] = data[0][5] if data[0][5] is not None else 0
            res['clock_start'] = data[0][6] if data[0][6] is not None else 0
            res['clock_end'] = data[0][7] if data[0][7] is not None else 0
            res['defect_grade_id'] = data[0][8]
            res['defect_remark'] = data[0][9]
            res['defect_date'] = data[0][10]
            res['defect_attribute'] = data[0][11]
            res['defect_type'] = self.get_one_table('defect_type')
            res['defect_grade'] = self.get_one_table('defect_grade')
            if res['defect_remark'] is None:
                res['defect_remark'] = res['defect_type'][res['defect_type_id'] - 1][2]
            return res
        except:
            print('get defect by defect_id failed.')
            return None

    def save_video(self, data):
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "SELECT start_manhole_id,end_manhole_id FROM video WHERE video_id={}".format(data['video_id']))
            temp_data = cursor.fetchall()
            start_manhole_id = temp_data[0][0]
            end_manhole_id = temp_data[0][1]
            sql = "UPDATE manhole set manhole_no='{}',manhole_type_id={},manhole_material_id={},manhole_cover_id={},manhole_longitude={},manhole_latitude={},internal_defect='{}',external_defect='{}',pipe_elevation={} where manhole_id={}".format(
                data['start_manhole_no'], data['start_manhole_type_id'], data['start_manhole_material_id'],
                data['start_manhole_cover_id'], data['start_manhole_longitude'], data['start_manhole_latitude'],
                data['start_internal_defect'], data['start_external_defect'], data['start_pipe_elevation'],
                start_manhole_id)
            cursor.execute(sql)
            sql = "UPDATE manhole SET manhole_no='{}',manhole_type_id={},manhole_material_id={},manhole_cover_id={},manhole_longitude={},manhole_latitude={},internal_defect='{}',external_defect='{}',pipe_elevation={} WHERE manhole_id={}".format(
                data['end_manhole_no'], data['end_manhole_type_id'], data['end_manhole_material_id'],
                data['end_manhole_cover_id'], data['end_manhole_longitude'], data['end_manhole_latitude'],
                data['end_internal_defect'], data['end_external_defect'], data['end_pipe_elevation'],
                end_manhole_id)
            cursor.execute(sql)
            sql = "UPDATE video SET staff_id={},road_name='{}',pipe_type_id={},section_shape_id={},joint_form_id={},pipe_material_id={},pipe_diameter={},start_pipe_depth={},end_pipe_depth={},pipe_length={},detection_length={},detection_direction={},construction_year='{}',regional_importance_id={},soil_id={},video_remark='{}' WHERE video_id={}".format(
                data['staff_id'], data['road_name'], data['pipe_type_id'], data['section_shape_id'],
                data['joint_form_id'], data['pipe_material_id'], data['pipe_diameter'], data['start_pipe_depth'],
                data['end_pipe_depth'], data['pipe_length'], data['detection_length'], data['detection_direction'],
                data['construction_year'], data['regional_importance_id'], data['soil_id'], data['video_remark'],
                data['video_id'])
            cursor.execute(sql)
            self.conn.commit()
            return True
        except:
            print('save video failed.')
            return False

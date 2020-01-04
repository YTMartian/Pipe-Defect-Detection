from datetime import datetime

import pymysql


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
        print('connect successful.')

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
            temp = [str(i[j]) for j in range(0, 12)]  # the first item is id, we need to record it.
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

    def get_project_statistic(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM project")
        self.conn.commit()
        data = cursor.fetchall()
        cursor.close()
        res = []
        for i in data:
            temp = [str(i[j]) for j in range(0, 6)]
            staff_id = temp[4]
            project_id = str(i[0])
            temp[4] = self.get_name('staff', staff_id)
            video_amount = self.get_value("SELECT COUNT(*) FROM project_video WHERE project_id={}".format(project_id))
            temp.append(str(video_amount))
            pipe_amount = self.get_value(
                "SELECT COUNT(*) FROM  video WHERE video_id IN (SELECT video_id FROM project_video WHERE project_id = {}) AND TRIM(video.start_manhole_no) != '' AND TRIM(video.end_manhole_no) != '' ".format(
                    project_id))
            temp.append(str(pipe_amount))
            pipe_total_length = self.get_value(
                "SELECT SUM(pipe_length) FROM  video WHERE video_id IN (SELECT video_id FROM project_video WHERE project_id = {}) AND TRIM(video.start_manhole_no) != '' AND TRIM(video.end_manhole_no) != ''".format(
                    project_id))
            if pipe_total_length is None:
                pipe_total_length = 0
            temp.append(str(pipe_total_length))
            standard_sum = self.get_value(
                "SELECT COUNT(*) FROM  defect WHERE video_id IN (SELECT video_id FROM project_video WHERE project_id = {}) ".format(
                    project_id))
            temp.append(str(standard_sum))
            defect_sum = standard_sum  # maybe they are the same thing?
            temp.append(str(defect_sum))
            res.append(temp.copy())
        return res

    def get_video(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM video")
        self.conn.commit()
        data = cursor.fetchall()
        cursor.close()
        res = []
        for i in data:
            temp = []
            temp.append(str(i[0]))  # video_id.
            temp.append(str(i[3]))  # road_name.
            temp.append(str(i[4]) + ' ~ ' + str(i[13]))  # pipe number.
            temp.append(str(i[24]))  # pipe_type_id.
            temp.append(str(i[27]))  # pipe_material_id.
            temp.append(str(i[38]))  # video_name.
            temp.append(str(i[2]))  # record_date.
            temp.append(str(i[39]))  # import_date.
            temp[3] = self.get_name('pipe_type', temp[3])
            temp[4] = self.get_name('pipe_material', temp[4])
            defect_amount = self.get_value("SELECT COUNT(*) FROM defect WHERE video_id = {}".format(temp[0]))
            temp.append(str(defect_amount))

            res.append(temp.copy())
        return res

    def get_defect(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM defect")
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

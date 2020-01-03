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

    def get_project_detailed(self):
        def get_name(table, id):
            cursor = self.conn.cursor()
            cursor.execute('select * from {0} where {0}_id = {1}'.format(table, id))
            self.conn.commit()
            data = cursor.fetchall()
            return data[0][1]

        cursor = self.conn.cursor()
        cursor.execute('select * from project')
        self.conn.commit()
        data = cursor.fetchall()
        cursor.close()
        res = []
        for i in data:
            temp = [i[j] for j in range(1, 12)]
            temp[4] = str(temp[4])  # convert datetime.date to string.
            detection_id = i[12]
            move_id = i[13]
            plugging_id = i[14]
            drainage_id = i[15]
            dredging_id = i[16]
            temp.append(get_name('detection', detection_id))
            temp.append(get_name('move', move_id))
            temp.append(get_name('plugging', plugging_id))
            temp.append(get_name('drainage', drainage_id))
            temp.append(get_name('dredging', dredging_id))
            res.append(temp.copy())
        return res

    def get_project_statistic(self):
        pass

    def get_video(self):
        pass

    def get_defect(self):
        pass

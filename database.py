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
        cursor = self.conn.cursor()
        cursor.execute('select * from project')
        self.conn.commit()
        data = cursor.fetchall()
        cursor.close()
        print(data)
        return []

    def get_project_statistic(self):
        pass

    def get_video(self):
        pass

    def get_defect(self):
        pass

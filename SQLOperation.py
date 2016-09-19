import pymysql


class CanvasDataBase:
    def __init__(self, host, usr, pw, name='user'):
        self.host = host
        self.user = usr
        self.pwd = pw
        self.name = name
        self.conn = pymysql.connect(host=self.host, user=self.user, passwd=self.pwd, port=3306, charset='utf8')
        self.cur = self.conn.cursor()
        self.db_name = 'Canvas_'+self.name

    def __del__(self):
        self.cur.close()
        self.conn.close()

    def drop_db(self):
        create_query = 'create database if not exists Canvas_' + self.name
        self.cur.execute(create_query)
        self.conn.select_db(self.db_name)
        drop_query = 'drop table if exists Assignments'
        self.cur.execute(drop_query)
        drop_query = 'drop table if exists Files'
        self.cur.execute(drop_query)

    def init_db(self):
        create_query = 'create database if not exists Canvas_' + self.name
        self.cur.execute(create_query)
        self.conn.select_db(self.db_name)
        assign_table_query = \
        '''
        create table if not exists Assignments (
            ID INT,
            COURSE TEXT,
            NAME TEXT,
            CREATED_AT TINYTEXT,
            UPDATED_AT TINYTEXT,
            DUE_AT TINYTEXT,
            UNLOCK_AT TINYTEXT) charset utf8 collate utf8_general_ci
        '''
        self.cur.execute(assign_table_query)
        file_table_query = \
        '''
        create table if not exists Files (
            ID INT,
            COURSE TEXT,
            FILENAME TEXT,
            CONTENT_TYPE TEXT,
            SIZE INT,
            PARENT_FOLDER_ID TEXT,
            PATH TEXT,
            CREATED_AT TINYTEXT,
            UPDATED_AT TINYTEXT,
            MODIFIED_AT TINYTEXT,
            UNLOCK_AT TINYTEXT,
            URL TEXT,
            DOWNLOAD_STATUS TINYTEXT) charset utf8 collate utf8_general_ci
        '''
        self.cur.execute(file_table_query)

    def insert_assignment(self, params):
        # id course name created_at
        # updated_at due_at unlock_at
        insert_query = \
        '''
        insert into Assignments values (%s, %s, %s, %s, %s, %s, %s)
        '''
        self.cur.execute(insert_query, params)
        self.conn.commit()

    def update_assignment(self, params):
        update_query = \
        '''
        update Assignments
                set updated_at = '{}', due_at = '{}'
            where id = {}
        '''.format(params[4], params[5], params[0])
        self.cur.execute(update_query)
        self.conn.commit()

    def op_assignment(self, params):
        aid = params[0]
        check_query = \
        '''
        select * from assignments where id = {}
        '''.format(str(aid))
        length = self.cur.execute(check_query)
        for content in self.cur:
            if content:
                self.update_assignment(params)
                break
        self.insert_assignment(params)

    def insert_file(self, params):
        # id course filename content_type
        # size parent_folder_id path created_at
        # updated_at modified_at unlock_at url
        # download_status
        insert_query = \
        '''
        insert into Files values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        self.cur.execute(insert_query, params)
        self.conn.commit()

    def update_file(self, params):
        update_query = \
        '''
        update Files
                set updated_at = '{}', modified_at = '{}', download_status = '{}'
            where id = {}
        '''.format(params[8], params[9], params[12], params[0])
        self.cur.execute(update_query)
        self.conn.commit()

    def check_file_download(self, params):
        fid = params[0]
        check_query = \
        '''
        select * from files where id = {}
        '''.format(str(fid))
        length = self.cur.execute(check_query)
        for content in self.cur:
            return content[-1]
        return 'failed'

    def op_file(self, params):
        fid = params[0]
        check_query = \
        '''
        select * from files where id = {}
        '''.format(str(fid))
        length = self.cur.execute(check_query)
        for content in self.cur:
            if content:
                self.update_file(params)
                return
        self.insert_file(params)


if __name__ == '__main__':
    cdb = CanvasDataBase('localhost', 'root', '')
    cdb.drop_db()
    # cdb.op_assignment([str(39), 'VE203, Discrete Mathematics', 'Assignment 1', '2016-09-07T07:05:19Z', '2016-209-14T07:46:05Z', '2016-092-22T08:00:00Z', '2016-09-211T16:00:00Z'])


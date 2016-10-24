import pymysql
import warnings


class CanvasDataBase:
    def __init__(self, host, usr, pw, name='user'):
        self.host = host
        self.user = usr
        self.pwd = pw
        self.name = name
        self.conn = pymysql.connect(host=self.host, user=self.user, passwd=self.pwd, port=3306, charset='utf8')
        self.cur = self.conn.cursor()
        self.db_name = 'Canvas_'+self.name
        warnings.filterwarnings("ignore")

    def __del__(self):
        self.cur.close()
        self.conn.close()

    def drop_db(self, tb_name='ALL'):
        create_query = 'create database if not exists Canvas_' + self.name
        self.cur.execute(create_query)
        self.conn.select_db(self.db_name)
        if tb_name == 'ALL':
            drop_query = 'drop table if exists Assignments'
            self.cur.execute(drop_query)
            drop_query = 'drop table if exists Files'
            self.cur.execute(drop_query)
            drop_query = 'drop table if exists Announcements'
            self.cur.execute(drop_query)
            drop_query = 'drop table if exists Discussions'
            self.cur.execute(drop_query)
        else:
            drop_query = 'drop table if exists ' + tb_name
            self.cur.execute(drop_query)

    def init_db(self):
        create_query = 'create database if not exists ' + self.db_name
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
            UNLOCK_AT TINYTEXT,
            DOWNLOAD_STATUS TINYTEXT) charset utf8 collate utf8_general_ci
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
        # permission: list -> int 1111
        # attachments no dealing
        anno_create_query = \
        '''
        create table if not exists Announcements (
            ID INT,
            COURSE TEXT,
            URL TEXT,
            TITLE TEXT,
            MESSAGE LONGTEXT,
            PERMISSIONS INT,
            AUTHOR_ID INT,
            AUTHOR_NAME TEXT,
            READ_STATE TINYTEXT,
            LAST_REPLY_AT TINYTEXT,
            CREATED_AT TINYTEXT,
            UPDATED_AT TINYTEXT,
            POSTED_AT TINYTEXT,
            DISCUSSION_TYPE TINYTEXT,
            GROUP_CATEGORY_ID TINYTEXT) charset utf8 collate utf8_general_ci
        '''
        self.cur.execute(anno_create_query)
        diss_create_query = \
        '''
        create table if not exists Discussions (
            ID INT,
            COURSE TEXT,
            URL TEXT,
            TITLE TEXT,
            MESSAGE LONGTEXT,
            PERMISSIONS INT,
            AUTHOR_ID INT,
            AUTHOR_NAME TEXT,
            READ_STATE TINYTEXT,
            LAST_REPLY_AT TINYTEXT,
            CREATED_AT TINYTEXT,
            UPDATED_AT TINYTEXT,
            POSTED_AT TINYTEXT,
            DISCUSSION_TYPE TINYTEXT,
            GROUP_CATEGORY_ID TINYTEXT) charset utf8 collate utf8_general_ci
        '''
        self.cur.execute(diss_create_query)
        reply_create_query = \
        '''
        create table if not exists Replys (
            ID INT,
            COURSE TEXT,
            AUTHOR_ID INT,
            AUTHOR_NAME TEXT,
            PARENT_ID INT,
            PARENT_TYPE TINYTEXT,
            PARENT_TITLE TEXT,
            MESSAGE LONGTEXT,
            CREATED_AT TINYTEXT,
            UPDATED_AT TINYTEXT,
            RATING_SUM TEXT) charset utf8 collate utf8_general_ci
        '''
        self.cur.execute(reply_create_query)

    def insert_assignment(self, params):
        # id course name created_at
        # updated_at due_at unlock_at
        insert_query = \
        '''
        insert into Assignments values (%s, %s, %s, %s, %s, %s, %s, %s)
        '''
        self.cur.execute(insert_query, params)
        self.conn.commit()

    def update_assignment(self, params):
        update_query = \
        '''
        update Assignments
                set updated_at = '{}', due_at = '{}', download_status = '{}'
            where id = {}
        '''.format(params[4], params[5], params[7], params[0])
        self.cur.execute(update_query)
        self.conn.commit()

    def check_assignment(self, params):
        aid = params[0]
        check_query = \
        '''
        select * from assignments where id = {} and updated_at = '{}'
        '''.format(str(aid), params[4])
        length = self.cur.execute(check_query)
        for content in self.cur:
            return content[-1]
        return 'failed'

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
                return
        self.insert_assignment(params)

    def insert_reply(self, params):
        # 11
        insert_query = \
        '''
        insert into replys values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        self.cur.execute(insert_query, params)
        self.conn.commit()

    def update_reply(self, params):
        update_query = \
        '''
        update replys
                set updated_at = '{}', rating_sum = '{}'
            where id = {}
        '''.format(params[9], params[10], params[0])
        self.cur.execute(update_query)
        self.conn.commit()

    def check_reply(self, params):
        aid = params[0]
        check_query = \
        '''
        select * from replys where id = {} and updated_at = '{}'
        '''.format(str(aid), params[9])
        length = self.cur.execute(check_query)
        for content in self.cur:
            return content[-1]
        return 'failed'

    def op_reply(self, params):
        aid = params[0]
        check_query = \
        '''
        select * from replys where id = {}
        '''.format(str(aid))
        length = self.cur.execute(check_query)
        for content in self.cur:
            if content:
                self.update_reply(params)
                return
        self.insert_reply(params)

    def insert_information(self, params, i_type):
        # 15
        insert_query = \
        '''
        insert into {} values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''.format(i_type)
        self.cur.execute(insert_query, params)
        self.conn.commit()

    def update_information(self, params, i_type):
        update_query = \
        '''
        update {}
                set updated_at = '{}', read_state = '{}', last_reply_at = '{}'
            where id = {}
        '''.format(i_type, params[11], params[8], params[9], str(params[0]))
        self.cur.execute(update_query)
        self.conn.commit()

    def check_information(self, params, i_type):
        aid = params[0]
        check_query = \
        '''
        select * from {} where id = {} and updated_at = '{}'
        '''.format(i_type, str(aid), params[11])
        length = self.cur.execute(check_query)
        for content in self.cur:
            return content[-1]
        return 'failed'

    def op_information(self, params, i_type):
        aid = params[0]
        check_query = \
        '''
        select * from {} where id = {}
        '''.format(i_type, str(aid))
        length = self.cur.execute(check_query)
        for content in self.cur:
            if content:
                self.update_information(params, i_type)
                return
        self.insert_information(params, i_type)

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
        select * from files where id = {} and updated_at = '{}'
        '''.format(str(fid), params[8])
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
    cdb.drop_db(tb_name='Replys')
    # cdb.op_assignment([str(39), 'VE203, Discrete Mathematics', 'Assignment 1', '2016-09-07T07:05:19Z', '2016-209-14T07:46:05Z', '2016-092-22T08:00:00Z', '2016-09-211T16:00:00Z'])


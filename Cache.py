# encoding: utf-8
from LoginJaccount import JaccountLogin
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import traceback
import ConfigParser


class JLParametersParser:
    def __init__(self, file_path):
        cp = ConfigParser.ConfigParser()
        cp.read(file_path)

        self.usr = cp.get('user_info', 'username')
        self.pw = cp.get('user_info', 'password')


if __name__ == '__main__':
    jlp = JLParametersParser('Config.ini')
    usr = jlp.usr
    pw = jlp.pw
    print 'Username: ' + usr
    print 'Password: ' + '*'*len(pw)
    if not sys.argv[1]:
        jl = JaccountLogin(usr, pw, 5, 5, 70, True)
    else:
        jl = JaccountLogin(usr, pw, int(sys.argv[1]), int(sys.argv[2]), 70, True)
    # print urllib2.urlopen('https://sjtu-umich.instructure.com/', timeout=10).read()
    try:
        xsoup, xres = jl.check_login()
        if not xres:
            jl.login(xsoup)
        jl.cdb.name = 'xiaoliran12'
        jl.cdb.db_name = 'Canvas_xiaoliran12'
        jl.cdb.init_db()
        jl.get_courses()
        jl.get_information()
        jl.get_assignments()
        jl.get_attachments()
        print('\nEND CACHING')
    except Exception as e:
        traceback.print_exc()
    finally:
        os.system('pause')


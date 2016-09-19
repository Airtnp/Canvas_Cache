# encoding: utf-8
import urllib
import urllib2
import urlparse
import cookielib
import re
import requests
import traceback
import json
import os
from bs4 import BeautifulSoup
from pytesseract import image_to_string
from time import sleep
from random import randint
from PIL import Image
from ssl import SSLError
from LoginTimeout import TimeoutThread, TimeLimitExpired
from SQLOperation import CanvasDataBase

host_url = 'https://sjtu-umich.instructure.com/'
# host_url = 'http://my2015.sjtu.edu.cn/App/CanvasKnowledgeBase/Load'
post_url = 'https://jaccount.sjtu.edu.cn/jaccount/ulogin'


class JaccountLogin:
    def __init__(self, usr, pw, timeout, threshold=140, captcha=False, host='localhost', host_user='root', host_pw=''):
        self.user = usr
        self.pw = pw
        self.timeout = timeout
        self.thresold = threshold
        self.check_captcha = captcha

        self.img_table = []
        for i in range(256):
            if i < threshold:
                self.img_table.append(0)
            else:
                self.img_table.append(1)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
            'Referer': host_url,
        }
        self.posts = {
            'user': self.user,
            'pass': self.pw,
            'sid': None,
            'returl': None,
            'se': None,
            'v': 'null',
            'captcha': None,
        }
        self.rs = requests.session()
        self.cj = cookielib.LWPCookieJar()
        self.cookie_support = urllib2.HTTPCookieProcessor(self.cj)
        self.opener = urllib2.build_opener(self.cookie_support, urllib2.HTTPHandler)
        urllib2.install_opener(self.opener)
        self.course_url = []
        self.course_title = []
        self.course_assign = {}
        self.course_attach = {}
        self.course_file = {}
        self.hw_path = 'Homework'
        self.fl_path = 'File'
        self.ban_sites = ['2015 Fall Entry', 'Current Students']

        self.cdb = CanvasDataBase(host, host_user, host_pw, self.user)
        self.cdb.init_db()

    def get_captcha(self):
        # 效果辣鸡..
        im = Image.open('captcha.jpg')
        im = im.convert('L')
        # im = im.point(self.img_table, '1')
        im.save('process_captcha.jpg')
        im = Image.open('captcha.jpg')
        captcha = image_to_string(im)
        captcha = re.findall('([a-z])', captcha)
        captcha = ''.join(captcha)
        print captcha
        return captcha

    def make_dir(self, name):
        try:
            os.mkdir(name)
        except Exception as e:
            # print e
            pass

    def get_json(self, json_data):
        return json.loads(json_data)

    @staticmethod
    def debug_prettify(self, response):
        return BeautifulSoup(response).prettify()

    def get_file(self, params):
        try:
            print '\turl = ' + params['url']
            print '\ttitle = ' + params['title']
            url = params['url']
            title = params['title']
            content = self.opener.open(url, timeout=self.timeout)
            f = open(title, 'wb')
            f.write(content.read())
            f.close()
            return True
        except urllib2.URLError:
            print 'URL Timeout error'
            return False
        except SSLError:
            print 'SSL handshake error'
            return False
        except Exception as e:
            print e
            print traceback.print_exc()
            return False

    def get_login_soup(self):
        soup = None
        try:
            h = urllib2.urlopen(host_url, timeout=self.timeout)
            soup = BeautifulSoup(h, 'html.parser')
        except urllib2.URLError:
            print 'URL Timeout error'
            soup = self.get_login_soup()
        except SSLError:
            print 'SSL handshake error'
            soup = self.get_login_soup()
        except Exception as e:
            print e
            print traceback.print_exc()
        return soup

    def check_login(self):
        print "\n---Begin Check Login---"
        soup = self.get_login_soup()
        print "---End Check Login---"
        if soup:
            if soup.title.string.find('Sign') != -1:
                return soup, False
            print soup.title.string
            if soup.title.string.find('Dashboard') != -1:
                return soup, True
        return soup, False

    def login(self, soup=None):
        print "\n---Begin Login---"
        try:
            if not soup:
                soup = self.get_login_soup()
            # h = urllib2.urlopen(host_url, timeout=self.timeout)
            # soup = BeautifulSoup(h, 'html.parser')
            # h = rs.get(host_url)
            # soup = BeautifulSoup(h.content, 'html.parser')
            # soup.findAll('input', {'name', 'sid'})
            sid = soup.select('input[name="sid"]')[0]
            sid = re.findall("value=\"(.*?)\"", str(sid))[0]
            returl = soup.select('input[name="returl"]')[0]
            returl = re.findall("value=\"(.*?)\"", str(returl))[0]
            se = soup.select('input[name="se"]')[0]
            se = re.findall("value=\"(.*?)\"", str(se))[0]
            v = soup.select('input[name="v"]')[0]
            v = re.findall("value=\"(.*?)\"", str(v))[0]

            self.posts['sid'] = sid
            self.posts['returl'] = returl
            self.posts['se'] = se
            if v:
                self.posts['v'] = v

            captcha_url = 'https://jaccount.sjtu.edu.cn/jaccount/captcha'
            captcha_pic = self.opener.open(captcha_url, timeout=self.timeout)
            # captcha_pic = rs.get(captcha_url, headers=self.headers)

            f = open('captcha.jpg', 'wb')
            # f.write(captcha_pic.content)
            f.write(captcha_pic.read())
            f.close()

            if self.check_captcha:
                self.posts['captcha'] = self.get_captcha()
            else:
                self.get_captcha()
                self.posts['captcha'] = raw_input('Enter your captcha: ').replace('\n', '')

            # print self.posts
            post_data = urllib.urlencode(self.posts)
            request = urllib2.Request(post_url, post_data, self.headers)
            response = self.opener.open(request, timeout=self.timeout)
            rsoup = BeautifulSoup(response)
            print rsoup.title.string
            if rsoup.title.string.find('Sign') != -1:
                self.login()
            # print BeautifulSoup(response).prettify()
            # response = rs.post(post_url, data=self.posts, headers=self.headers)
            # print BeautifulSoup(response.content).prettify()
            sleep(randint(2, 5))
            print "---End Login---"
        except urllib2.URLError:
            print 'URL Timeout error'
            self.login()
        except SSLError:
            print 'SSL handshake error'
            self.login()
        except IndexError:
            print 'Login in Session'
            # self.login()
        except Exception as e:
            print e
            print traceback.print_exc()

    def get_courses(self):
        print "\n---Begin Fetching Courses---"
        try:
            # ssoup, sres = self.check_login()
            # if not sres:
            #   self.login(ssoup)
            response = self.opener.open(host_url+'courses', timeout=self.timeout)
            soup = BeautifulSoup(response)
            courses = re.findall('<a href=\"(.*?)\" title="(.*?)\">', soup.prettify())
            for course in courses:
                print course
                self.course_url.append(course[0])
                self.course_title.append(course[1])
            print "---End Fetching Courses---"
        except Exception as e:
            print e
            print traceback.print_exc()

    def get_assignments(self):
        '''
        course_posts = {
            'include[]': 'assignments',  # discussion_topic
            'exclude_response_fields[]': 'description',  # 'rubric'
            'override_assignment_dates': 'true'
        }
        '''
        # course_data = urllib.urlencode(course_posts)
        # print host_url+'api/v1'+self.course_url[2]+'/assignment_groups'
        print "\n---Begin Fetching Assignments---"
        try:
            # ssoup, sres = self.check_login()
            # if not sres:
            #    self.login(ssoup)
            self.make_dir(self.hw_path)
            suffix_url = 'include%5B%5D=assignments' \
                         '&include%5B%5D=discussion_topic' \
                         '&exclude_response_fields%5B%5D=description' \
                         '&exclude_response_fields%5B%5D=rubric' \
                         '&override_assignment_dates=true'
            for i in range(0, len(self.course_url)):
                print "\n\t-Begin Assignments for " + self.course_title[i] + '-'
                self.make_dir(self.hw_path+'/'+self.course_title[i])
                course_url = host_url+'api/v1/'+self.course_url[i]+'/assignment_groups'+'?'+suffix_url
                req = urllib2.Request(course_url)
                response = self.opener.open(req)
                # print BeautifulSoup(response).prettify()
                json_data = response.read()
                json_data = re.findall('\[(\{.*\})\]', json_data)
                assignment_data = self.get_json(json_data[0])
                assignments = assignment_data['assignments']
                self.course_assign[self.course_title[i]] = []
                ad = {}

                properties = ['id', 'due_at', 'unlock_at', 'updated_at', 'created_at', 'name', 'html_url']
                for assignment in assignments:
                    db_list = [0, 0, 0, 0, 0, 0, 0]
                    for p in properties:
                        if p in assignment.keys():
                            aid = assignment[p]
                            ad[p] = aid
                        else:
                            ad[p] = 'NULL'

                    db_list[0] = ad['id']  # ID
                    db_list[1] = self.course_title[i]  # COURSE
                    db_list[2] = ad['name']  # Name
                    db_list[3] = ad['created_at']
                    db_list[4] = ad['updated_at']
                    db_list[5] = ad['due_at']
                    db_list[6] = ad['unlock_at']

                    assign_data = urllib2.urlopen(ad['html_url'])
                    soup = BeautifulSoup(assign_data)
                    files = soup.findAll('a', {'class', 'instructure_scribd_file'})
                    ad['files'] = []
                    for afile in files:
                        href = afile['href']
                        title = afile['title']
                        fl = {
                            'url': host_url+href,
                            'title': title,
                        }
                        ad['files'].append(fl)

                        fl['title'] = self.hw_path+'/'+self.course_title[i] + '/' + title
                        try:
                            TimeoutThread(self.timeout, self.get_file, fl)
                        except TimeLimitExpired:
                            print fl['title']
                            print 'Download fail for first time, try second time'
                            try:
                                TimeoutThread(self.timeout, self.get_file, fl)
                            except TimeLimitExpired:
                                print fl['title']
                                print 'Download fail!'
                    self.cdb.op_assignment(db_list)
                    self.course_assign[self.course_title[i]].append(ad)
                print "\t-End Assignments for " + self.course_title[i] + '-'
            print "---End Fetching Assignments---"
        except Exception as e:
            print e
            print traceback.print_exc()

    def get_folder_files(self, fid, path_prefix):
        self.make_dir(path_prefix)
        fid = str(fid)
        file_url = host_url + 'api/v1/folders/' + fid + '/files'
        req = urllib2.Request(file_url)
        response = self.opener.open(req)
        json_data = response.read()
        json_data = re.findall(';\[(\{.*\})\]', json_data)
        t_files = []
        file_properties = ['id', 'folder_id', 'filename', 'content-type', 'url', 'size',
                           'created_at', 'updated_at', 'unlock_at', 'modified_at']
        if json_data:
            json_data = json_data[0]
            files = re.findall('(\{.*?\})', json_data)
            for xfile in files:
                r_file = {}
                file_data = self.get_json(xfile)
                for fp in file_properties:
                    if fp in file_data.keys():
                        r_file[fp] = file_data[fp]
                    else:
                        r_file[fp] = 'null'

                db_list = [0]*13
                db_list[0] = r_file['id']
                db_list[1] = path_prefix.split('/')[1] # Courses
                db_list[2] = r_file['filename']
                db_list[3] = r_file['content-type']
                db_list[4] = r_file['size']
                db_list[5] = r_file['folder_id']
                db_list[6] = path_prefix #Path
                db_list[7] = r_file['created_at']
                db_list[8] = r_file['updated_at']
                db_list[9] = r_file['modified_at']
                db_list[10] = r_file['unlock_at']
                db_list[11] = r_file['url']
                db_list[12] = 'success'

                t_files.append(r_file)
                fl = {}
                fl['url'] = r_file['url']
                fl['title'] = path_prefix + '/' + r_file['filename']
                download_status = self.cdb.check_file_download(db_list)
                # print download_status
                if download_status != 'success':
                    try:
                        TimeoutThread(self.timeout, self.get_file, fl)
                    except TimeLimitExpired:
                        print fl['title']
                        print 'Download fail for first time, try second time'
                        try:
                            TimeoutThread(self.timeout, self.get_file, fl)
                        except TimeLimitExpired:
                            print fl['title']
                            print 'Download fail!'
                            db_list[12] = 'failed'
                self.cdb.op_file(db_list)
        return t_files

    def get_folder(self, fid, path_prefix):
        fid = str(fid)
        folder_url = host_url + 'api/v1/folders/' + fid + '/folders'
        req = urllib2.Request(folder_url)
        response = self.opener.open(req)
        json_data = response.read()
        json_data = re.findall(';\[(\{.*\})\]', json_data)
        t_folder = []
        folder_properties = ['folder_url', 'folders_counter', 'name', 'id', 'context_id',
                             'updated_at', 'created_at', 'parent_folder_id']
        file_properties = ['files_url', 'files_count']

        if json_data:
            json_data = json_data[0]
            folders = re.findall('(\{.*?\})', json_data)
            for xfolder in folders:
                a_folder = {}
                a_file = {}
                folder_data = self.get_json(xfolder)
                for fp in folder_properties:
                    if fp in folder_data.keys():
                        a_folder[fp] = folder_data[fp]
                for fp in file_properties:
                    if fp in folder_data.keys():
                        a_file[fp] = folder_data[fp]
                a_file['files_detail'] = self.get_folder_files(fid, path_prefix)
                a_folder['file'] = a_file
                a_folder['child_folder'] = self.get_folder(a_folder['id'], path_prefix+'/'+a_folder['name'])
                t_folder.append(a_folder)
        else:
            a_folder = {}
            a_file = {}
            a_file['files_detail'] = self.get_folder_files(fid, path_prefix)
            a_folder['file'] = a_file
            t_folder.append(a_folder)
            return t_folder

    def get_attachments(self):
        '''
        course_posts = {
            'include[]': 'assignments',  # discussion_topic
            'exclude_response_fields[]': 'description',  # 'rubric'
            'override_assignment_dates': 'true'
        }
        '''
        # course_data = urllib.urlencode(course_posts)
        # print host_url+'api/v1'+self.course_url[2]+'/assignment_groups'
        print "\n---Begin Fetching Files---"
        try:
            # ssoup, sres = self.check_login()
            # if not sres:
            #    self.login(ssoup)
            self.make_dir(self.fl_path)
            folder_suffix_url = ''
            file_suffix_url = ''
            for i in range(0, len(self.course_url)):
                if self.course_title[i] in self.ban_sites:
                    continue
                print "\n\t-Begin Files for " + self.course_title[i] + '-'
                self.make_dir(self.fl_path+'/'+self.course_title[i])
                root_url = host_url+'api/v1/'+self.course_url[i]+'/folders/root'
                req = urllib2.Request(root_url)
                response = self.opener.open(req)
                # print BeautifulSoup(response).prettify()
                json_data = response.read()
                json_data = re.findall(';(\{.*\})', json_data)
                file_data = self.get_json(json_data[0])
                self.course_attach[self.course_title[i]] = {}
                a_folder = {}
                a_file = {}
                folder_properties = ['folder_url', 'folders_counter', 'name', 'id', 'context_id',
                                     'updated_at', 'created_at']
                file_properties = ['files_url', 'files_count']
                for fp in folder_properties:
                    if fp in file_data.keys():
                        a_folder[fp] = file_data[fp]
                for fp in file_properties:
                    if fp in file_data.keys():
                        a_file[fp] = file_data[fp]
                a_folder['file'] = a_file
                a_folder['child_folder'] = self.get_folder(a_folder['id'], self.fl_path + '/' + self.course_title[i])
                self.course_attach[self.course_title[i]]['root'] = a_folder
                print "\t-End Files for " + self.course_title[i] + '-'
            print "---End Fetching Files---"
        except Exception as e:
            print e
            print traceback.print_exc()


if __name__ == '__main__':
    # Seen from tieba
    # jl = JaccountLogin('SJTUwbl', '199509091014wbl', 100, 70)
    jl = JaccountLogin('username', 'password', 10, 70, True)
    # print urllib2.urlopen('https://sjtu-umich.instructure.com/', timeout=10).read()
    xsoup, xres = jl.check_login()
    if not xres:
        jl.login(xsoup)
    jl.get_courses()
    # jl.get_assignments()
    jl.get_attachments()



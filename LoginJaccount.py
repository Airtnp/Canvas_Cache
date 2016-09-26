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
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
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
    def __init__(self, usr, pw, timeout, dtimeout=10, threshold=140, captcha=False, host='localhost', host_user='root', host_pw=''):
        self.user = usr
        self.pw = pw
        self.timeout = timeout
        self.thresold = threshold
        self.check_captcha = captcha
        if not dtimeout:
            self.dtimeout = self.timeout
        else:
            self.dtimeout = dtimeout

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
        self.course_discuss = {}
        self.course_announce = {}
        self.course_attach = {}
        self.course_file = {}
        self.hw_path = 'Homework'
        self.fl_path = 'File'
        # self.ban_sites = ['2015 Fall Entry', 'Current Students']
        self.ban_sites = []
        self.refresh_files = 0
        self.cdb = CanvasDataBase(host, host_user, host_pw, self.user)
        # self.cdb.init_db()

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
            print '\t\turl = ' + params['url']
            url = params['url']
            title = params['title']
            # t_type = sys.getdefaultencoding()
            # title = title.decode('utf-8').encode(t_type)
            print '\t\ttitle = ' + title
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

    def login(self, soup=None, ui_params=None):
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
            '''
            if ui_params:
                captcha_view = ui_params['window'].graphicsView
                captcha_scene = ui_params['window'].scene
                captcha_pict = ui_params['window'].captcha
                captcha_pict.load('captcha.jpg')
                captcha_item = ui_params['window'].captcha_item
                captcha_item.setPixmap(captcha_pict)
                captcha_scene.addItem(captcha_item)
                captcha_view.setScene(captcha_scene)
                captcha_view.update()
                captcha_view.show()
            '''

            if self.check_captcha:
                self.posts['captcha'] = self.get_captcha()
            else:
                if ui_params:
                    captcha_widget = ui_params['window'].lineEdit_3
                    captcha_signal = ui_params['window'].login_signal
                    while not captcha_signal:
                        captcha_signal = ui_params['window'].login_signal
                    captcha = captcha_widget.text()
                    self.posts['captcha'] = captcha

                else:
                    self.posts['captcha'] = raw_input('Enter your captcha: ')
            self.posts['captcha'] = self.posts['captcha'].replace('\n', '')
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
            response = self.get_url_data(host_url+'courses')
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

    def get_url_data(self, url):
        try:
            data = self.opener.open(url, timeout=self.timeout)
        except urllib2.URLError:
            print 'URL Timeout error'
            data = self.get_url_data(url)
        except SSLError:
            print 'SSL handshake error'
            data = self.get_url_data(url)
        except Exception as e:
            print e
            print traceback.print_exc()
            data = None
        return data

    def get_course_assignments(self, c_title, c_url):
        try:
            suffix_url = 'include%5B%5D=assignments' \
                             '&include%5B%5D=discussion_topic' \
                             '&exclude_response_fields%5B%5D=description' \
                             '&exclude_response_fields%5B%5D=rubric' \
                             '&override_assignment_dates=true'
            print "\n\t-Begin Assignments for " + c_title + '-'
            self.make_dir(self.hw_path+'/'+c_title)
            course_url = host_url+'api/v1/'+c_url+'/assignment_groups'+'?'+suffix_url
            req = urllib2.Request(course_url)
            response = self.opener.open(req, timeout=self.timeout)
            # print BeautifulSoup(response).prettify()
            json_data = response.read()
            json_data = json_data.replace('while(1);', '')
            json_data = self.get_json(json_data)
            for assign_group in json_data:
                # assign_group = re.findall('(\{.*\})', assign_group)
                # has new things: assignment_group
                # assignment_data = self.get_json(assign_group)
                assignments = assign_group['assignments']
                self.course_assign[c_title] = []
                ad = {}

                properties = ['id', 'due_at', 'unlock_at', 'updated_at', 'created_at', 'name', 'html_url']
                for assignment in assignments:
                    db_list = [0, 0, 0, 0, 0, 0, 0, 0]
                    for p in properties:
                        if p in assignment.keys():
                            aid = assignment[p]
                            ad[p] = aid
                        else:
                            ad[p] = 'NULL'

                    db_list[0] = ad['id']  # ID
                    db_list[1] = c_title  # COURSE
                    db_list[2] = ad['name']  # Name
                    db_list[3] = ad['created_at']
                    db_list[4] = ad['updated_at']
                    db_list[5] = ad['due_at']
                    db_list[6] = ad['unlock_at']
                    db_list[7] = 'success'

                    assign_data = self.get_url_data(ad['html_url'])
                    if assign_data:
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
                            title = title.split(".")
                            fl['title'] = self.hw_path+'/'+c_title + '/' + title[0] + '_' + str(ad['id']) + '.' + title[1]
                            download_status = self.cdb.check_assignment(db_list)
                            if download_status != 'success' or self.refresh_files == 1:
                                try:
                                    TimeoutThread(self.dtimeout, self.get_file, fl)
                                except TimeLimitExpired:
                                    print fl['title']
                                    print 'Download fail for first time, try second time'
                                    try:
                                        TimeoutThread(self.dtimeout, self.get_file, fl)
                                    except TimeLimitExpired:
                                        print fl['title']
                                        print 'Download fail!'
                                        db_list[7] = 'failed'
                        self.cdb.op_assignment(db_list)
                        self.course_assign[c_title].append(ad)
            print "\t-End Assignments for " + c_title + '-'
        except urllib2.URLError:
            print 'URL Timeout error'
            self.get_course_assignments(c_title, c_url)
        except SSLError:
            print 'SSL handshake error'
            self.get_course_assignments(c_title, c_url)
        except ValueError:
            print 'Unknown JSON Error'
            print response.read()
            # self.get_course_assignments(c_title, c_url)
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
            for i in range(0, len(self.course_url)):
                c_title = self.course_title[i]
                c_url = self.course_url[i]
                self.get_course_assignments(c_title, c_url)
            print "---End Fetching Assignments---"
        except Exception as e:
            print e
            print traceback.print_exc()

    def get_folder_files(self, fid, path_prefix):
        try:
            self.make_dir(path_prefix)
            fid = str(fid)
            file_url = host_url + 'api/v1/folders/' + fid + '/files'
            req = urllib2.Request(file_url)
            response = self.opener.open(req, timeout=self.timeout)
            json_data = response.read()
            json_data = re.findall(';\[(\{.*\})\]', json_data)
            t_files = []
            file_properties = ['id', 'folder_id', 'display_name', 'filename', 'content-type', 'url', 'size',
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
                    db_list[2] = r_file['display_name']
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
                    title = r_file['display_name'].split(".")
                    fl['title'] = path_prefix + '/' + title[0] + '_' + str(r_file['id']) + '.' + title[1]
                    # fl['title'] = path_prefix + '/' + r_file['display_name'] + '_' + str(r_file['id'])
                    download_status = self.cdb.check_file_download(db_list)
                    # print download_status
                    # self.refresh_files = 1
                    if download_status != 'success' or self.refresh_files == 1:
                        try:
                            TimeoutThread(self.dtimeout, self.get_file, fl)
                        except TimeLimitExpired:
                            print fl['title']
                            print 'Download fail for first time, try second time'
                            try:
                                TimeoutThread(self.dtimeout, self.get_file, fl)
                            except TimeLimitExpired:
                                print fl['title']
                                print 'Download fail!'
                                db_list[12] = 'failed'
                        except Exception as e:
                            db_list[12] = 'failed'
                    self.cdb.op_file(db_list)
        except urllib2.URLError:
            print 'URL Timeout error'
            t_files = self.get_folder_files(fid, path_prefix)
        except SSLError:
            print 'SSL handshake error'
            t_files = self.get_folder_files(fid, path_prefix)
        except Exception as e:
            print e
            t_files = []
        return t_files

    def get_folder(self, fid, path_prefix):
        try:
            fid = str(fid)
            folder_url = host_url + 'api/v1/folders/' + fid + '/folders'
            req = urllib2.Request(folder_url)
            response = self.opener.open(req, timeout=self.timeout)
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
                    print('\n\t\tFolder-'+a_folder['name'])
                    a_folder['child_folder'] = self.get_folder(a_folder['id'], path_prefix+'/'+a_folder['name'])
                    t_folder.append(a_folder)
            else:
                a_folder = {}
                a_file = {}
                a_file['files_detail'] = self.get_folder_files(fid, path_prefix)
                a_folder['file'] = a_file
                t_folder.append(a_folder)
        except urllib2.URLError:
            print 'URL Timeout error'
            t_folder = self.get_folder_files(fid, path_prefix)
        except SSLError:
            print 'SSL handshake error'
            t_folder = self.get_folder_files(fid, path_prefix)
        except Exception as e:
            print e
            t_folder = []
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
                response = self.get_url_data(req)
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
                a_file['files_detail'] = self.get_folder_files(a_folder['id'], self.fl_path + '/' + self.course_title[i])
                a_folder['file'] = a_file
                a_folder['child_folder'] = self.get_folder(a_folder['id'], self.fl_path + '/' + self.course_title[i])
                self.course_attach[self.course_title[i]]['root'] = a_folder
                print "\t-End Files for " + self.course_title[i] + '-'
            print "---End Fetching Files---"
        except urllib2.URLError:
            print 'URL Timeout error'
            self.get_attachments()
        except SSLError:
            print 'SSL handshake error'
            self.get_attachments()
        except Exception as e:
            print e
            print traceback.print_exc()

    def get_reply(self, base_url, diss_id, base_title, a_title):
        reply_url = base_url + '/{}/' + 'view?include_new_entries=1&include_enrollment_state=1'
        reply_url = reply_url.format(diss_id)
        reply_properties = [
            'unread_entries', 'forced_entries', 'entry_ratings',
            'participants', 'view', 'new_entries'
        ]
        reply_part_properties = [
            'id', 'display_name', 'avatar_image_url', 'html_url'
        ]
        reply_view_properties = [
            'id', 'user_id', 'parent_id', 'created_at',
            'updated_at', 'rating_count', 'rating_sum', 'message',
            'replies', 'deleted'
        ] #
        reply_view_reply_properties = [
            'id', 'user_id', 'parent_id', 'created_at', 'updated_at', 'message', 'rating_count',
            'rating_sum', 'deleted'
        ]
        t_reply = []
        reply_data = self.get_url_data(reply_url)
        json_data = reply_data.read().replace('while(1);', '')
        json_data = self.get_json(json_data)
        if json_data:
            reply = json_data
            a_reply = {}
            for dp in reply_properties:
                if dp in reply.keys():
                    a_reply[dp] = reply[dp]
                else:
                    a_reply[dp] = ''
            if reply['view']:
                for rep in reply['view']:
                    db_list = [0]*11
                    db_list[0] = rep['id']
                    db_list[1] = base_title

                    db_list[5] = 'first'
                    db_list[3] = ''
                    if not 'deleted' in rep.keys() or not rep['deleted']:

                        db_list[2] = rep['user_id']
                        for p in reply['participants']:
                            if p['id'] == db_list[2]:
                                db_list[3] = p['display_name']
                                break
                        db_list[7] = rep['message']
                    else:
                        db_list[2] = rep['editor_id']
                        db_list[5] = db_list[5] + '_deleted'
                        db_list[3] = db_list[3] + '_deleted'
                        db_list[7] = ''

                    db_list[4] = rep['parent_id']
                    db_list[6] = a_title
                    db_list[8] = rep['created_at']
                    db_list[9] = rep['updated_at']
                    db_list[10] = rep['rating_sum']
                    self.cdb.op_reply(db_list)
                    if 'replies' in rep.keys():
                        if rep['replies']:
                            for rrep in rep['replies']:
                                ddb_list = [0]*11
                                ddb_list[0] = rrep['id']
                                ddb_list[1] = base_title
                                
                                ddb_list[5] = 'second'
                                ddb_list[3] = ''
                                if not 'deleted' in rrep.keys() or not rrep['deleted']:
                                    ddb_list[2] = rrep['user_id']
                                    for p in reply['participants']:
                                        if p['id'] == ddb_list[2]:
                                            ddb_list[3] = p['display_name']
                                            break
                                    ddb_list[7] = rrep['message']
                                else:
                                    ddb_list[2] = rrep['editor_id']
                                    ddb_list[5] = ddb_list[5] + '_deleted'
                                    ddb_list[3] = ddb_list[3] + '_deleted'
                                    ddb_list[7] = ''

                                ddb_list[4] = rrep['parent_id']
                                ddb_list[6] = a_title
                                ddb_list[8] = rrep['created_at']
                                ddb_list[9] = rrep['updated_at']
                                ddb_list[10] = rrep['rating_sum']
                                self.cdb.op_reply(ddb_list)
            t_reply.append(a_reply)
        return t_reply

    def get_announcement(self, base_url, base_title):
        suffix_url = '?only_announcements=true'
        anno_url = base_url+suffix_url
        anno_properties = [
            'id', 'title', 'last_reply_at', 'delayed_post_at', 'created_at', 'updated_at',
            'posted_at', 'assignment_id', 'root_topic_id', 'position',
            'discussion_type', 'lock_at', 'permissions',
            'user_can_see_posts', 'read_state',
            'topic_children', 'attachments', 'author',
            'html_url', 'url', 'group_category_id', 'locked', 'lock_explanation',
            'message', 'pinned', 'subscription_hold'
        ]
        anno_perm_properties = [
            'attach', 'update', 'reply', 'delete'
        ] # topic_children/attachments: list
        anno_author_properties = ['id', 'display_name', 'avatar_image_url']
        anno_data = self.get_url_data(anno_url)
        json_data = anno_data.read().replace("while(1);", '')
        json_data = self.get_json(json_data)
        t_anno = []
        if json_data:
            for announcement in json_data:
                a_anno = {}

                for dp in anno_properties:
                    if dp in announcement.keys():
                        a_anno[dp] = announcement[dp]
                    else:
                        a_anno[dp] = ''

                db_list = [0]*15
                db_list[0] = a_anno['id']
                db_list[1] = base_title
                db_list[2] = a_anno['url']
                db_list[3] = a_anno['title']
                db_list[4] = a_anno['message']
                a_perm = a_anno['permissions']
                db_list[5] = str(int(a_perm['attach'])*1000+int(a_perm['update'])*100+int(a_perm['reply'])*10+int(a_perm['delete']))
                db_list[6] = a_anno['author']['id']
                db_list[7] = a_anno['author']['display_name']
                db_list[8] = a_anno['read_state']
                db_list[9] = a_anno['last_reply_at']
                db_list[10] = a_anno['created_at']
                db_list[11] = a_anno['updated_at']
                db_list[12] = a_anno['posted_at']
                db_list[13] = a_anno['discussion_type']
                db_list[14] = a_anno['group_category_id']
                self.cdb.op_information(db_list, 'announcements')

                a_anno['reply'] = self.get_reply(base_url, a_anno['id'], base_title, a_anno['title'])
                t_anno.append(a_anno)
                if db_list[8] == 'unread':
                    print("\t\t\t"+a_anno['title'].decode('utf-8'))
        return t_anno

    def get_discussion(self, base_url, base_title):
        diss_url = base_url
        diss_properties = [
            'id', 'title', 'last_reply_at', 'delayed_post_at', 'created_at', 'updated_at',
            'posted_at', 'assignment_id', 'root_topic_id', 'position',
            'discussion_type', 'lock_at', 'permissions',
            'user_can_see_posts', 'read_state',
            'topic_children', 'attachments', 'author',
            'html_url', 'url', 'group_category_id', 'locked', 'lock_explanation',
            'message', 'pinned'
        ]
        diss_perm_properties = [
            'attach', 'update', 'reply', 'delete'
        ] # topic_children/attachments: list
        diss_author_properties = [
            'id', 'display_name', 'avatar_image_url'
        ]
        diss_data = self.get_url_data(diss_url)
        json_data = diss_data.read().replace("while(1);", '')
        json_data = self.get_json(json_data)
        t_diss = []
        if json_data:
            for discussion in json_data:
                a_diss = {}
                for dp in diss_properties:
                    if dp in discussion.keys():
                        a_diss[dp] = discussion[dp]
                    else:
                        a_diss[dp] = ''

                db_list = [0]*15
                db_list[0] = a_diss['id']
                db_list[1] = base_title
                db_list[2] = a_diss['url']
                db_list[3] = a_diss['title']
                db_list[4] = a_diss['message']
                a_perm = a_diss['permissions']
                db_list[5] = str(int(a_perm['attach'])*1000+int(a_perm['update'])*100+int(a_perm['reply'])*10+int(a_perm['delete']))
                db_list[6] = a_diss['author']['id']
                db_list[7] = a_diss['author']['display_name']
                db_list[8] = a_diss['read_state']
                db_list[9] = a_diss['last_reply_at']
                db_list[10] = a_diss['created_at']
                db_list[11] = a_diss['updated_at']
                db_list[12] = a_diss['posted_at']
                db_list[13] = a_diss['discussion_type']
                db_list[14] = a_diss['group_category_id']
                self.cdb.op_information(db_list, 'discussions')

                a_diss['reply'] = self.get_reply(base_url, a_diss['id'], base_title, a_diss['title'])
                t_diss.append(a_diss)
                if db_list[8] == 'unread':
                    print("\t\t\t"+a_diss['title'].decode('utf-8'))
        return t_diss

    def get_information(self):
        print '\n---Begin Fetching Announcements+Discussions---'
        anno_url = 'https://sjtu-umich.instructure.com/api/v1{}/discussion_topics'
        diss_url = 'https://sjtu-umich.instructure.com/api/v1{}/discussion_topics'

        for i in range(0, len(self.course_title)):
            print '\n\t-Begin Fetching Announcements+Discussions For ' + self.course_title[i] + '-'
            c_anno_url = anno_url.format(self.course_url[i])
            c_diss_url = diss_url.format(self.course_url[i])
            self.get_announcement(c_anno_url, self.course_title[i])
            self.get_discussion(c_diss_url, self.course_title[i])

            print '\n\t-End Fetching Announcements+Discussions For ' + self.course_title[i] + '-'

        print '\n---End Fetching Announcements+Discussions---'

if __name__ == '__main__':
    jl = JaccountLogin('username', 'password', 10, 70, True)
    # print urllib2.urlopen('https://sjtu-umich.instructure.com/', timeout=10).read()
    xsoup, xres = jl.check_login()
    if not xres:
        jl.login(xsoup)
    jl.get_courses()
    jl.get_information()
    jl.get_assignments()
    jl.get_attachments()



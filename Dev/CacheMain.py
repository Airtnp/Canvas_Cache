# encoding: utf-8
from ConfigParser import ConfigParser
import urllib
import urllib2
import traceback
import os
import cookielib
import json
import socket
from math import floor
from ssl import SSLError


class CanvasConfigParser:
    """
        For parse the config in config.ini
        :
    """

    def __init__(self, file_path):
        """
        Initialize the parser and read the content.
        Keep the data in
            self.token,
            self.db_host,
            self.db_usr,
            self.db_pw,
            self.db_port
        :param file_path: the path of the config.ini
        :type file_path: string
        """
        cp = ConfigParser()
        cp.read(file_path)

        self.token = cp.get('user_info', 'token')
        self.timeout = cp.get('timeout', 'url_timeout')
        self.dtimeout = cp.get('timeout', 'download_timeout')


class CanvasCache:
    """
        Main class for caching infomation on Canvas
    """

    def __init__(self, ccp):
        """

        :param ccp: CanvasConfigParser
        :type ccp: CanvasConfigParser
        """
        self.token = ccp.token
        self.timeout = int(ccp.timeout)
        self.dtimeout = int(ccp.dtimeout)
        self.usr_id = None

        self.host_url = 'https://sjtu-umich.instructure.com/'
        self.suffix_url = '?access_token=' + self.token
        self.cj = cookielib.LWPCookieJar()
        self.cookie_support = urllib2.HTTPCookieProcessor(self.cj)
        self.opener = urllib2.build_opener(self.cookie_support, urllib2.HTTPHandler)
        urllib2.install_opener(self.opener)

        self.fl_path = 'Dev_Files'
        self.course_url = []
        self.course_title = []

    @staticmethod
    def make_dir(name):
        """

        :param name: dir name
        :type name: string
        """
        try:
            os.mkdir(name)
        except Exception as e:
            # print e
            pass

    def get_url_data(self, api_url):
        """

        :param api_url: the api url of the data
        :type api_url: string
        :return: content of the url
        :rtype: string
        """
        try:
            url = self.host_url + api_url + self.suffix_url
            data = self.opener.open(url, timeout=self.timeout).read()
        except urllib2.URLError:
            print 'URL Timeout error'
            data = None
        except SSLError:
            print 'SSL handshake error'
            data = None
        except Exception as e:
            print e
            print traceback.print_exc()
            data = None
        return data

    def download_from_url(self, url, filepath):
        """

        :param url: file url
        :type url: string
        :param filename: file name with folder path
        :type filename: string
        :return file integrity
        :rtype boolean
        """
        size = 0L

        def get_remote_file_info(url, proxy=None):

            """
            From http://blog.csdn.net/jobschen/article/details/47107691
            Get remote file information
            :param url: url
            :type url: string
            :param proxy: proxy setting
            :type proxy: dict
            :return: headers
            :rtype: dict
            """
            opener = self.opener
            if proxy:
                if url.lower().startswith('https://'):
                    opener.add_handler(urllib2.ProxyHandler({'https' : proxy}))
                else:
                    opener.add_handler(urllib2.ProxyHandler({'http' : proxy}))
            try:
                request = urllib2.Request(url)
                request.get_method = lambda: 'HEAD'
                response = opener.open(request, timeout=self.timeout)
                response.read()
            except Exception as e: # 远程文件不存在
                return 0
            else:
                return dict(response.headers)

        def report_hook(b_n, b_s, s):
            """
            get file downloading report
            :param b_n: block number
            :type b_n: integer
            :param b_s: block size
            :type b_s: integer
            :param s: total size
            :type s: integer
            """
            size = s
            per = min(100.0, 100.0 * b_n * b_s / s)

            print '\t\t|' + int(floor(per/2.5))*'*' + int(40-floor(per/2.5))*'-' + '|' + '%.2f%%' % per

        def check_integrity(filepath):
            """
            check if the file is fully downloaded.
            :param filepath: file path
            :type filepath: string
            :return: integrity
            :rtype: boolean
            """
            if os.path.exists(filepath):
                return os.path.getsize(filepath) == size
            else:
                return False

        print '\t\turl: ' + url
        print '\t\tfilename: ' + filepath
        url = url + '&access_token=' + self.token
        try:
            socket.setdefaulttimeout(self.dtimeout)
            size = long(get_remote_file_info(url)['content-length'])
            urllib.urlretrieve(url, filepath, report_hook)
        except Exception as e:
            print '\t\tError: ' + str(e)
        finally:
            print '\t\tIntegrity: ' + str(check_integrity(filepath))
            return check_integrity(filepath)


    @staticmethod
    def get_json_data(data):
        """

        :param data: string from api response
        :type data: string
        :return: data as json
        :rtype: dict
        """
        if data:
            data = json.loads(data)
        else:
            data = {}
        return data

    def get_user_id(self):
        """
        Get user id
        :return: user_id
        :rtype: integer
        """
        usr_api_url = 'api/v1/user/self'
        usr_data = self.get_url_data(usr_api_url)
        usr_data = self.get_json_data(usr_data)
        return usr_data['id']

    def get_courses(self):
        """
        Get courses id/title
        """
        print "\n---Begin Fetching Courses---"
        try:
            course_api_url = '/api/v1/courses'
            course_data = self.get_url_data(course_api_url)
            courses = self.get_json_data(course_data)
            for course in courses:
                print course['name']
                self.course_url.append('/courses/' + str(course['id']))
                self.course_title.append(course['name'])
            print "---End Fetching Courses---"
        except Exception as e:
            print e
            print traceback.print_exc()

    def get_folder_file(self, fid, path_prefix, file_record):
        """

        :param fid: file id
        :type fid: integer | string
        :param path_prefix: relative path of file
        :type path_prefix: string
        :param file_record: dict of files
        :type file_record: dict
        """

        fc = file_record

        try:
            self.make_dir(path_prefix)
            fid = str(fid)
            file_api_url = 'api/v1/folders/' + fid + '/files'
            file_data = self.get_url_data(file_api_url)
            files = self.get_json_data(file_data)
            for xfile in files:
                fl = {}
                fl['id'] = xfile['id']
                fl['url'] = xfile['url']
                fl['locked'] = xfile['locked']
                fl['updated_at'] = xfile['updated_at']
                title = xfile['display_name'].split(".")
                if len(title) == 1:
                    fl['title'] = path_prefix + '/' + title[0] + '_' + str(xfile['id'])
                else:
                    fl['title'] = path_prefix + '/' + ".".join(title[0:len(title) - 1]) + '_' + str(
                            xfile['id']) + '.' + title[-1]
                if not fl['locked'] and not (str(fl['id']) in fc.keys()):
                    intg = self.download_from_url(fl['url'], fl['title'])
                    if intg:
                        fl['download_status'] = True
                    else:
                        fl['download_status'] = False
                    fc[fl['id']] = fl

        except urllib2.URLError:
            print 'URL Timeout error'
        except SSLError:
            print 'SSL handshake error'
        except Exception as e:
            print e
            print traceback.print_exc()

    def get_folder(self, fid, path_prefix):
        """

        :param fid: folder id
        :type fid:  integer | string
        :param path_prefix: the relative path of the folder
        :type path_prefix: string
        """

        def get_file_record():
            """
            Get current record in this dir
            :return: file record dict
            :rtype: dict
            """
            if not os.path.exists(path_prefix + '/' + 'file_record'):
                f = open(path_prefix + '/' + 'file_record', 'w+')
                f.close()
                # os.system('attrib +H ' + os.getcwd() + '/' + path_prefix + '/' + 'file_record') # TODO: chmod in *nix
                return {}
            else:
                f = open(path_prefix + '/' + 'file_record', 'rt')
                return self.get_json_data(f.read())

        def update_file_record(file_dict):
            """
            update file dict
            :param file_dict: file dict
            :type file_dict: dict
            """
            f = open(path_prefix + '/' + 'file_record', 'wt')
            f.write(json.dumps(file_dict))

        self.make_dir(path_prefix)
        fc = get_file_record() or {}

        try:
            fid = str(fid)
            self.get_folder_file(fid, path_prefix, fc)

            folder_api_url = 'api/v1/folders/' + fid + '/folders'
            folder_data = self.get_url_data(folder_api_url)
            folder_data = self.get_json_data(folder_data)
            for xfolder in folder_data:
                print('\n\t\tFolder-' + path_prefix + "/" + xfolder['name'])
                self.get_folder(xfolder['id'], path_prefix + '/' + xfolder['name'])
        except urllib2.URLError:
            print 'URL Timeout error'
        except SSLError:
            print 'SSL handshake error'
        except Exception as e:
            print e
            print traceback.print_exc()
        finally:
            update_file_record(fc)

    def get_all_file(self):
        """
        Get files
        """
        print "\n---Begin Fetching Files---"
        try:
            if not self.course_url:
                self.get_courses()
            self.make_dir(self.fl_path)
            for i in range(0, len(self.course_url)):
                print "\n\t-Begin Files for " + self.course_title[i] + '-'
                self.make_dir(self.fl_path + '/' + self.course_title[i])
                files_root_url = 'api/v1' + self.course_url[i] + '/folders/root'
                files_root_data = self.get_url_data(files_root_url)
                files_root = self.get_json_data(files_root_data)
                # self.get_folder_file(files_root['id'], self.fl_path + '/' + self.course_title[i], fc)
                self.get_folder(files_root['id'], self.fl_path + '/' + self.course_title[i])
                print "\t-End Files for " + self.course_title[i] + '-'
                break
            print "---End Fetching Files---"
        except urllib2.URLError:
            print 'URL Timeout error'
        except SSLError:
            print 'SSL handshake error'
        except Exception as e:
            print e
            print traceback.print_exc()

if __name__ == '__main__':
    ccp = CanvasConfigParser('Config.ini')
    cc = CanvasCache(ccp)
    cc.get_all_file()

# encoding: utf-8
from ConfigParser import ConfigParser
import urllib
import urllib2
import traceback
import os
import cookielib
import re
import json
from bs4 import BeautifulSoup
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
        self.db_host = cp.get('database', 'db_host')
        self.db_usr = cp.get('database', 'db_usr')
        self.db_pw = cp.get('database', 'db_pw')
        self.db_port = cp.get('database', 'db_port')


class CanvasCache:
    """
        Main class for caching infomation on Canvas
    """

    def __init__(self, token, timeout, db_host, db_usr, db_pw, db_port):
        """

        :param token: canvas token
        :type token: string
        :param timeout: timeout for waiting for response
        :type timeout: integer
        :param db_host: database host
        :type db_host: string
        :param db_usr: database user
        :type db_usr: string
        :param db_pw: database password
        :type db_pw: string
        :param db_port: database port
        :type db_port: integer
        """
        self.token = token
        self.timeout = timeout
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

    def download_from_url(self, url, filename):
        """

        :param url: file url
        :type url: string
        :param filename: file name with folder path
        :type filename: string
        """
        url = url + '&access_token=' + self.token
        urllib.urlretrieve(url, filename)

    @staticmethod
    def get_json_data(data):
        """

        :param data: string from api response
        :type data: string
        :return: data as json
        :rtype: dict
        """
        data = json.loads(data)
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

    def get_folder_file(self, fid, path_prefix):
        """

        :param fid: file id
        :type fid: integer
        :param path_prefix: relative path of file
        :type path_prefix: string
        """
        try:
            self.make_dir(path_prefix)
            fid = str(fid)
            file_api_url = 'api/v1/folders/' + fid + '/files'
            file_data = self.get_url_data(file_api_url)
            files = self.get_json_data(file_data)
            for xfile in files:
                fl = {}
                fl['url'] = xfile['url']
                title = xfile['display_name'].split(".")
                if len(title) == 1:
                    fl['title'] = path_prefix + '/' + title[0] + '_' + str(xfile['id'])
                else:
                    fl['title'] = path_prefix + '/' + ".".join(title[0:len(title) - 1]) + '_' + str(
                            xfile['id']) + '.' + title[-1]
                self.download_from_url(fl['url'], fl['title'])
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
        :type fid:  integer
        :param path_prefix: the relative path of the folder
        :type path_prefix: string
        """
        try:
            fid = str(fid)
            folder_api_url = 'api/v1/folders/' + fid + '/folders'
            folder_data = self.get_url_data(folder_api_url)
            folder_data = self.get_json_data(folder_data)
            for xfolder in folder_data:
                self.get_folder_file(fid, path_prefix)
                print('\n\t\tFolder-' + path_prefix + "/" + xfolder['name'])
                self.get_folder(xfolder['id'], path_prefix + '/' + xfolder['name'])
        except urllib2.URLError:
            print 'URL Timeout error'
        except SSLError:
            print 'SSL handshake error'
        except Exception as e:
            print e
            print traceback.print_exc()

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
                self.get_folder_file(files_root['id'], self.fl_path + '/' + self.course_title[i])
                self.get_folder(files_root['id'], self.fl_path + '/' + self.course_title[i])
                print "\t-End Files for " + self.course_title[i] + '-'
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
    cc = CanvasCache(ccp.token, 5, ccp.db_host, ccp.db_usr, ccp.db_pw, ccp.db_port)
    cc.get_all_file()

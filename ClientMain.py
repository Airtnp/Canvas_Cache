# encoding: utf-8
from LoginJaccount import JaccountLogin
from LoginTimeout import TimeoutThread
import Interfaces.ClientInterface as ClientInterface
import Interfaces.ClientMessageBox as ClientMessageBox
import Interfaces.ClientWidget as ClientWidget
import Interfaces.ClientLog as ClientLogWindow
from PyQt4.QtGui import *
from PyQt4.QtCore import *

import traceback
import sys
import locale
import time
import threading

try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

'''
Need to add:
1. Dialog for log (completing require 8)
2. thread for logining
3. check pw and usr
4. table for assignments & files & announcements
5. Announcements + Discussion
6. https://canvas.instructure.com/doc/api/discussion_topics.html
7. https://canvas.instructure.com/doc/api/announcements.html
8. Use thread to seperate UI and running function
'''


class ClientLog(QDialog, ClientLogWindow.Ui_Dialog):
    def __init__(self, parent=None):
        super(ClientLog, self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(self.width(), self.height())


class ClientMainWindow(QMainWindow, ClientInterface.Ui_MainWindow):
    def __init__(self, parent=None):
        super(ClientMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        self.timeout = 10
        self.jl = JaccountLogin('', '', self.timeout)
        self.login_signal = False
        self.captcha = None
        self.captcha_item = None
        self.scene = None
        # ClientWidget.OutputProcessMain()
        self.init_widgets()
        # self.log = ClientLog()
        # self.log.show()

    def init_widgets(self):
        self.set_status('Log out')
        self.lineEdit_2.setEchoMode(QLineEdit.Password)
        self.pushButton.clicked.connect(lambda: self.login())

        # sys.stdout = ClientWidget.OutLog(self.log.textEdit, sys.stdout)
        # sys.stderr = ClientWidget.OutLog(self.log.textEdit, sys.stderr, QColor(255, 0, 0))

        # sys.stdout = ClientWidget.ClientLogStream(textWritten=self.write_output)
        # sys.stderr = ClientWidget.ClientLogStream(textWritten=self.write_output)




        '''
        self.captcha = QImage()
        self.captcha_item = QGraphicsPixmapItem()
        self.scene = QGraphicsScene()
        self.radioButton.setChecked(True)
        self.captcha.load(r'captcha.png')
        print self.captcha.isNull()
        # self.captcha_item.setPixmap(self.captcha)
        # self.scene.addItem(self.captcha_item)
        self.graphicsView.setScene(self.scene)
        self.graphicsView.resize(self.captcha.width()+10, self.captcha.height()+10)
        self.graphicsView.show()
        '''

    @staticmethod
    def update_output(self):
        while True:
            sys.stdout.flush()
            sys.stderr.flush()
            time.sleep(1)

    def write_output(self, text):
        QApplication.processEvents()
        cursor = self.log.textEdit.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.log.textEdit.setTextCursor(cursor)
        self.log.textEdit.ensureCursorVisible()

    def set_status(self, text):
        self.label_5.setText('Status: '+text)

    def lock_captcha(self):
        if self.lineEdit_3.isEnabled():
            self.lineEdit_3.setEnabled(False)
        else:
            self.lineEdit_3.setEnabled(True)

    def check_login_pre(self):
        return self.jl.check_login()

    def login_pre(self, soup=None):
        self.jl.login(soup)

    def reset_timeout(self):
        timeout = self.lineEdit_3.text()
        try:
            timeout = int(timeout)
            self.jl.timeout = timeout
        except Exception as e:
            print 'Error Timeout'

    def login(self):
        QApplication.processEvents()
        self.reset_timeout()
        usr = self.lineEdit.text()
        pw = self.lineEdit_2.text()
        # captcha_check = self.radioButton.isChecked()
        captcha_check = True
        self.jl.check_captcha = captcha_check
        if usr and pw:
            self.jl.user = usr
            self.jl.pw = pw
            self.jl.posts['user'] = usr
            self.jl.posts['pass'] = pw
            self.jl.cdb.db_name = 'Canvas_' + 'xiaoliran12'
            if self.pushButton.text() == 'Login':
                if self.jl.check_captcha:
                    xsoup, xres = self.check_login_pre()
                    if not xres:
                        self.login_pre(xsoup)
                        self.set_status('Log in')
                        self.jl.cdb.init_db()
                        self.jl.get_courses()
                        self.jl.get_assignments()
                        self.jl.get_attachments()
                    else:
                        self.set_status('Log in')
                        self.jl.cdb.init_db()
                        self.jl.get_courses()
                        self.jl.get_assignments()
                        self.jl.get_attachments()
        else:
            msgbox = ClientMessageBox.MessageBoxDlg()
            msgbox.slotCritical(QString(u'Please input your username and password！'))


try:
    app = QApplication(sys.argv)
    my_code = locale.getpreferredencoding()
    code = QTextCodec.codecForName(my_code)
    QTextCodec.setCodecForLocale(code)
    QTextCodec.setCodecForTr(code)
    QTextCodec.setCodecForCStrings(code)
    mainwindow = ClientMainWindow()
    mainwindow.show()
    sys.exit(app.exec_())


except Exception as e:
    print e
    traceback.print_exc()





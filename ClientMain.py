# encoding: utf-8
from LoginJaccount import JaccountLogin
from LoginTimeout import TimeoutThread
import Interfaces.ClientInterface as ClientInterface
import Interfaces.ClientMessageBox as ClientMessageBox
import Interfaces.ClientWidget as ClientWidget
from PyQt4.QtGui import *
from PyQt4.QtCore import *

import traceback
import sys
import locale

try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

'''
Need to add:
1. Dialog for log
2. thread for logining
3. check pw and usr
4. table for assignments & files & announcements
5. Announcements + Discussion
6. https://canvas.instructure.com/doc/api/discussion_topics.html
7. https://canvas.instructure.com/doc/api/announcements.html
'''


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
        self.init_widgets()

    def init_widgets(self):
        self.set_status('Log out')
        # sys.stdout = ClientWidget.OutLog(self.textBrowser, sys.stdout)
        # sys.stderr = ClientWidget.OutLog(self.textBrowser, sys.stderr, QColor(255, 0, 0))
        self.lineEdit_2.setEchoMode(QLineEdit.Password)
        self.pushButton.clicked.connect(lambda: self.login())
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

    def set_status(self, text):
        self.label_5.setText('Status: '+text)

    def lock_captcha(self):
        if self.lineEdit_3.isEnabled():
            self.lineEdit_3.setEnabled(False)
        else:
            self.lineEdit_3.setEnabled(True)

    def login_pre(self, params):
        self.jl.login(ui_params=params)

    def login(self):
        usr = self.lineEdit.text()
        pw = self.lineEdit_2.text()
        captcha_check = self.radioButton.isChecked()
        self.jl.check_captcha = captcha_check
        if usr and pw:
            self.jl.user = usr
            self.jl.pw = pw
            self.jl.posts['user'] = usr
            self.jl.posts['pass'] = pw
            if self.pushButton.text() == 'Login':
                ui_params = {
                        'window': self,
                }
                if self.jl.check_captcha:
                    xsoup, xres = self.jl.check_login()
                    if not xres:
                        self.jl.login(xsoup, ui_params=ui_params)
                        self.set_status('Log in')
                        self.jl.cdb.init_db()
                    else:
                        self.set_status('Log in')
                        self.jl.cdb.init_db()
                else:
                    self.pushButton.setText('Enter Captcha')
                    TimeoutThread(10000, self.login_pre, ui_params)
            if not self.login_signal and self.pushButton.text() == 'Enter Captcha':
                self.login_signal = True
                self.pushButton.setText('Login')

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





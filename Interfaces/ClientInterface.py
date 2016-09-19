# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'client.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(679, 473)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.tabFunc = QtGui.QTabWidget(self.centralwidget)
        self.tabFunc.setGeometry(QtCore.QRect(20, 20, 631, 401))
        self.tabFunc.setObjectName(_fromUtf8("tabFunc"))
        self.tabLogin = QtGui.QWidget()
        self.tabLogin.setObjectName(_fromUtf8("tabLogin"))
        self.lineEdit = QtGui.QLineEdit(self.tabLogin)
        self.lineEdit.setGeometry(QtCore.QRect(220, 150, 171, 20))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.lineEdit_2 = QtGui.QLineEdit(self.tabLogin)
        self.lineEdit_2.setGeometry(QtCore.QRect(220, 190, 171, 20))
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.lineEdit_3 = QtGui.QLineEdit(self.tabLogin)
        self.lineEdit_3.setGeometry(QtCore.QRect(220, 230, 171, 20))
        self.lineEdit_3.setObjectName(_fromUtf8("lineEdit_3"))
        self.label = QtGui.QLabel(self.tabLogin)
        self.label.setGeometry(QtCore.QRect(150, 150, 71, 21))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.tabLogin)
        self.label_2.setGeometry(QtCore.QRect(150, 190, 71, 21))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(self.tabLogin)
        self.label_3.setGeometry(QtCore.QRect(150, 222, 71, 31))
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(self.tabLogin)
        self.label_4.setGeometry(QtCore.QRect(130, 40, 411, 91))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("OCR A Extended"))
        font.setPointSize(25)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.graphicsView = QtGui.QGraphicsView(self.tabLogin)
        self.graphicsView.setGeometry(QtCore.QRect(420, 200, 111, 51))
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.pushButton = QtGui.QPushButton(self.tabLogin)
        self.pushButton.setGeometry(QtCore.QRect(240, 310, 161, 41))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.radioButton = QtGui.QRadioButton(self.tabLogin)
        self.radioButton.setGeometry(QtCore.QRect(420, 160, 131, 21))
        self.radioButton.setObjectName(_fromUtf8("radioButton"))
        self.tabFunc.addTab(self.tabLogin, _fromUtf8(""))
        self.tabAssignment = QtGui.QWidget()
        self.tabAssignment.setObjectName(_fromUtf8("tabAssignment"))
        self.tableWidget = QtGui.QTableWidget(self.tabAssignment)
        self.tableWidget.setGeometry(QtCore.QRect(40, 110, 551, 181))
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.pushButton_2 = QtGui.QPushButton(self.tabAssignment)
        self.pushButton_2.setGeometry(QtCore.QRect(240, 310, 161, 41))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.label_7 = QtGui.QLabel(self.tabAssignment)
        self.label_7.setGeometry(QtCore.QRect(110, 10, 411, 91))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("OCR A Extended"))
        font.setPointSize(25)
        self.label_7.setFont(font)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.tabFunc.addTab(self.tabAssignment, _fromUtf8(""))
        self.tabFile = QtGui.QWidget()
        self.tabFile.setObjectName(_fromUtf8("tabFile"))
        self.tableWidget_2 = QtGui.QTableWidget(self.tabFile)
        self.tableWidget_2.setGeometry(QtCore.QRect(40, 110, 551, 181))
        self.tableWidget_2.setObjectName(_fromUtf8("tableWidget_2"))
        self.tableWidget_2.setColumnCount(0)
        self.tableWidget_2.setRowCount(0)
        self.pushButton_3 = QtGui.QPushButton(self.tabFile)
        self.pushButton_3.setGeometry(QtCore.QRect(240, 310, 161, 41))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.label_8 = QtGui.QLabel(self.tabFile)
        self.label_8.setGeometry(QtCore.QRect(110, 10, 411, 91))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("OCR A Extended"))
        font.setPointSize(25)
        self.label_8.setFont(font)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.tabFunc.addTab(self.tabFile, _fromUtf8(""))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.textBrowser = QtGui.QTextBrowser(self.tab)
        self.textBrowser.setGeometry(QtCore.QRect(20, 30, 591, 321))
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.tabFunc.addTab(self.tab, _fromUtf8(""))
        self.label_6 = QtGui.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(290, 420, 121, 31))
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.label_5 = QtGui.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(530, 0, 131, 41))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabFunc.setCurrentIndex(3)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label.setText(_translate("MainWindow", "Username", None))
        self.label_2.setText(_translate("MainWindow", "Password", None))
        self.label_3.setText(_translate("MainWindow", "Captcha", None))
        self.label_4.setText(_translate("MainWindow", "SJTU Jaccount Login", None))
        self.pushButton.setText(_translate("MainWindow", "Login", None))
        self.radioButton.setText(_translate("MainWindow", "Auto fill captcha", None))
        self.tabFunc.setTabText(self.tabFunc.indexOf(self.tabLogin), _translate("MainWindow", "Login", None))
        self.pushButton_2.setText(_translate("MainWindow", "Cache Assignments", None))
        self.label_7.setText(_translate("MainWindow", "Canvas Assignments", None))
        self.tabFunc.setTabText(self.tabFunc.indexOf(self.tabAssignment), _translate("MainWindow", "Assignments", None))
        self.pushButton_3.setText(_translate("MainWindow", "Cache Files", None))
        self.label_8.setText(_translate("MainWindow", "Canvas Files", None))
        self.tabFunc.setTabText(self.tabFunc.indexOf(self.tabFile), _translate("MainWindow", "Files", None))
        self.tabFunc.setTabText(self.tabFunc.indexOf(self.tab), _translate("MainWindow", "Log", None))
        self.label_6.setText(_translate("MainWindow", "Tips: ", None))
        self.label_5.setText(_translate("MainWindow", "Status: Login in", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


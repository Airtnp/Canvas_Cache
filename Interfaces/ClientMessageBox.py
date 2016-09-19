# -*- coding: utf-8 -*-
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
import locale

my_code = locale.getpreferredencoding()
code = QTextCodec.codecForName(my_code)
QTextCodec.setCodecForLocale(code)
QTextCodec.setCodecForTr(code)
QTextCodec.setCodecForCStrings(code)

try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

# QTextCodec.setCodecForTr(QTextCodec.codecForName("UTF-8"))


class MessageBoxDlg:
    def __init__(self):
        pass

    def tr(self, text):
        return QString(text)
        
    def close(self):
        pass

    def slotQuestion(self, text):
        button=QMessageBox.question(None,"Question",
                                    self.tr(text),
                                    QMessageBox.Ok|QMessageBox.Cancel,
                                    QMessageBox.Ok)
        if button==QMessageBox.Ok:
            # self.label.setText("Question button/Ok")
            return True
        elif button==QMessageBox.Cancel:
            # self.label.setText("Question button/Cancel")
            return False
        else:
            return False

    def slotInformation(self, text):
        QMessageBox.information(None,"Information",
                                self.tr(text),
                                QMessageBox.Ok, 
                                QMessageBox.Ok)
        # self.label.setText("Information MessageBox")

    def slotWarning(self):
        button=QMessageBox.warning(None,"Warning",
                                   self.tr("是否保存对文档的修改?"),
                                   QMessageBox.Save|QMessageBox.Discard|QMessageBox.Cancel,
                                   QMessageBox.Save)
        if button==QMessageBox.Save:
            self.label.setText("Warning button/Save")
        elif button==QMessageBox.Discard:
            self.label.setText("Warning button/Discard")
        elif button==QMessageBox.Cancel:
            self.label.setText("Warning button/Cancel")
        else:
            return

    def slotCritical(self, text):
        QMessageBox.critical(None,"Critical",
                             self.tr(text), 
                             QMessageBox.Ok, 
                             QMessageBox.Ok)
        # self.label.setText("Critical MessageBox")

    def slotAbout(self):
        QMessageBox.about(None,"About",self.tr("About事例"))
        self.label.setText("About MessageBox")

    def slotAboutQt(self):
        QMessageBox.aboutQt(None,"About Qt")
        self.label.setText("About Qt MessageBox")

    def slotCustom(self):
        customMsgBox=QMessageBox(None)
        customMsgBox.setWindowTitle("Custom message box")
        lockButton=customMsgBox.addButton(self.tr("锁定"),
                                          QMessageBox.ActionRole)
        unlockButton=customMsgBox.addButton(self.tr("解锁"),
                                            QMessageBox.ActionRole)
        cancelButton=customMsgBox.addButton("cancel",QMessageBox.ActionRole)

        customMsgBox.setText(self.tr("这是一个自定义消息框!"))
        customMsgBox.exec_()

        button=customMsgBox.clickedButton()
        if button==lockButton:
            self.label.setText("Custom MessageBox/Lock")
        elif button==unlockButton:
            self.label.setText("Custom MessageBox/Unlock")
        elif button==cancelButton:
            self.label.setText("Custom MessageBox/Cancel")

if __name__ == '__main__':
    app=QApplication(sys.argv)
    MessageBox=MessageBoxDlg()
    MessageBox.show()
    app.exec_()


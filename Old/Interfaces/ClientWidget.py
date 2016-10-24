# http://stackoverflow.com/questions/17132994/pyside-and-python-logging/17145093#17145093
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import sys

class OutLog:
    def __init__(self, edit, out=None, color=None):
        """(edit, out=None, color=None) -> can write stdout, stderr to a
        QTextEdit.
        edit = QTextEdit
        out = alternate stream ( can be the original sys.stdout )
        color = alternate color (i.e. color stderr a different color)
        """
        self.edit = edit
        self.out = None
        self.color = color

    def write(self, m):
        if self.color:
            tc = self.edit.textColor()
            self.edit.setTextColor(self.color)

        self.edit.moveCursor(QtGui.QTextCursor.End)
        self.edit.insertPlainText(m)

        if self.color:
            self.edit.setTextColor(tc)

        if self.out:
            self.out.write(m)

    def flush(self):
        self.edit.flush()


class ClientThread(QtCore.QThread):
    def __init__(self, func, params):
        super(ClientThread, self).__init__()
        self.func = func
        self.params = params
        self.trigger = QtCore.pyqtSignal()

    def run(self):
        self.func(self.params)
        self.trigger.emit()


class ClientLogStream(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))

    def flush(self):
        pass


class ClientLogProcess(QtCore.QProcess):
    def __init__(self, edit=None):
        # Call base class method
        QtCore.QProcess.__init__(self)
        # Create an instance variable here (of type QTextEdit)
        self.edit = QtGui.QTextEdit()
        self.edit.setWindowTitle("QTextEdit Standard Output Redirection")
        self.edit.show()

    # Define Slot Here
    @QtCore.pyqtSlot()
    def readStdOutput(self):
        self.edit.append(QtCore.QString(self.readAllStandardOutput()))


def OutputProcessMain():
    app = QtGui.QApplication(sys.argv)
    output_process = ClientLogProcess()
    output_process.setProcessChannelMode(QtCore.QProcess.MergedChannels)
    output_process.start('ldconfig -v')
    QtCore.QObject.connect(output_process, QtCore.SIGNAL('readyReadStandardOutput()'), output_process, QtCore.SLOT('readStdOutput()'))

    return app.exec_()


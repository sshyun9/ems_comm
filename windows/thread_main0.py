# PyQt5 템플릿소스
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class MyApp(QWidget): # QMainWindow로 변경요
    def __init__(self):
        super(MyApp, self).__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('./windows/ui/threadtask.ui', self) # UI변경필요
        # TODO 로직은 여기에 작성
        self.show()

    def initUI(self):
        pass

if __name__=='__main__':
    app = QApplication(sys.argv)
    win=MyApp()
    app.exec_()

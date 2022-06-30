# 스레드사용/커스텀시그널사용
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import time

# PyQt에서 스레드 사용하기 위한 클래스
class Worker(QThread):
    valChangeSignal = pyqtSignal(int)

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.working = True
    
    def run(self):
        # 스레드로 동작할 내용
        # self.parent.pgbTask.setRange(0,99)
        while self.working:
            for i in range(0,100):
                print(f'출력 > {i}')
                self.valChangeSignal.emit(i)
                # self.parent.pgbTask.setValue(i)
                # self.parent.txbLog.append(f'출력 > {i}')

class MyApp(QWidget): # QMainWindow로 변경요
    
    def __init__(self):
        super(MyApp, self).__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('./windows/ui/threadtask.ui', self)
        self.btnStart.clicked.connect(self.btnStartClicked)
        # Worker 클래스가 가지고 있는  valchangeSignal 설정
        self.th = Worker(self)
        self.th.valChangeSignal.connect(self.updateProgress) # 슬롯정의
        self.show()

    @pyqtSlot(int) # int (parameter) 빠지면 오류
    def updateProgress(self, i):
        self.pgbTask.setValue(i)
        self.txbLog.append(f'출력 > {i}')
        if i == 99:
            self.th.working = False
    
    @pyqtSlot()
    def btnStartClicked(self):
        self.pgbTask.setRange(0, 99)
        # th.Worker(self)
        self.th.start()
        self.th.working = True

if __name__=='__main__':
    app = QApplication(sys.argv)
    win=MyApp()
    app.exec_()
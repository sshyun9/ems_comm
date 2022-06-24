# 버튼
import sys #  argv 때문에
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class MyApp(QWidget):

    def __init__(self) -> None:
        super().__init__()
        self.initUI()  # 스스로 UI 초기화

    def initUI(self):
        self.setWindowTitle('QPushButton')
        self.setGeometry(490,250,300,300)
        self.setWindowIcon(QIcon('lion2.png'))

        btn1 = QPushButton('Hello', self)
        # btn1.setEnabled(False) # 버튼 안눌림
        btn1.clicked.connect(self.btn1_click)

        vbox = QVBoxLayout(self)
        vbox.addWidget(btn1)

        self.show()

    def btn1_click(self):  #슬롯
        QMessageBox.about(self, 'greeting', 'Hi, everyone~')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = MyApp()

    app.exec_()


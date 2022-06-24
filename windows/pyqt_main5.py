#버튼
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
        self.setGeometry(800,390,320,300)
        self.setWindowIcon(QIcon('url(./windows/images/lion.png'))

        btn1 = QPushButton('Click1', self)
        btn2 = QPushButton('Click2', self)
        btn3 = QPushButton('Click3', self)
        btn4 = QPushButton('Click4', self)
        btn5 = QPushButton('Click5', self)
        # btn1.setGeometry(50,100,100,40) -> hbox 쓰면 쓸모없음..
        # QHBoxLayout  QVBoxLayout  QGridLayout
        vbox = QVBoxLayout(self)
        vbox.addWidget(btn1, 0, 0)
        vbox.addWidget(btn2, 0, 0)
        vbox.addWidget(btn3, 0, 0)
        vbox.addWidget(btn4, 0, 0)
        vbox.addWidget(btn5, 0, 0)


        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = MyApp()

    app.exec_()


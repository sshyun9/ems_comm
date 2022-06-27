# 버튼, 슬라이더, 다이얼
import sys #  argv 때문에
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class MyApp(QWidget):

    def __init__(self) -> None:
        super().__init__()
        self.initUI()  # 스스로 UI 초기화

    def initUI(self):
        self.setWindowTitle('Signal')
        self.setGeometry(490, 250, 300, 300)
        self.setWindowIcon(QIcon('lion2.png'))

        self.label = QLabel(self)
        self.label.setFont(QFont('Arial', 16))

        self.btn = QPushButton('LED ON', self)

        # 시그널 정의
        self.btn.clicked.connect(self.btn_clicked)

        # 화면 구성
        vbox = QVBoxLayout(self)
        vbox.addWidget(self.label)
        vbox.addWidget(self.btn)

        self.show()

    def btn_clicked(self):
       self.label.setText('LED ON')
       # raspberry pi GPIO ON

    def btn1_click(self):  #슬롯
        QMessageBox.about(self, 'greeting', 'Hi, everyone~')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = MyApp()

    app.exec_()


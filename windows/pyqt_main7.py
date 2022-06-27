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
        self.setWindowTitle('QSlider&QDial')
        self.setGeometry(490,250,300,300)
        self.setWindowIcon(QIcon('lion2.png'))

        # 슬라이더
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setRange(0,50)
        self.slider.setSingleStep(10) # ()안의 숫자 단위로 올라감
        self.slider.setTickPosition(1) # 슬라이더

        # 다이얼
        self.dial = QDial(self)
        self.dial.setRange(0, 50)
        self.dial.setSingleStep(5)

        self.btn = QPushButton('Reset', self)

        # 시그널 정의
        self.slider.valueChanged.connect(self.slider_changed)
        self.dial.valueChanged.connect(self.dial_changed)
        self.btn.clicked.connect(self.btn_clicked)

        # 화면 구성
        vbox = QVBoxLayout(self)
        vbox.addWidget(self.slider)
        vbox.addWidget(self.dial)
        vbox.addWidget(self.btn)

        self.show()

    def slider_changed(self):
        val = self.slider.value()
        self.dial.setValue(val)
    
    def dial_changed(self):
        val = self.dial.value()
        self.slider.setValue(val)

    def btn_clicked(self):
        self.slider.setValue(0)
        self.dial.setValue(0)

    def btn1_click(self):  #슬롯
        QMessageBox.about(self, 'greeting', 'Hi, everyone~')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = MyApp()

    app.exec_()


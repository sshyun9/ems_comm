## PyQt 클래스화 / PyQt 템플릿
import sys #  argv 때문에
from PyQt5.QtWidgets import QApplication, QWidget

class MyApp(QWidget):

    def __init__(self) -> None:
        super().__init__()
        self.initUI()  # 스스로 UI 초기화

    def initUI(self):
        self.setWindowTitle('PyQt Widget2')
        # self.move(800, 390) # 정중앙위치 구식계산방법 : 1980*1080 해상도 X-> 1980/2-320/2  Y-> 1080/2-300/2
        # self.resize(320, 300)
        self.setGeometry(800,390,320,300) # 위에 self.move, resize 합친거
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = MyApp()

    app.exec_()


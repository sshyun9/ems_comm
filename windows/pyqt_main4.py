## QLabel Widget
import sys #  argv 때문에
from PyQt5.QtWidgets import *
from PyQt5.QtGui import * #QPainter, QColor, QFont  # 위젯 X, 속성
from PyQt5. QtCore import Qt # Core 속성

class MyApp(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.initUI()  # 스스로 UI 초기화

    def initUI(self):
        self.setWindowTitle('PyQt QLabel')
        self.setGeometry(800,390,320,300) # 위치
        self.setWindowIcon(QIcon('lion.png'))

        # Label 작업 시작
        label1, label2 = QLabel('라벨1은 아래로'), QLabel('라벨2는 가운데')
        label1.setAlignment(Qt.AlignBottom)
        label1.setStyleSheet(
            ('border-width: 3px;'
             'border-style: solid;'
             'border-color: blue;'
             'image: url(./windows/images/image1.png)')
        )
        label2.setAlignment(Qt.AlignCenter)
        label2.setStyleSheet(
            ('border-width: 3px;'
             'border-style: dot-dot-dash;'
             'border-color: green;'
             'image: url(./windows/images/image2.png)')
        )

        hbox = QHBoxLayout(self)
        hbox.addWidget(label1)
        hbox.addWidget(label2)



        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = MyApp()

    app.exec_()


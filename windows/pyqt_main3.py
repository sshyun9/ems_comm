## QFont 위젯 사용
import sys #  argv 때문에
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import Qt

class MyApp(QWidget):

    def __init__(self) -> None:
        super().__init__()
        self.initUI()  # 스스로 UI 초기화

    def initUI(self):
        self.setWindowTitle('QFont test')
        self.setGeometry(800,390,320,300) # 위에 self.move, resize 합친거
        self.text = 'Test Massage'
        self.show()

    def paintEvent(self, signal):
        paint = QPainter(self)
        paint.begin(self)
        self.drawText(signal, paint)
        paint.end()

    def drawText(self, signal, paint):
        paint.setPen(QColor(70,70,255)) # 색상 (R,G,B) 0-255
        paint.setFont(QFont('Impact', 20))
        paint.drawText(105,100, 'Hello Qt!')
        paint.setPen(QColor(100,100,100))
        paint.setFont(QFont('Arial',16))
        paint.drawText(signal.rect(), Qt.AlignCenter, self.text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = MyApp()

    app.exec_()


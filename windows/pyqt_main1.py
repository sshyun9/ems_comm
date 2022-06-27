## PYQT 학습
from PyQt5.QtWidgets import *
import sys

def run():
    app = QApplication(sys.argv) # 1. app 객체 생성

    wnd = QMainWindow()  # 2. window 객체 생성 Qwidget, QDialog 셋 다 가능!
    label = QLabel('\tHello Qt5!!')  # 라벨위젯 생성
    wnd.setWindowTitle('First PyQt')
    wnd.resize(500,300) # 윈도우 창 크기
    wnd.setCentralWidget(label)  # 윈도우 위아래정중앙 위치
    wnd.show() #3. 

    app.exec_() #4. 

if __name__ == '__main__':
    run()
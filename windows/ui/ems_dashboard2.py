# EMS 대시보드앱
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import * 

import requests
import json
import dashboard_rc # 리소스 py파일 추가
import time
import paho.mqtt.client as mqtt # mqtt subscribe를 위해서 추가
import datetime as dt

# pip install PyMySQL
import pymysql

# pip install pyqtgraph
# pip install pyqtchart
from PyQt5.QtChart import *

broker_url = '127.0.0.1' # 로컬에 MQTT broker가 같이 설치되어 있으므로

class Worker(QThread):
    sigStatus = pyqtSignal(str) # 연결상태 시그널, 부모클래스 MyApp 전달용
    sigMessage = pyqtSignal(dict) # MQTT Subscribe 시그널, MyApp 전달 딕셔너리형

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.host = broker_url
        self.port = 1883
        self.client = mqtt.Client(client_id='Dashboard')

    def onConnect(self, mqttc, obj, flags, rc):
        try:
            print(f'connected with result code > {rc}')
            self.sigStatus.emit('SUCCEED') # MyApp으로 성공메시지 전달
        except Exception as e:
            print(f'error > {e.args}')
            self.sigStatus.emit('FAILED')

    def onMessage(self, mqttc, ogj, msg):
        rcv_msg = str(msg.payload.decode('utf-8'))
        # print(f'{msg.topic} / {rcv_msg}')  # 시그널로 전달했으므로 주석처리
        self.sigMessage.emit(json.loads(rcv_msg))

        time.sleep(2.0)
    
    def mqttloop(self):
        self.client.loop()
        print('MQTT client loop')
    
    def run(self): # Thread에서는  run() 필수 
        self.client.on_connect = self.onConnect
        self.client.on_message = self.onMessage
        self.client.connect(self.host, self.port)
        self.client.subscribe(topic='ems/rasp/data/')
        self.client.loop_forever()

class MyApp(QMainWindow):
    isTempAlarmed = False
    isHumidAlarmed = False
    tempData = humidData = None
    idx = 0

    def __init__(self):
        super(MyApp, self).__init__()
        self.initUI()
        self.showTime()
        self.showWeather()
        self.initThread()
        self.initChart()

    def initChart(self):
        # self.viewLimit = 128 # chart 그릴갯수 제한

        self.tempData = self.humidData = QLineSeries()  # 초기화
        self.iotChart = QChart()

        # axisX = QDateTimeAxis()
        # axisX.setFormat('HH:mm:ss')
        # axisX.setTickCount(5)
        # dt = QDateTime.currentDateTime()
        # axisX.setRange(dt, dt.addSecs(self.viewLimit))

        # axisY = QValueAxis()
        
        self.iotChart = QChart()
        # self.iotChart.addAxis(axisX, Qt.AlignBottom)
        # self.iotChart.addAxis(axisY, Qt.AlignLeft)
        # self.tempData.attachAxis(axisX)
        # self.humidData.attachAxis(axisX)

        self.iotChart.layout().setContentsMargins(5,5,5,5)

        self.dataView.setChart(self.iotChart)
        self.dataView.setRenderHints(QPainter.Antialiasing)

    def initThread(self):
        self.myThread = Worker(self)
        self.myThread.sigStatus.connect(self.updateStatus)
        self.myThread.sigMessage.connect(self.updateMessage)
        self.myThread.start()

    @pyqtSlot(dict)
    def updateMessage(self, data):
        # 1. 딕셔너리 분해
        # 2. Label에 Device 명칭 업데이트
        # 3. 온도, 습도 label 현재 온도, 습도 업데이트
        # 4. MySQL DB에 입력
        # 5. 이상기온 알람
        # 6. txbLog 출력
        # 7. chart Data 추가
        
        print(data)
        dev_id = data['DEV_ID']
        self.lblTempTitle.setText(f'{dev_id} Temperature')
        self.lblHumidTitle.setText(f'{dev_id} Humidity')
        temp = data['TEMP']
        self.lblCurrTemp.setText(f'{temp:.1f}')
        humid = data['HUMID']
        self.lblCurrHumid.setText(f'{humid:.0f}')
        # self.txbLog.append(json.dumps(data))
        # self.dialHumid.setValue(int(humid))   # 220701 위젯삭제

        #5.
        if temp >= 30.0:
            self.lblTempAlarm.setText(f'{dev_id} 이상기온감지')
            # self.btnTempAlarm.setEnabled(True) # 버튼활성화
            # self.btnTempStop.setEnabled(False) 
            if self.isTempAlarmed == False:
                self.isTempAlarmed = True   # 경고메세지 한번 뜨고 안뜸
                QMessageBox.warning(self, '경고', f'{dev_id}에서 이상기온 감지!!')
        elif temp <= 26.0 :
            self.lblTempAlarm.setText(f'{dev_id} 정상기온')
            # self.btnTempAlarm.setEnabled(False) # 버튼활성화
            # self.btnTempStop.setEnabled(True) 
            self.isTempAlarmed = False

        if humid >= 85.0:
            self.lblHumidAlarm.setText(f'{dev_id} 이상습도감지')
            if self.isHumidAlarmed == False:
                self.isHumidAlarmed = True
                QMessageBox.warning(self, '경고', f'{dev_id}에서 이상습도 감지!!')
        elif humid <= 65.0:
            self.lblHumidAlarm.setText(f'{dev_id} 정상습도')
            self.isHumidAlarmed == False

        # 4. DB입력
        self.conn = pymysql.connect(host='127.0.0.1',
                                    user='bms',
                                    password='1234',
                                    db='bms',
                                    charset='euckr')

        curr_dt = data['CURR_DT']
        query = '''INSERT INTO ems_data
                            (dev_id, curr_dt, temp, humid)
                    VALUES
                            (%s, %s, %s, %s) '''

        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(query, (dev_id, curr_dt, temp, humid))
                self.conn.commit()
                print('DB Inserted!')
        
        #7 chart 업데이트
        self.updateChart(curr_dt, temp, humid)
    
    def updateChart(self, curr_dt, temp, humid):
        self.tempData.append(self.idx, temp)
        self.humidData.append(self.idx, humid)

    
    @pyqtSlot(str)
    def updateStatus(self, stat):
        if stat == 'SUCCEED':
            self.lblStatus.setText('Connected!')
            self.connFrame.setStyleSheet(
            'background-image: url(:/green);'
            'background-repeat : none;'
            'border : none;'
            )
        else:
            self.lblStatus.setText('Disconnected')
            self.connFrame.setStyleSheet(
            'background-image: url(:/red);'
            'background-repeat : none;'
            'border : none;'
            )

    def initUI(self):
        uic.loadUi('./windows/ui/dashboard.ui', self)
        self.setWindowIcon(QIcon('iot_64.png'))
        # 화면 정중앙 위치
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft()) # End of screen central position
        # self.btnTempAlarm.setEnabled(False)  # 버튼 비활성화
        # self.btnTempStop.setEnabled(True)

        # 위젯 시그널 정의
        self.btnTempAlarm.clicked.connect(self.btnTempAlarmClicked)
        self.btnTempStop.clicked.connect(self.btnTempStopClicked)
        self.btnHumidAlarm.clicked.connect(self.btnHumidAlarmClicked)
        self.btnHumidStop.clicked.connect(self.btnHumidStopClicked)
        self.show()

    def btnHumidStopClicked(self):
        QMessageBox.information(self, '정상', '제습기 중지')
        self.client = mqtt.Client(client_id='Controller')
        self.client.connect(broker_url, 1883)
        curr = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        origin_data = {'DEV_ID' : 'CONTROL', 'CURR_DT' : curr,
                        'TYPE': 'DEHUMD', 'STAT': 'OFF'}
        pub_data = json.dumps(origin_data)
        self.client.publish(topic='ems/rasp/control/',
                                payload=pub_data)
        print('Dehumidifier OFF Published')
        self.insertAlarmData('CONTROL', curr, 'DEHUMD', 'OFF')


    def btnHumidAlarmClicked(self):
        QMessageBox.information(self, '알람', '이상습도로 제습기 가동')
        self.client = mqtt.Client(client_id='Controller')
        self.client.connect(broker_url, 1883)
        curr = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        origin_data = {'DEV_ID' : 'CONTROL', 'CURR_DT' : curr,
                        'TYPE': 'DEHUMD', 'STAT': 'ON'}
        pub_data = json.dumps(origin_data)
        self.client.publish(topic='ems/rasp/control/',
                                payload=pub_data)
        print('Dehumidifier ON Published')
        self.insertAlarmData('CONTROL', curr, 'DEHUMD', 'ON')

    def btnTempStopClicked(self):
        QMessageBox.information(self, '정상', '에어컨 중지')
        self.client = mqtt.Client(client_id='Controller')
        self.client.connect(broker_url, 1883)
        curr = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        origin_data = {'DEV_ID' : 'CONTROL', 'CURR_DT' : curr,
                        'TYPE': 'AIRCON', 'STAT': 'OFF'}
        pub_data = json.dumps(origin_data)
        self.client.publish(topic='ems/rasp/control/',
                                payload=pub_data)
        print('AIRCON OFF Published')
        self.insertAlarmData('CONTROL', curr, 'AIRCON', 'OFF')


    def btnTempAlarmClicked(self):
        QMessageBox.information(self, '알람', '이상온도로 에어컨 가동')
        self.client = mqtt.Client(client_id='Controller')
        self.client.connect(broker_url, 1883)
        curr = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        origin_data = {'DEV_ID' : 'CONTROL', 'CURR_DT' : curr,
                        'TYPE': 'AIRCON', 'STAT': 'ON'}
        pub_data = json.dumps(origin_data)
        self.client.publish(topic='ems/rasp/control/',
                                payload=pub_data)
        print('AIRCON ON Published')
        self.insertAlarmData('CONTROL', curr, 'AIRCON', 'ON')


    # 이상상태, 정상상태 DB 저장함수
    def insertAlarmData(self, dev_id, curr_dt, types, stat):  # type 사용X types로 변경
        self.conn = pymysql.connect(host='127.0.0.1',
                                    user='bms',
                                    password='1234',
                                    db='bms',
                                    charset='euckr')
        query = '''INSERT INTO ems_alarm
                            (dev_id, curr_dt, type, stat)
                    VALUES
                            (%s, %s, %s, %s) '''

        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(query, (dev_id, curr_dt, types, stat))
                self.conn.commit()
                print('Alarm Inserted!')

    # 종료 메세지박스
    def closeEvent(self,signal):
        ans = QMessageBox.question(self, '종료', '종료하시겠습니까?',
                                   QMessageBox.Yes | QMessageBox.No,
                                   QMessageBox.No)
        if ans == QMessageBox.Yes:
            self.conn.close() # DB접속 끊기!!!!! 연결후에끊기 반드시
            signal.accept()
        else:
            signal.ignore()


    def showTime(self):
        today = QDateTime.currentDateTime()
        currDate = today.date()
        currTime = today.time()
        currDay = today.toString('dddd')
        
        self.lblDate.setText(currDate.toString("yyyy-MM-dd"))
        self.lblDay.setText(currDay)
        self.lblTime.setText(currTime.toString('HH:mm'))
        if today.time().hour() > 5 and today.time().hour() < 12:
            self.lblGreeting.setText('Good Morning!')
        elif today.time().hour() >= 12 and today.time().hour() < 18:
            self.lblGreeting.setText('Good Afternoon!')
        elif today.time().hour() >= 18:
            self.lblGreeting.setText('Good Evening!')


    def showWeather(self):
        url = 'https://api.openweathermap.org/data/2.5/weather' \
              '?q=seoul&appid=0a9f6aeb854114111d15d53b5a76469d' \
              '&lang=kr&units=metric'
        result = requests.get(url)
        result = json.loads(result.text)
        weather = result['weather'][0]['main'].lower()
        print(weather)
        self.weatherFrame.setStyleSheet(
            (
            f'background-image: url(:/{weather});'
            'background-repeat: none;'
            'border: none;'
            )
        )

if __name__=='__main__':
    app = QApplication(sys.argv)
    win = MyApp()
    app.exec()
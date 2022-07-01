## 동시에 두가지태스크 -> published, subscribed 동시에 출력
from threading import Thread, Timer
import time
import paho.mqtt.client as mqtt
import json
import datetime as dt

import adafruit_dht as dht
import board

SENSOR = dht.DHT11(board.D4)

class publisher(Thread):   #QThread와 비슷
    def __init__(self):
        Thread.__init__(self)
        self.host = '127.0.0.1'
        self.port = 1883
        self.client = mqtt.Client(client_id='EMS101')
        print('publisher 스레드 시작')
    
    def run(self):
        self.client.connect(self.host, self.port)
        self.publish_data_auto()
    
    def publish_data_auto(self):
        try:
            t = SENSOR.temperature
            h = SENSOR.humidity
            curr = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            origin_data = {'DEV_ID' : 'DASHBOARD', 'CURR_DT' : curr,
                            'TEMP': t, 'HUMID': h}
            pub_data = json.dumps(origin_data)
            self.client.publish(topic='ems/rasp/data/',
                                    payload=pub_data)
            print(f'{curr} -> MQTT Published')
        except RuntimeError as e:
            print(f'ERROR > {e.args[0]}')

        Timer(2.0, self.publish_data_auto).start()


class subscriber(Thread):   
    def __init__(self):
        Thread.__init__(self)
        self.host = '127.0.0.1' # 추후 변경
        self.port = 1883
        print('publisher 스레드 시작')
        self.client = mqtt.Client(client_id='EMS911')
    
    def onConnect(self, mqttc, obj, flags, rc):
        print(f'sub:connected with result code > {rc}')

    def onMessage(self, mqttc, ogj, msg):
        rcv_msg = str(msg.payload.decode('utf-8'))
        print(f'{msg.topic} / {rcv_msg}')
        time.sleep(1.0)

    def run(self):
        self.client.on_connect = self.onConnect
        self.client.on_message = self.onMessage
        self.client.connect(self.host, self.port)
        self.client.subscribe(topic='ems/rasp/control/')
        self.client.loop_forever()

if __name__ == '__main__':
    thPub = publisher()
    thSub = subscriber()
    thPub.start()
    thSub.start()
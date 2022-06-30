# MQTT Publisher 2
import threading
import datetime as dt
import paho.mqtt.client as mqtt
import json

import adafruit_dht as dht
import board

client2 = None
count = 0
SENSOR = dht.DHT11(board.D4)

def publish_sensor_data():
    try:
        curr = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        t = SENSOR.temperature
        h = SENSOR.humidity
        origin_data = { 'DEV_ID' : 'EMS06', 'CURR_DT' : curr,
                        'TEMP' : t, 'HUMID' : h }
        pub_data = json.dumps(origin_data)
        client2.publish(topic='ems/rasp/data/',
                        payload=pub_data)
        print(f'{curr} -> MQTT Published')  
    except RuntimeError as e:
        print(f'ERROR > {e.args[0]}')
    
    threading.Timer(2.0, publish_sensor_data).start()

if __name__ == '__main__':
    broker_url = '192.168.0.15'  # 데이터 보낼 컴 주소
    client2 = mqtt.Client(client_id='EMS06')
    client2.connect(host=broker_url,
                    port=1883)
    
    publish_sensor_data()
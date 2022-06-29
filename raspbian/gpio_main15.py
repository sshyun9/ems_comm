# new adafruit package
# sudo pip install adafruit-circuitpython-dht
# sudo apt install libgpiod2
import adafruit_dht as dht
import board
import time

SENSOR = dht.DHT11(board.D4) # 보드 GPIO 4번 , 센서 초기화

while True:
    try:
        t = SENSOR.temperature
        h = SENSOR.humidity
        print(f'TEMP > {t:.1f}`c  / HUMID > {h:.0f}%')
    
    except RuntimeError as e:
        print(f'ERROR > {e.args[0]}')
        time.sleep(3.0)

    except Exception as e:
        SENSOR.exit()
        raise e
    
    time.sleep(3.0)

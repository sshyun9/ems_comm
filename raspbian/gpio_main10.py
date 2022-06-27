# Distance Sensor Test
from turtle import distance
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

TRIG = 16
ECHO = 18

GPIO.setup(TRIG, GPIO.OUT) # trig 초음파 발생
GPIO.setup(ECHO, GPIO.IN)  # echo 초음파 반사 읽음

GPIO.output(TRIG, GPIO.LOW)
print('Init Ultrasonic')
time.sleep(2.0)

try: 
    while True:
        GPIO.output(TRIG, GPIO.HIGH)
        time.sleep(0.00001) # 10us delay
        GPIO.output(TRIG, GPIO.LOW)

        while GPIO.input(ECHO) == 0:
            start = time.time()

        while GPIO.input(ECHO) == 1:
            stop = time.time()

        check_time = stop - start
        distance = check_time * 34300/2
        print(f'Distance = {distance:.1f} cm')
        time.sleep(0.4)

except KeyboardInterrupt:
    GPIO.cleanup()
# RGB LED ON/OFF
import RPi.GPIO as GPIO
import time

RED = 11 #라즈베리파이 11번
GREEN = 12
BLUE = 13

GPIO.setmode(GPIO.BOARD)  # GPIO.BCM
GPIO.setup(RED, GPIO.OUT)  # 11핀 출력셋팅
GPIO.setup(GREEN, GPIO.OUT)  # 12핀 출력셋팅
GPIO.setup(BLUE, GPIO.OUT)  # 13핀 출력셋팅

# GPIO.output(RED, GPIO.LOW)  #HIGH LIGHT ON, LOW LIGHT OFF

try:
    while True:
        GPIO.output(RED, GPIO.HIGH) # RED on, 나머지 off
        GPIO.output(GREEN, GPIO.LOW) 
        GPIO.output(BLUE, GPIO.LOW)
        time.sleep(0.5)

        GPIO.output(RED, GPIO.LOW) # GREEN on, 나머지 off
        GPIO.output(GREEN, GPIO.HIGH) 
        GPIO.output(BLUE, GPIO.LOW)
        time.sleep(0.5)

        GPIO.output(RED, GPIO.LOW) # BLUE on, 나머지 off
        GPIO.output(GREEN, GPIO.LOW) 
        GPIO.output(BLUE, GPIO.HIGH)
        time.sleep(0.5)

        GPIO.output(RED, GPIO.HIGH) # ALL HIGH
        GPIO.output(GREEN, GPIO.HIGH) 
        GPIO.output(BLUE, GPIO.HIGH)
        time.sleep(0.5)

except KeyboardInterrupt:   # 콘솔 ctrl+C -> 프로그램 종료
    GPIO.output(RED, GPIO.LOW)
    GPIO.output(GREEN, GPIO.LOW)
    GPIO.output(BLUE, GPIO.LOW)


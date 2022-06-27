## PUSHBUTTON RGB LED Control
import RPi.GPIO as GPIO
import time

BUTTON = 3
RED = 11 #라즈베리파이 11번
GREEN = 12
BLUE = 13

GPIO.setmode(GPIO.BOARD)
GPIO.setup(BUTTON, GPIO.IN)
GPIO.setup(RED, GPIO.OUT)  # 11핀 출력셋팅
GPIO.setup(GREEN, GPIO.OUT)  # 12핀 출력셋팅
GPIO.setup(BLUE, GPIO.OUT)  # 13핀 출력셋팅

is_click = False  # 변수 초기화

def button_push(val):
    global is_click
    if is_click == True:
        GPIO.output(RED, GPIO.HIGH) # ALL HIGH
        GPIO.output(GREEN, GPIO.HIGH) 
        GPIO.output(BLUE, GPIO.HIGH)
    else:
        GPIO.output(RED, GPIO.LOW) 
        GPIO.output(GREEN, GPIO.LOW) 
        GPIO.output(BLUE, GPIO.LOW)

    is_click = not is_click

while True:
    GPIO.wait_for_edge(BUTTON, GPIO.RISING, bouncetime=100)
    time.sleep(0.1)

    button_push(GPIO.input(BUTTON)) # 버튼 누를때마다 불 들어옴
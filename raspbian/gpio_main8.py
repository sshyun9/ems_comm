## PUSHBUTTON RGB LED Control 2
import RPi.GPIO as GPIO
import time

BUTTON = 3
SERVO = 12

GPIO.setmode(GPIO.BOARD)  # 
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SERVO, GPIO.OUT)

count = 0
pwm = GPIO.PWM(SERVO, 50) # 50Hz
pwm.start(3.0)  # 0.6ms

def button_push(channel) :
    global count
    if count % 3 == 1:  #90
        pwm.ChangeDutyCycle(7.5)
    elif count % 3 == 2: # 180
        pwm.ChangeDutyCycle(12.5)
    else :
        pwm.ChangeDutyCycle(3.0)
    count += 1
    

GPIO.add_event_detect(BUTTON, GPIO.RISING, callback=button_push,
                      bouncetime=100)

try:
    while True: time.sleep(0.1)

except KeyboardInterrupt:
    pwm.ChangeDutyCycle(0.0)
    pwm.stop()
    GPIO.Cleanup()
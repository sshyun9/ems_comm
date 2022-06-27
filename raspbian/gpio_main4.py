## PUSHBUTTON RGB LED Control 2
import RPi.GPIO as GPIO
import time

BUTTON = 3
RED = 11
GREEN = 12
BLUE = 13

GPIO.setmode(GPIO.BOARD)
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(RED, GPIO.OUT)  
GPIO.setup(GREEN, GPIO.OUT)  
GPIO.setup(BLUE, GPIO.OUT)   

is_click = False
count = 0

def button_push(channel) :
    global count
    if count % 5 == 1:  #RED
        GPIO.output(RED, GPIO.HIGH) 
        GPIO.output(GREEN, GPIO.LOW) 
        GPIO.output(BLUE, GPIO.LOW)
    elif count % 5 == 2: # GREEN
        GPIO.output(RED, GPIO.LOW) 
        GPIO.output(GREEN, GPIO.HIGH) 
        GPIO.output(BLUE, GPIO.LOW)
    elif count % 5 == 3: # BLUE
        GPIO.output(RED, GPIO.LOW) 
        GPIO.output(GREEN, GPIO.LOW) 
        GPIO.output(BLUE, GPIO.HIGH)
    elif count % 5 == 4: # WHITE
        GPIO.output(RED, GPIO.HIGH) 
        GPIO.output(GREEN, GPIO.HIGH) 
        GPIO.output(BLUE, GPIO.HIGH)
    else :
        GPIO.output(RED, GPIO.LOW) 
        GPIO.output(GREEN, GPIO.LOW) 
        GPIO.output(BLUE, GPIO.LOW)
    count += 1
    
    is_click = not is_click

GPIO.add_event_detect(BUTTON, GPIO.RISING, callback=button_push,
                      bouncetime=100)

try:
    while True: time.sleep(0.1)

except KeyboardInterrupt:
    GPIO.output(RED, GPIO.LOW) 
    GPIO.output(GREEN, GPIO.LOW) 
    GPIO.output(BLUE, GPIO.LOW)
    GPIO.cleanup()

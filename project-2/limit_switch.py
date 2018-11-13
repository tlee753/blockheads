import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

Pin_number = 26

GPIO.setup(Pin_number, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

while True:
    input_state = GPIO.input(Pin_number)
    if input_state == True:
        print('Button Pressed')
        time.sleep(0.2)

import RPi.GPIO as GPIO
import time

Limit_switch_channel = 26;
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(Limit_switch_channel, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin 10 to be an input pin and set initial value to be pulled low (off)

while True: # Run forever
    input_state = GPIO.input(Limit_switch_channel)
    if input_state == False:
        print('Button Pressed')
        time.sleep(0.2)

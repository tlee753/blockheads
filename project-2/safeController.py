

from enum import Enum
import RPi.GPIO as GPIO
import time 
import wiringpi
import bluetooth
import sys
import Adafruit_MPR121.MPR121 as MPR121

class State(Enum):
	LOCKED = 0
	UNLOCKED = 1

#Global variables
global state
global correct_combination
global cap
global correct_numbers_entered
global delay_period

#Pinout
global Limit_switch_pin
global redPin
global greenPin
global bluePin



#Initialize the safe in locked positoin
def initialize():
	
	#Pinout
	Limit_switch_pin = 26
	redPin   = 11
	greenPin = 13
	bluePin  = 15

	#initialize state
	state = State.LOCKED
	
	#-----Set up keypad-----#
	cap = MPR121.MPR121()
	correct_combination = '1234'
	correct_numbers_entered = 0;
	
	if not cap.begin():
    		print('Error initializing MPR121.  Check your wiring!')
    		sys.exit(1)
	
	#-----Set up servo-----#
	# use 'GPIO naming'
	wiringpi.wiringPiSetupGpio()
 
	# set #18 to be a PWM output
	wiringpi.pinMode(18, wiringpi.GPIO.PWM_OUTPUT)
 
	# set the PWM mode to milliseconds stype
	wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)
 
	# divide down clock
	wiringpi.pwmSetClock(192)
	wiringpi.pwmSetRange(2000)
 
	delay_period = 0.01
	
	#-----Set up limit switch-----#
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(Limit_switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	
	#-----Set up LED-----#
	GPIO.setmode(GPIO.BOARD)
  	GPIO.setup(redPin, GPIO.OUT)
	GPIO.setup(greenPin, GPIO.OUT)
	GPIO.setup(bluePin, GPIO.OUT)

def blink(pin):
  	GPIO.output(pin, GPIO.HIGH)
  
def turnOff(pin):
	GPIO.output(pin, GPIO.LOW)
  
def redOn():
	blink(redPin)
  
def greenOn():
  	blink(greenPin)
  
def blueOn():
  	blink(bluePin)
  
def redOff():
	turnOff(redPin)

def greenOff():
	turnOff(greenPin)

def blueOff():
	turnOff(bluePin)
	
def wait_for_correct_combo():
	#If correct combination is entered, unlock the safe
	last_touched = cap.touched()
	correct_combo_not_entered = True
	while correct_combo_not_entered:
    		current_touched = cap.touched()
   	 	# Check each pin's last and current state to see if it was pressed or released.
    		for i in range(12):
			# Each pin is represented by a bit in the touched value.  A value of 1
			# means the pin is being touched, and 0 means it is not being touched.
			pin_bit = 1 << i
			# First check if transitioned from not touched to touched.
			if current_touched & pin_bit and not last_touched & pin_bit:
				#print('{0} touched!'.format(i))
				if i == int(correct_combination[correct_numbers_entered]):
					greenOn()
					time.sleep(0.1)
					greenOff()
					correct_numbers_entered = correct_numbers_entered + 1;
					if correct_numbers_entered == 4:
						correct_combo_not_entered = False;
						correct_numbers_entered = 0;
						#unlock safe
			else:
				redOn()
				time.sleep(0.1)
				redOff()
				correct_numbers_entered = 0;
				# Next check if transitioned from touched to not touched.
				#if not current_touched & pin_bit and last_touched & pin_bit:
				#print('{0} released!'.format(i))
				# Update last state and wait a short period before repeating.
			last_touched = current_touched
			time.sleep(0.1)

def wait_for_safe_close():
	#check if limit switch detects closure
	safe_not_closed = True;
	while safe_not_closed:
    		input_state = GPIO.input(Pin_number)
    		if input_state == False:
			safe_not_closed = False;
        	time.sleep(0.2)

def phone_in_range_callback(channel):
	#check if user's phone is in bluetooth range so s/he can open the safe
	state = State.UNLOCKED



def open_safe():
	#turn the motor/solenoid to unlock the safe
	for pulse in range(120, 50, -1):
                wiringpi.pwmWrite(18, pulse)
                time.sleep(delay_period)

def close_safe():
	#turn the motor/solenoid to lock the safe
	for pulse in range(50, 120, 1):
                wiringpi.pwmWrite(18, pulse)
                time.sleep(delay_period)
		
def main():
	#Initialize into locked state
	initialize()

	while True:
		print('Waiting for correct combo')
		wait_for_correct_combo()
		print('Opening safe')
		state = State.UNLOCKED
		open_safe()
		print('Waiting for safe to close')
		wait_for_safe_close()
		print('Safe closed')
		state = State.LOCKED
		close_safe()
		

main()



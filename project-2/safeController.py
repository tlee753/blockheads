

from enum import Enum
from gpiozero import LED
import time 
import wiringpi
import bluetooth

class State(Enum):
	LOCKED = 0
	UNLOCKED = 1

#Global variables
global state
global correct_combination

redLED = LED(17)
redLED.off()

def main():
	#Initialize into locked state
	initialize()

	while true:
#Wait for interrupt to lock

#Wait for unlock interrupt


#Initialize the safe in locked positoin
def initialize():

	#initialize state
	state = State.LOCKED
	
	#-----Set up keypad-----#
	correct_combination = 1234
	
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

#sensors
def combination_entered_callback(channel):
	#If correct combination is entered, unlock the safe
	if combo == correct_combination:
		state = State.UNLOCKED

def safe_closed_callback(channel):
	#check if limit switch detects closure
	state = State.LOCKED

def phone_in_range_callback(channel):
	#check if user's phone is in bluetooth range so s/he can open the safe
	state = State.UNLOCKED

#actuators
def change_led_color(color):
	#change the color of the LED
	greenLED = LED(17)
	redLED = LED(18)
	if color == "red"
		greenLED.off()
		redLED.on()
	else if color == "green"
		redLED.off()
		greenLED.on()


def open_safe():
	#turn the motor/solenoid to unlock the safe
	for pulse in range(50, 250, 1):
                wiringpi.pwmWrite(18, pulse)

def close_safe():
	#turn the motor/solenoid to lock the safe
	for pulse in range(250, 50, -1):
                wiringpi.pwmWrite(18, pulse)

#state transitions
def lock():
	change_led_color("red")
	close_safe()

def unlock():
	change_led_color("green")
	open_safe()


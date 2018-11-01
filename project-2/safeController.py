

from enum import Enum
from gpiozero import LED

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
	state = State.LOCKED
	correct_combination = 1234

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

def close_safe():
	#turn the motor/solenoid to lock the safe

#state transitions
def lock():
	change_led_color("red")
	close_safe()

def unlock():
	change_led_color("green")
	open_safe()


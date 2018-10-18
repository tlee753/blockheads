

from enum import Enum

class State(Enum):
	LOCKED = 0
	UNLOCKED = 1

#Global variables
global state
global correct_combination



def main():
	



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

def phone_in_range_callback(channel):
	#returns true if the user's phone is in bluetooth range so s/he can open the safe

#actuators
def change_led_color(color):
	#change the color of the LED

def open_safe():
	#turn the motor/solenoid to unlock the safe

def close_safe():
	#turn the motor/solenoid to lock the safe
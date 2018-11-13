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

class safeController:

	#Initialize the safe in locked positoin
	def initialize(self):

		#Pinout
		self.Limit_switch_pin = 26
		self.redPin   = 11
		self.greenPin = 13
		self.bluePin  = 15
		self.servoPin = 18

		#initialize state
		self.state = State.LOCKED

		#-----Set up keypad-----#
		self.cap = MPR121.MPR121()
		self.correct_combination = '1234'
		self.correct_numbers_entered = 0;

		if not self.cap.begin():
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

		self.delay_period = 0.01

		#-----Set up limit switch-----#
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(self.Limit_switch_pin, GPIO.IN)

		#-----Set up LED-----#
		GPIO.setup(self.redPin, GPIO.OUT)
		GPIO.setup(self.greenPin, GPIO.OUT)
		GPIO.setup(self.bluePin, GPIO.OUT)

	def blink(self, pin):
		GPIO.output(pin, GPIO.HIGH)

	def turnOff(self, pin):
		GPIO.output(pin, GPIO.LOW)

	def redOn(self):
		blink(self.redPin)

	def greenOn(self):
		blink(self.greenPin)

	def blueOn(self):
		blink(self.bluePin)

	def redOff(self):
		turnOff(self.redPin)

	def greenOff(self):
		turnOff(self.greenPin)

	def blueOff(self):
		turnOff(self.bluePin)

	def wait_for_correct_combo(self):
		#If correct combination is entered, unlock the safe
		last_touched = self.cap.touched()
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
						self.greenOn()
						time.sleep(0.1)
						self.greenOff()
						correct_numbers_entered = correct_numbers_entered + 1;
						if correct_numbers_entered == 4:
							correct_combo_not_entered = False;
							correct_numbers_entered = 0;
							#unlock safe
				else:
					self.redOn()
					time.sleep(0.1)
					self.redOff()
					correct_numbers_entered = 0;
					# Next check if transitioned from touched to not touched.
					#if not current_touched & pin_bit and last_touched & pin_bit:
					#print('{0} released!'.format(i))
					# Update last state and wait a short period before repeating.
				last_touched = current_touched
				time.sleep(0.1)

	def wait_for_safe_close(self):
		#check if limit switch detects closure
		safe_not_closed = True;
		while safe_not_closed:
			input_state = GPIO.input(self.servoPin)
			if input_state == False:
				safe_not_closed = False;
			time.sleep(0.2)

	def phone_in_range_callback(self):
		#check if user's phone is in bluetooth range so s/he can open the safe
		state = State.UNLOCKED

	def open_safe(self):
		#turn the motor/solenoid to unlock the safe
		for pulse in range(120, 50, -1):
			wiringpi.pwmWrite(18, pulse)
			time.sleep(self.delay_period)

	def close_safe(self):
		#turn the motor/solenoid to lock the safe
		for pulse in range(50, 120, 1):
			wiringpi.pwmWrite(18, pulse)
			time.sleep(self.delay_period)
		
	def main(self):
		#Initialize into locked state
		self.initialize()

		while True:
			print('Waiting for correct combo')
			self.wait_for_correct_combo()
			print('Opening safe')
			self.state = State.UNLOCKED
			self.open_safe()
			print('Waiting for safe to close')
			self.wait_for_safe_close()
			print('Safe closed')
			self.state = State.LOCKED
			self.close_safe()
		

sc = safeController()
sc.main()



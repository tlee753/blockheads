import sys, time

import RPi.GPIO as GPIO

redPin   = 11
greenPin = 13
bluePin  = 15

def blink(pin):
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(pin, GPIO.OUT)
  GPIO.output(pin, GPIO.HIGH)
  
def turnOff(pin):
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(pin, GPIO.OUT)
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


while True:
  redOn()
  time.sleep(1)
  redOff()
  greenOn()
  time.sleep(1)
  greenOff()
  blueOn()
  time.sleep(1)
  blueOff()
  

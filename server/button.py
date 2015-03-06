import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)

#initialise a previous input variable to 0 (assume button not pressed last)
prev_input = 0
buttonpin = 33
def buttonpressed(pin):
	GPIO.setup(pin, GPIO.OUT)
	GPIO.output(pin, (not GPIO.input(pin)))

GPIO.setup(buttonpin ,GPIO.IN)
while True:
	input = GPIO.input(buttonpin)
	if ((not prev_input) and input):
		buttonpressed(40)
		print buttonpin
	
	#update previous input
	prev_input = input
	time.sleep(0.05)
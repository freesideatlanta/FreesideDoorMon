
#Setup Thread To Read Cards

import wiringpi
import Queue


readQueue = Queue.Queue()

SENSE_A = 17
SENSE_B = 27


def gpio_callback_a():
	readQueue.put(0)
	while wiringpi.digitalRead(SENSE_A) == 0:
		pass

def gpio_callback_b():
	readQueue.put(1)
	while wiringpi.digitalRead(SENSE_B) == 0:
		pass

wiringpi.wiringPiSetupGpio()
wiringpi.pinMode(SENSE_A,wiringpi.GPIO.INPUT)
wiringpi.pinMode(SENSE_B,wiringpi.GPIO.INPUT)

wiringpi.pullUpDnControl(SENSE_A, wiringpi.GPIO.PUD_DOWN)
wiringpi.pullUpDnControl(SENSE_B,wiringpi.GPIO.PUD_DOWN)

wiringpi.wiringPiISR(SENSE_A,wiringpi.GPIO.INT_EDGE_FALLING, gpio_callback_a)
wiringpi.wiringPiISR(SENSE_B,wiringpi.GPIO.INT_EDGE_FALLING, gpio_callback_b)

while True:
	wiringpi.delay(10)
	if not readQueue.empty():
		wiringpi.delay(300)	#Wait for all data to arrive
		readCard = "" 
		while not readQueue.empty():
			readCard += str(readQueue.get())

		if len(readCard) == 26:
			print str(int(readCard[1:9],2)) + str(int(readCard[9:25],2))

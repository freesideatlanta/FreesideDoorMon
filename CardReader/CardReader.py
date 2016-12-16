
#Setup Thread To Read Cards

import wiringpi
import Queue

import socket

SENSE_A = 17
SENSE_B = 27

firstA = True
firstB = True

readQueue = Queue.Queue()

#Weigand ReaderInterrupts
def gpio_callback_a():
	global firstA
	if firstA:
		firstA = False
	else:
		readQueue.put(0)

def gpio_callback_b():
	global firstB
	if firstB:
		firstB = False
	else:
		readQueue.put(1)

readQueue = Queue.Queue()

#Setup Weigand IO
wiringpi.wiringPiSetupGpio()
wiringpi.pinMode(SENSE_A,wiringpi.GPIO.INPUT)
wiringpi.pinMode(SENSE_B,wiringpi.GPIO.INPUT)

wiringpi.pullUpDnControl(SENSE_A,wiringpi.GPIO.PUD_UP)
wiringpi.pullUpDnControl(SENSE_B,wiringpi.GPIO.PUD_UP)

wiringpi.wiringPiISR(SENSE_A,wiringpi.GPIO.INT_EDGE_FALLING, gpio_callback_a)
wiringpi.wiringPiISR(SENSE_B,wiringpi.GPIO.INT_EDGE_FALLING, gpio_callback_b)

#Setup broadcast socket
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

#Wait for cardto be read
while True:
	wiringpi.delay(10)
	if not readQueue.empty():
		wiringpi.delay(300)	#Wait for all data to arrive. Note* There's) got to be abetter way todetect finished. Also first read always reads 28 bits. No Idea why.

		readCard = "" 
		while not readQueue.empty():
			readCard +=str(readQueue.get())

		if len(readCard) == 26:
			fac = str(int(readCard[1:9],2))
			code = str(int(readCard[9:25],2))
			card = fac + code.zfill(5)
			sock.sendto('{"action" : "cardRead", "location" : "frontDoor", "id" : "'  + card + '" }'  , ('255.255.255.255', 50505))
			print card


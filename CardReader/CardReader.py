
#Setup Thread To Read Cards

import pigpio
import wiegand
import time

import Queue

import socket


from subprocess import call
call(["sudo", "pigpiod"])

SENSE_A = 17
SENSE_B = 27

readQueue = Queue.Queue()

#Weigand ReaderInterrupts
def read_callback(bits, code):
	if bits== 26:
		fac = (code >> 17) & 0xFF
		id = (code >> 1) & 0xFFFF
	readQueue.put(str(fac)+str(id).zfill(5))


#Setup Weigand IO
pi = pigpio.pi()
dec = wiegand.decoder(pi, SENSE_A, SENSE_B, read_callback)



#Setup broadcast socket
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)


#Wait for cardto be read
while True:

	if not readQueue.empty():
		id = readQueue.get();
		print id		
		sock.sendto('{"action" : "cardRead", "location" : "frontDoor", "id" : "'  + id + '" }'  , ('255.255.255.255', 50505))

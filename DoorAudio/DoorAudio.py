import socket
import json
import os.path
import pygame

pygame.mixer.init()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.bind(('<broadcast>', 50505))

while True:
	msg = s.recvfrom(1024)	
	jmsg = json.loads(msg[0])

	if jmsg['location'] == 'frontDoor':
		if jmsg['action'] == 'cardRead':
			#check audio fileexists
			filename = "/usr/local/bim/FreesideDoorMon/DoorAudio/wav/" + jmsg + ".wav"
			if os.path.isfile(filename):
				pygame.mixer.load(filename)
				pygame.mixer.play()
				while pygame.mixer.music.get_busy() == True:
					continue	

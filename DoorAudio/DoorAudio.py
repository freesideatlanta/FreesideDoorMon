import socket
import json
import os.path
import pygame

pygame.init()
pygame.mixer.init()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.bind(('<broadcast>', 50505))

while True:
	msg = s.recvfrom(1024)	
	jmsg = json.loads(msg[0])
	if jmsg['location'] == 'frontDoor':
		if jmsg['action'] == 'cardRead':
			#check audio fileexists
			filename = "/usr/local/bin/FreesideDoorMon/DoorAudio/wav/" + jmsg['id'] + ".wav"			
			if os.path.isfile(filename):
				sound = pygame.mixer.Sound(filename)
				channel = sound.play()
				while channel.get_busy():
					pygame.time.delay(100)

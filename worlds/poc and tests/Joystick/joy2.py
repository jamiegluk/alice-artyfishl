import socket
import pygame
import pickle
import sys
pygame.init()
if pygame.joystick.get_count()==1:
    joystick=pygame.joystick.Joystick(0)
    print('Found 1 joystick: %s'%joystick.get_name())
    joystick.init()
elif pygame.joystick.get_count()>1:
    print('Found %d joysticks:'%pygame.joystick.get_count())
    for index in range(pygame.joystick.get_count()):
        joy=pygame.joystick.Joystick(index)
        print('%d: %s'%(joy.get_id(),joy.get_name()))
    done=False
    while not done:
        try:
            print('Select joystick number:')
            index=int(raw_input())
            if 0<=index<pygame.joystick.get_count():
                joystick=pygame.joystick.Joystick(index)
                print('Selected %d: %s'%(index,joystick.get_name()))
                joystick.init()
                done=True
            else:
                print('Invalid joystick ID')
        except IOError:
            print('Please enter one of the above IDs')
else:
    print('No joysticks found. Press ENTER to exit.')
    raw_input()
    sys.exit(0)
print('Serving joystick on localhost:2727')
raw_input()
mySocket = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
mySocket.bind ( ( '', 2727 ) )
mySocket.listen ( 1 )
while True:
	channel, details = mySocket.accept()
	try:
		while True:
			channel.recv(100)
			pygame.event.pump()
			channel.send(pickle.dumps((joystick.get_axis(0),joystick.get_axis(1))))
	except:
		channel.close()

import socket
import pygame
import pickle
import sys
from threading import Thread

global mySocket

def sendinfo():
    class sendstuff(Thread):
        def run(self):
            while(True):
                    channel, details = mySocket.accept()
                    try:
                            while(True):
                                    channel.recv(100)
                                    pygame.event.pump()
                                    buttons = []
                                    for i in range(0,19):
                                        buttons.append(Joystick.get_button(i))
                                    channel.send(pickle.dumps((`joystick.get_axis(0)`, `joystick.get_axis(1)`, `joystick.get_axis(2)`, `joystick.get_axis(3)`, ''.join(buttons))))
                    except:
                            channel.close()
    sendstuff().start()

pygame.init()
if(pygame.joystick.get_count() == 1):
    joystick=pygame.joystick.Joystick(0)
    print("Found 1 joystick: %s"%joystick.get_name())
    joystick.init()
elif(pygame.joystick.get_count() > 1):
    print("Found %d joysticks:"%pygame.joystick.get_count())
    for index in range(pygame.joystick.get_count()):
        joy=pygame.joystick.Joystick(index)
        print("%d: %s"%(joy.get_id(),joy.get_name()))
    done=False
    while(not(done)):
        try:
            print("Select joystick number:")
            index=int(raw_input())
            if(0 <= index<pygame.joystick.get_count()):
                joystick=pygame.joystick.Joystick(index)
                print("Selected %d: %s"%(index,joystick.get_name()))
                joy = joystick.init()
                done=True
            else:
                print("Invalid joystick ID")
        except(IOError):
            print("Please enter one of the above IDs")
else:
    print("No joysticks found. Press ENTER to exit.")
    raw_input()
    sys.exit(0)
joystick = pygame.joystick.Joystick(0)
print("Number of axes: " + `joystick.get_numaxes()`)
print("Number of buttons: " + `joystick.get_numbuttons()`)

global mySocket
mySocket = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
mySocket.bind(( '', 2729 ))
mySocket.listen( 1 )
print('Serving joystick on localhost:2729')
sendinfo()
print
raw_input("Press enter to quit...")
mySocket.close()
sys.exit(0)



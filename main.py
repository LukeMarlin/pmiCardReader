#!/usr/bin/python3.2

import RPIO
import threading 
print("Starting RFID reader...")

tag = "" #The buffer used to store the RFID Tag

#The pins used to receive 0s and 1s
GPIO_0 = 23
GPIO_1 = 24

BIT_TRANSMISSION_TIME = 0.00205 #From wiegand specification
FRAMESIZE = 26 #Supposed size of received frame
FRAMETIME = FRAMESIZE * BIT_TRANSMISSION_TIME #Theoric time necessary to transfer a frame
ALLOWANCE = 10 #Auhtorized allowance for the transmission time
TIMEOUT = FRAMETIME*(1+ALLOWANCE/100) #Real time allowed for the transmission

#Method to convert the RFID binary value into a readable integer
def binaryToInt(binary_string):
	binary_string = binary_string[1:-1]
	result = int(binary_string, 2)
	return result

#Method trigger after timer tick that prints out the tag
def processTag():
	global tag
	print("Frame of length (" + str(len(tag)) + "): " + tag + " (" + str(binaryToInt(tag)) + ")" )
	tag = ""
	
def addBitToTag(gpio_id, val):
	global tag
	global t
	
	#Beginning of a new frame, we start the timer
	if tag == "":
		t = threading.Timer(TIMEOUT, processTag)
		t.start()
	#We check wether we received a 0 or a 1
	if gpio_id == GPIO_0:
		tag += "0"
	elif gpio_id == GPIO_1:
		tag += "1"		

#We set the pins to Input
RPIO.setup(GPIO_0, RPIO.IN)
RPIO.setup(GPIO_1, RPIO.IN)

#We register our callback on the pins events
RPIO.add_interrupt_callback(GPIO_0, addBitToTag, edge='falling', pull_up_down=RPIO.PUD_UP)
RPIO.add_interrupt_callback(GPIO_1, addBitToTag, edge='falling', pull_up_down=RPIO.PUD_UP)

RPIO.wait_for_interrupts()

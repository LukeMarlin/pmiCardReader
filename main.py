#!/usr/bin/python3.2

import RPIO
import threading 
print("Hellolivier !")

buffer = ""
GPIO_0 = 23
GPIO_1 = 24
lineCount = 0
FRAME_SIZE = 26
TIMEOUT = 0.06

def binaryToInt(binary_string):
	binary_string = binary_string[1:-1]
	result = int(binary_string, 2)
	return result

def process_buffer():
	global buffer
	print("Frame of length (" + str(len(buffer)) + "): " + buffer + " (" + str(binaryToInt(buffer)) + ")" )
	buffer = ""
	
def print_value(gpio_id, val):
	global buffer
	global lineCount
	global t

	if buffer == "":
		t = threading.Timer(TIMEOUT, process_buffer)
		t.start()
	if gpio_id == GPIO_0:
		buffer += "0"
	elif gpio_id == GPIO_1:
		buffer += "1"		

RPIO.setup(GPIO_0, RPIO.IN)
RPIO.setup(GPIO_1, RPIO.IN)

RPIO.add_interrupt_callback(GPIO_0, print_value, edge='both', pull_up_down=RPIO.PUD_UP)
RPIO.add_interrupt_callback(GPIO_1, print_value, edge='both', pull_up_down=RPIO.PUD_UP)

RPIO.wait_for_interrupts()

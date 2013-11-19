#!/usr/bin/python3.2

import RPIO
import signal
import sys
from cardReader import CardReader

BIT_TRANSMISSION_TIME = 0.002 #From wiegand specification
FRAMESIZE = 26 #Supposed size of received frame
FRAMETIME = FRAMESIZE * BIT_TRANSMISSION_TIME #Theoric time necessary to transfer a frame
ALLOWANCE = 50 #Auhtorized allowance for the transmission time in percent
TIMEOUT = FRAMETIME*(1+ALLOWANCE/100) #Real time allowed for the transmission

#Creating readers
readersList = [
CardReader(23, 24, TIMEOUT),
#CardReader(8, 7, TIMEOUT)
]

def closeProgram(signal, frame):
	""" Close fonction"""
	print("\nResseting GPIO...", end="")
	RPIO.cleanup() #Reset every channel that has been set up by this program, and unexport interrupt gpio interfaces
	print(" ok")
	print("exiting")
	sys.exit(0)

signal.signal(signal.SIGINT, closeProgram)
	

#Starting readers
readersCount = 1
for reader in readersList:
    print("Initializing reader " + str(readersCount) + "...", end = "")
    reader.registerReader()
    print(" Done !")
    readersCount += 1

#Ready message
print("Ready to go !")

RPIO.wait_for_interrupts()

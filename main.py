#!/usr/bin/python3.2

import RPIO
from cardReader import CardReader

BIT_TRANSMISSION_TIME = 0.002 #From wiegand specification
FRAMESIZE = 26 #Supposed size of received frame
FRAMETIME = FRAMESIZE * BIT_TRANSMISSION_TIME #Theoric time necessary to transfer a frame
ALLOWANCE = 10 #Auhtorized allowance for the transmission time
TIMEOUT = FRAMETIME*(1+ALLOWANCE/100) #Real time allowed for the transmission

#Creating readers
readersList = [CardReader(23, 24, TIMEOUT)]

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

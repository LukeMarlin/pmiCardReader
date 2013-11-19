import RPIO
import threading

class CardReader(object):
	"""Class representing a reader. One object should be instantiated for each physical reader"""

	def __init__(self, GPIO_0, GPIO_1, TIMEOUT):
		#Pins used to receive 0s and 1s
		self.GPIO_0 = GPIO_0
		self.GPIO_1 = GPIO_1
	
		self.tag = "" #The buffer used to store the RFID Tag
		self.TIMEOUT = TIMEOUT #Real time allowed for the transmission
		return super().__init__()

	def addBitToTag(self, gpio_id, val):

		#Beginning of a new frame, we start the timer
		if self.tag == "":
			self.t = threading.Timer(self.TIMEOUT, self.processTag)
			self.t.start()

		#We check wether we received a 0 or a 1
		if gpio_id == self.GPIO_0:
			self.tag += "0"
		elif gpio_id == self.GPIO_1:
			self.tag += "1"	

	def registerReader(self, edge = 'falling', pull_up_down=RPIO.PUD_UP):
		RPIO.setup(self.GPIO_0, RPIO.IN)
		RPIO.setup(self.GPIO_1, RPIO.IN)
		RPIO.add_interrupt_callback(self.GPIO_0, self.addBitToTag, edge = edge, pull_up_down = pull_up_down)
		RPIO.add_interrupt_callback(self.GPIO_1, self.addBitToTag, edge = edge, pull_up_down = pull_up_down)
    
		#Initializing timer
		self.t = threading.Timer(0.1, self.processTag)
		self.t.start()

	def removeReader(self):
		RPIO.del_interrupt_callback(self.GPIO_0)
		RPIO.del_interrupt_callback(self.GPIO_1)

	#Method triggered after Timer tick that prints out the tag
	def processTag(self):
		if self.tag == "":
			return
		print("Frame of length (" + str(len(self.tag)) + "): " + self.tag + " (" + str(CardReader.binaryToInt(self.tag)) + ")" )
		self.tag = ""


	#Method to convert the RFID binary value into a readable integer
	@staticmethod
	def binaryToInt(binary_string):
		binary_string = binary_string[1:-1] #Removing the first and last bit (Non-data bits)
		result = int(binary_string, 2)
		return result

##########################################
##	motor.py - Motor-Klasse		##
##########################################

##IMPORT
from RPIO import PWM
import time

class Motor (object):
	def __init__(self, pin, minW = 0, maxW = 100):
		PWM.set_loglevel(PWM.LOG_LEVEL_ERRORS)
		
		self.__pin = pin
		self.__minW = minW
		self.__maxW = maxW
		self.__servo = PWM.Servo()
		self.__W = 0
	
	def calibrate_esc(self):
		print ("Disconnect ESC-Power")
		res = raw_input()
		#self.__servo.set_servo(self.__pin, 2000)
		self.setW(100)
		print ("Connect ESC-Power. Wait for BEEP")
		res = raw_input()
		#self.__servo.set_servo(self.__pin, 1000)
		self.setW(0)

	def start(self):
		#self.__servo.set_servo(self.__pin, 1000)
		self.setW(0)
	
	def stop(self):
		self.__servo.stop_servo(self.__pin)

	def normalizeW(self, W):
		if W < self.__minW:
			return self.__minW
		elif W > self.__maxW:
			return self.__maxW
		else:
			return W

	def increase(self, value = 5):
		self.__W = self.normalizeW(self.__W + value)
		
		self.setW()

	def decrease(self, value = 5):
		self.__W = self.normalizeW(self.__W - value)

		self.setW()

	def setW(self, W = None):
		if W != None:
			self.__W = W
		self.__servo.set_servo(self.__pin, 1000+self.__W*10)

		

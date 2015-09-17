# coding: utf-8

##########################################
# accel.py - Gyroskop-Klasse
##########################################

#IMPORT
from time import sleep
#importiere smbus für Zugriff auf den i2c-Port
import smbus
import string

class Accel (object):

	def __init__(self, i2c_bus = 1, i2c_address = 0x53):
		self.__i2c_bus = smbus.SMBus(i2c_bus)
		self.i2c_address = i2c_address
		self.__i2c_bus.write_byte_data(self.i2c_address, 0x2D, 0x08)

	def read(self):
		self.bytes = self.__i2c_bus.read_i2c_block_data(self.i2c_address, 0x32, 6)
	
	def getResult(self, refresh=0):
		if refresh:
			self.read()
		res = []
		for i in range(0, 6, 2):
			g = self.bytes[i] | (self.bytes[i+1] << 8)
			if g > 32767:
				g -= 65536
			res.append(g)
		return res

	def getX(self):
		X = self.read()[0]
		return X
	
	def getY(self):
		Y = self.read()[1]
		return Y
	
	def getZ(self):
		Y = self.read()[2]
		return Y
##########################################
##	gyro.py - Gyroskop-Klasse	##
##########################################

#IMPORT
from time import sleep
#importiere smbus für Zugriff auf den i2c-Port
import smbus
import string

class Gyro (object):
	def __init__(self, i2c_bus = 1, i2c_address = 0x69):
		self.__i2c_bus = smbus.SMBus(i2c_bus)
		self.i2c_address = i2c_address
		
		self.config()
		pass
	
	def getSignedNumber(self, number):
		if number & (1 << 15):
		    return number | ~65535
		else:
		    return number & 65535
	
	def config(self):
		#normal mode and all axes on to control reg1
		i2c_bus.write_byte_data(i2c_address,0x20,0x0F)
		#full 2000dps to control reg4
		i2c_bus.write_byte_data(i2c_address,0x23,0x20)

	def readX(self):
		i2c_bus.write_byte(i2c_address,0x28)
		X_L = i2c_bus.read_byte(i2c_address)
		i2c_bus.write_byte(i2c_address,0x29)
		X_H = i2c_bus.read_byte(i2c_address)
		X = X_H << 8 | X_L
		return X
		
	def readY(self):
		i2c_bus.write_byte(i2c_address,0x2A)
		Y_L = i2c_bus.read_byte(i2c_address)
		i2c_bus.write_byte(i2c_address,0x2B)
		Y_H = i2c_bus.read_byte(i2c_address)
		Y = Y_H << 8 | Y_L
		return Y
		
	def readZ(self):
		i2c_bus.write_byte(i2c_address,0x2C)
		Z_L = i2c_bus.read_byte(i2c_address)
		i2c_bus.write_byte(i2c_address,0x2D)
		Z_H = i2c_bus.read_byte(i2c_address)
		Z = Z_H << 8 | Z_L
		return Z
	
	def getX(self):
		X = self.readX()
		X = self.getSignedNumber(X)
		return X
	
	def getY(self):
		Y = self.readY()
		Y = self.getSignedNumber(Y)
		return Y
	
	def getZ(self):
		Y = self.readY()
		Y = self.getSignedNumber(Y)
		return Y
##########################################
##	gyro.py - Gyroskop-Klasse	##
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
		
		self.config()
		pass
	
	def config(self):
		#enable the accelerometer
		self.__i2c_bus.write_byte_data(i2c_address,0x2D,0x08)

	def readList(self):
        return self.__i2c_bus.read_i2c_block_data(self.i2c_address, 0x32, 6)
    
    def read(self):
        raw = self.readList()
        res = []
        for i in range(0, 6, 2):
            g = raw[i] | (raw[i+1] << 8)
            if g > 32767: g -= 65536
            res.append(g)
        return res

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
    
accel = Accel()
print accel.read()
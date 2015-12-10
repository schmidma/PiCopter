# coding: utf-8

##########################################
# gyro.py - Gyroskop-Klasse
##########################################

#IMPORT
import smbus

class Gyro():
    
    def __init__(self, i2c_bus = 1, i2c_address = 0x69):
        
        self.__CalibrationIteration = 30
        self.__i2c_bus = smbus.SMBus(i2c_bus)
        
        self.i2c_address = i2c_address
        
        self.__i2c_bus.write_byte_data(self.i2c_address, 0x20, 0x0F)
        self.__i2c_bus.write_byte_data(self.i2c_address, 0x23, 0b00110000)
        
        self.offset = [0,0,0]
        
        self.gyro_axes = [0,0,0]
        
        self.pitch = 0
        self.roll = 0

    def read(self):
        self.__i2c_bus.write_byte(self.i2c_address,0x28)
        X_L = self.__i2c_bus.read_byte(self.i2c_address)
        self.__i2c_bus.write_byte(self.i2c_address,0x29)
        X_H = self.__i2c_bus.read_byte(self.i2c_address)

        self.__i2c_bus.write_byte(self.i2c_address,0x2A)
        Y_L = self.__i2c_bus.read_byte(self.i2c_address)
        self.__i2c_bus.write_byte(self.i2c_address,0x2B)
        Y_H = self.__i2c_bus.read_byte(self.i2c_address)

        self.__i2c_bus.write_byte(self.i2c_address,0x2C)
        Z_L = self.__i2c_bus.read_byte(self.i2c_address)
        self.__i2c_bus.write_byte(self.i2c_address,0x2D)
        Z_H = self.__i2c_bus.read_byte(self.i2c_address)
        
        self.bytes = [Y_L, Y_H, X_L, X_H, Z_L, Z_H]
        
    def getResult(self):
        self.read()
        
        res = []
        
        for i in range(0, 6, 2):
            g = self.bytes[i] | (self.bytes[i+1] << 8)
            if g > 32767:
                g -= 65536
            res.append(g*0.7)
        
        return res
    
    def gyroCalculation(self, delta_time):
        result = self.getResult()
        self.gyro_axes = [self.gyro_axes[i]+((result[i]-self.offset[i])/10*(delta_time/1000.0)) for i in range (3)]
        self.pitch = self.gyro_axes[0]
        self.roll = -1*self.gyro_axes[1]
    
    def calibrateGyro(self):
        self.offset = [0,0,0]
        self.gyro_axes = [0,0,0]
        for i in range(self.__CalibrationIteration):
            result = self.getResult()
            self.offset = [self.offset[a] + result[a] for a in range(3)]
        self.offset = [self.offset[0]/self.__CalibrationIteration, self.offset[1]/self.__CalibrationIteration, self.offset[2]/self.__CalibrationIteration]
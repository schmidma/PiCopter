# coding: utf-8

##########################################
# gyro.py - Gyroskop-Klasse
##########################################

#IMPORT
import smbus

class Gyro():
    def __init__(self, i2c_bus = 1, i2c_address = 0x69):
        self.__i2c_bus = smbus.SMBus(i2c_bus)
        
        self.i2c_address = i2c_address
        
        self.__i2c_bus.write_byte_data(self.i2c_address, 0x20, 0x0F)
        self.__i2c_bus.write_byte_data(self.i2c_address, 0x23, 0b00110000)
        
        self.calibrationValues = [0,0,0]
        
        self.gyro_diff = [0,0,0]
        self.gyro_axes = [0,0,0]

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
    
            res.append(g)
        
        res[1] = -res[1]
        
        """for i in range(3):
            if 0 < res[i] < 10:
                res[i] = 0
            elif 0 > res[i] > -10:
                res[i] = 0
        """
        return res
    
    def gyroCalculation(self, delta_time):
        result = self.getResult()
        print(result)
        print(self.calibrationValues)
        print(delta_time)
        
        self.gyro_axes = [self.gyro_axes[i]+((result[i]+self.calibrationValues[i])/10*(delta_time/1000.0)) for i in range (3)]
        print(self.gyro_axes)
        self.gyro_diff = [self.gyro_axes[i]/100 for i in range(3)]

        for i in range(3):
            if self.gyro_diff[i] > 10:
                self.gyro_diff[i] = 10
            elif self.gyro_diff[i] < -10:
                self.gyro_diff[i] = -10
    
    def calibrateGyro(self):
        for i in range(10):
            result = self.getResult()
            self.calibrationValues = [self.calibrationValues[a] + result[a] for a in range(3)]
            
        self.calibrationValues = [-result[0]/10, -result[1]/10, -result[2]/10]
    
    def getGyroValues(self, delta_time):
        gyro_result = self.getResult()
        self.gyro_axes = [(self.gyro_axes[i] + gyro_result[i]+self.calibrationValues[i])*delta_time for i in range(3)]
        return self.gyro_axes

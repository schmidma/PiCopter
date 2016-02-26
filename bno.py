# coding: utf-8

##########################################
# accel.py - Accelerometer-Klasse
##########################################

#IMPORT
#importiere smbus für Zugriff auf die i2c-Ports
import smbus
import time

# I2C addresses
BNO055_ADDRESS_A                     = 0x28
BNO055_ADDRESS_B                     = 0x29
BNO055_ID                            = 0xA0

# Page id register definition
BNO055_PAGE_ID_ADDR                  = 0x07

# PAGE0 REGISTER DEFINITION START
BNO055_CHIP_ID_ADDR                  = 0x00
BNO055_ACCEL_REV_ID_ADDR             = 0x01
BNO055_MAG_REV_ID_ADDR               = 0x02
BNO055_GYRO_REV_ID_ADDR              = 0x03
BNO055_SW_REV_ID_LSB_ADDR            = 0x04
BNO055_SW_REV_ID_MSB_ADDR            = 0x05
BNO055_BL_REV_ID_ADDR                = 0X06

# Euler data registers
BNO055_EULER_H_LSB_ADDR              = 0X1A
BNO055_EULER_H_MSB_ADDR              = 0X1B
BNO055_EULER_R_LSB_ADDR              = 0X1C
BNO055_EULER_R_MSB_ADDR              = 0X1D
BNO055_EULER_P_LSB_ADDR              = 0X1E
BNO055_EULER_P_MSB_ADDR              = 0X1F

# Status registers
BNO055_CALIB_STAT_ADDR               = 0X35
BNO055_SELFTEST_RESULT_ADDR          = 0X36

BNO055_SYS_CLK_STAT_ADDR             = 0X38
BNO055_SYS_STAT_ADDR                 = 0X39
BNO055_SYS_ERR_ADDR                  = 0X3A


# Mode registers
BNO055_OPR_MODE_ADDR                 = 0X3D
BNO055_PWR_MODE_ADDR                 = 0X3E

BNO055_SYS_TRIGGER_ADDR              = 0X3F

# Power modes
POWER_MODE_NORMAL                    = 0X00

# Operation mode settings
OPERATION_MODE_CONFIG                = 0X00
OPERATION_MODE_NDOF                  = 0X0C


class BNO ():
    
    def __init__(self, i2c_bus = 1, i2c_address = BNO055_ADDRESS_A, mode=OPERATION_MODE_NDOF):
        
        self.heading = 0
        self.pitch = 0
        self.roll = 0
        
        self.offset = [0,0,0]
        self.__CalibrationIteration = 30
        
        self.__i2c_bus = smbus.SMBus(i2c_bus)
        
        self.i2c_address = i2c_address
        
        ##SETUP
        self._mode = mode
        
        self._config_mode()
        
        # Delay for 30 milliseconds (datsheet recommends 19ms, but a little more
        # can't hurt and the kernel is going to spend some unknown amount of time
        # too).
        
        time.sleep(0.03)
        
        self._write_byte(BNO055_PAGE_ID_ADDR, 0)
        
        self._write_byte(BNO055_SYS_TRIGGER_ADDR, 0x20)
        
        # Wait 650ms after reset for chip to be ready (as suggested in datasheet).
        time.sleep(0.65)
        
        self._write_byte(BNO055_PWR_MODE_ADDR, POWER_MODE_NORMAL)
        
        self._write_byte(BNO055_SYS_TRIGGER_ADDR, 0x0)
        
        self._operation_mode()    
    
    def _config_mode(self):
        self._set_mode(OPERATION_MODE_CONFIG)
        
    def _operation_mode(self):
        self._set_mode(self._mode)
        
    def _set_mode(self, mode):
        self._write_byte(BNO055_OPR_MODE_ADDR, mode)
        time.sleep(0.03)
    
    def _write_byte(self, reg, data):
        self.__i2c_bus.write_byte_data(self.i2c_address, reg, data)
    
    def _read_byte(self, reg):
        return self.__i2c_bus.read_byte_data(self.i2c_address, reg)
    
    def _read_bytes(self, reg, length):
        # Read a number of unsigned byte values starting from the provided address.
        return bytearray(self._readList(reg, length))
    
    def _readList(self, reg, length):
        return self.__i2c_bus.read_i2c_block_data(self.i2c_address, reg, length)
        
    def _read_vector(self, address, count=3):
        # Read count number of 16-bit signed values starting from the provided
        # address. Returns a tuple of the values that were read.
        data = self._read_bytes(address, count*2)
        
        result = [0]*count
        for i in range(count):
            result[i] = ((data[i*2+1] << 8) | data[i*2]) & 0xFFFF
            if result[i] > 32767:
                result[i] -= 65536
        return result
    
    def read_euler(self):
        """Return the current absolute orientation as a tuple of heading, roll,
        and pitch euler angles in degrees.
        """
        heading, roll, pitch = self._read_vector(BNO055_EULER_H_LSB_ADDR)
        return (heading/16.0, roll/16.0, pitch/16.0)
    
    def get_calibration_status(self):
        """Read the calibration status of the sensors and return a 4 tuple with
        calibration status as follows:
          - System, 3=fully calibrated, 0=not calibrated
          - Gyroscope, 3=fully calibrated, 0=not calibrated
          - Accelerometer, 3=fully calibrated, 0=not calibrated
          - Magnetometer, 3=fully calibrated, 0=not calibrated
        """
        # Return the calibration status register value.
        cal_status = self._read_byte(BNO055_CALIB_STAT_ADDR)
        sys = (cal_status >> 6) & 0x03
        gyro = (cal_status >> 4) & 0x03
        accel = (cal_status >> 2) & 0x03
        mag = cal_status & 0x03
        # Return the results as a tuple of all 3 values.
        return (sys, gyro, accel, mag)
    
    def get_system_status(self, run_self_test=True):
        """Return a tuple with status information.  Three values will be returned:
          - System status register value with the following meaning:
              0 = Idle
              1 = System Error
              2 = Initializing Peripherals
              3 = System Initialization
              4 = Executing Self-Test
              5 = Sensor fusion algorithm running
              6 = System running without fusion algorithms
          - Self test result register value with the following meaning:
              Bit value: 1 = test passed, 0 = test failed
              Bit 0 = Accelerometer self test
              Bit 1 = Magnetometer self test
              Bit 2 = Gyroscope self test
              Bit 3 = MCU self test
              Value of 0x0F = all good!
          - System error register value with the following meaning:
              0 = No error
              1 = Peripheral initialization error
              2 = System initialization error
              3 = Self test result failed
              4 = Register map value out of range
              5 = Register map address out of range
              6 = Register map write error
              7 = BNO low power mode not available for selected operation mode
              8 = Accelerometer power mode not available
              9 = Fusion algorithm configuration error
             10 = Sensor configuration error

        If run_self_test is passed in as False then no self test is performed and
        None will be returned for the self test result.  Note that running a
        self test requires going into config mode which will stop the fusion
        engine from running.
        """
        self_test = None
        if run_self_test:
            # Switch to configuration mode if running self test.
            self._config_mode()
            # Perform a self test.
            sys_trigger = self._read_byte(BNO055_SYS_TRIGGER_ADDR)
            self._write_byte(BNO055_SYS_TRIGGER_ADDR, sys_trigger | 0x1)
            # Wait for self test to finish.
            time.sleep(1.0)
            # Read test result.
            self_test = self._read_byte(BNO055_SELFTEST_RESULT_ADDR)
            # Go back to operation mode.
            self._operation_mode()
        # Now read status and error registers.
        status = self._read_byte(BNO055_SYS_STAT_ADDR)
        error = self._read_byte(BNO055_SYS_ERR_ADDR)
        # Return the results as a tuple of all 3 values.
        return (status, self_test, error)
    
    def get_revision(self):
        """Return a tuple with revision information about the BNO055 chip. Will return 5 values:
          - Software revision
          - Bootloader version
          - Accelerometer ID
          - Magnetometer ID
          - Gyro ID
        """
        # Read revision values.
        accel = self._read_byte(BNO055_ACCEL_REV_ID_ADDR)
        mag = self._read_byte(BNO055_MAG_REV_ID_ADDR)
        gyro = self._read_byte(BNO055_GYRO_REV_ID_ADDR)
        bl = self._read_byte(BNO055_BL_REV_ID_ADDR)
        sw_lsb = self._read_byte(BNO055_SW_REV_ID_LSB_ADDR)
        sw_msb = self._read_byte(BNO055_SW_REV_ID_MSB_ADDR)
        sw = ((sw_msb << 8) | sw_lsb) & 0xFFFF
        # Return the results as a tuple of all 5 values.
        return (sw, bl, accel, mag, gyro)

    def calibrateBNO(self):
        self.offset = [0,0,0]
        
        for i in range(self.__CalibrationIteration):
            heading, roll, pitch = self.read_euler()
            if heading > 360 or 0 > heading:
                heading = self.heading
            if roll > 90 or -90 > roll:
                roll = self.roll
            if pitch > 180 or -180 > pitch:
                pitch = self.pitch
            self.offset[0] += heading
            self.offset[1] += roll
            self.offset[2] += pitch
            
        self.offset = [self.offset[0]/self.__CalibrationIteration, self.offset[1]/self.__CalibrationIteration, self.offset[2]/self.__CalibrationIteration]
            
    def bnoCalculation(self):
        heading, roll, pitch = self.read_euler()
        if heading > 360 or 0 > heading:
            heading = self.heading
        if roll > 90 or -90 > roll:
            roll = self.roll
        if pitch > 180 or -180 > pitch:
            pitch = self.pitch
            
        heading = heading - self.offset[0]
        roll = roll - self.offset[1]
        pitch = pitch - self.offset[2]
        
        return [heading, roll, pitch]
    
    def tick(self):
        self.heading, self.roll, self.pitch = self.bnoCalculation()
        
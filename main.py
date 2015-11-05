# coding: utf-8

##########################################
# MAIN.py - Hauptfunktion
##########################################

from gamepad import Gamepad
from accel import Accel
from motor import Motor

class Main():
    def __init__(self):        
        self.main_throttle = 0
        self.throttle = [0,0,0,0]

        self.holdPosition = 0
        self.holdHeight = 0
        self.isGamepad = 1
        
        self.gamepad = Gamepad()
        self.gamepad_axis = [0,0,0]
        self.gamepad_throttle = 0
        
        self.accel = Accel()
        self.accel_axis = [0,0,0]
        self.accel_calib = [0,0,0]
        self.accel_diff = [0,0,0]
        
        self.m1 = Motor(15)
        self.m2 = Motor(27)
        self.m3 = Motor(10)
        self.m4 = Motor(7)
        
        self.motors = [self.m1, self.m2, self.m3, self.m4]
        
        print ("IDLE")
        self.idle()
        
    def idle(self):
        while not self.gamepad.isStart():
            print ("IDLE")
        #if self.gamepad.isStart():
        print ("START")
        self.start()
        self.changeMotorSpeed()
        
    def getGamepadValues(self):
        self.gamepad_axis = self.gamepad.getAxis()
        if self.gamepad.isCalibFront():
            self.accel_calib[0] += 1
        if self.gamepad.isCalibRear():
            self.accel_calib[0] -= 1
        if self.gamepad.isCalibRight():
            self.accel_calib[1] += 1
        if self.gamepad.isCalibLeft():
            self.accel_calib[1] -= 1
        self.gamepad_throttle = self.gamepad.getThrottle()
        self.holdPosition = self.gamepad.isholdPosition()
        self.holdHeight = self.gamepad.isholdHeight()
        
    def getAccelValues(self):
        #accel_result = self.accel.getResult()
        #calibrateValues = self.accel.getCalibrateValues()
        #self.accel_axis = [accel_result[0]-calibrateValues[0], accel_result[1]-calibrateValues[1], accel_result[2]-calibrateValues[2]]
        #self.accel_axis = [accel_result[i]-calibrateValues[i] for i in range(3)]
        pass
        
        
    def start(self):
        for m in self.motors:
            m.start()
        
    def changeMotorSpeed(self):
        while self.gamepad.isStart():
            self.getGamepadValues()
            self.getAccelValues()
            
            if (self.holdHeight):
                print ("HoldHeight!")
            else:
                self.main_throttle = self.gamepad_throttle
            
            self.accel_diff = [self.accel_axis[i]-self.accel_calib[i] for i in range (4)]
            
            self.throttle[0] += self.accel_diff[0]
            self.throttle[1] += self.accel_diff[1]
            self.throttle[2] -= self.accel_diff[2]
            self.throttle[3] -= self.accel_diff[3]
            
            print (self.main_throttle)
            print (self.throttle)
            #for i in range(4):
            #    self.motors[i].setW(self.main_throttle+self.throttle[i])
            
        self.idle()
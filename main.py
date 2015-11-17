# coding: utf-8

##########################################
# MAIN.py - Hauptfunktion
##########################################

from gamepad import Gamepad
from accel import Accel
from motor import Motor
import time

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
            print("IDLE")
        print ("START")
        self.start()
        self.changeMotorSpeed()

        
    def getGamepadValues(self):
        self.gamepad_axis = self.gamepad.getAxis()
        if self.gamepad.isCalibFront():
            self.accel.addToCalibrationValues([1,0,0])
        if self.gamepad.isCalibRear():
            self.accel.addToCalibrationValues([-1,0,0])
        if self.gamepad.isCalibRight():
            self.accel.addToCalibrationValues([0,1,0])
        if self.gamepad.isCalibLeft():
            self.accel.addToCalibrationValues([0,-1,0])
        if self.gamepad.isCalib():
            self.accel.calibrateAccel()
        self.gamepad_throttle = self.gamepad.getThrottle()
        self.holdPosition = self.gamepad.isHoldPosition()
        self.holdHeight = self.gamepad.isHoldHeight()
        
    def getAccelValues(self):
        accel_result = self.accel.getResult(1)
        calibrationValues = self.accel.getCalibrationValues()
        #self.accel_axis = [accel_result[0]-calibrateValues[0], accel_result[1]-calibrateValues[1], accel_result[2]-calibrateValues[2]]
        self.accel_axis = [accel_result[i]+calibrationValues[i] for i in range(3)]
        
        
    def start(self):
        while self.gamepad.getThrottle()<=50:
            print("Throttle to min 50")
        while self.gamepad.getThrottle()!=0:
            print("Throttle to 0 to start!")
        for m in self.motors:
            m.start()
        print("START")
        
    def changeMotorSpeed(self):
        while self.gamepad.isStart():
            self.getGamepadValues()
            self.getAccelValues()
            
            if (self.holdHeight):
                print ("HoldHeight!")
            else:
                self.main_throttle = self.gamepad_throttle
            
            self.accel_diff = [(self.accel.getResult(1)[i]+self.accel.getCalibrationValues()[i])/10 for i in range (3)]
            for i in range(3):
                if self.accel_diff[i] > 10:
                    self.accel_diff[i] = 10
            
            #Accel-Motor-Steuereung
            self.throttle[0] += self.accel_diff[0]
            self.throttle[1] += self.accel_diff[0]
            self.throttle[2] -= self.accel_diff[0]
            self.throttle[3] -= self.accel_diff[0]
    
            self.throttle[0] -= self.accel_diff[1]
            self.throttle[1] += self.accel_diff[1]
            self.throttle[2] += self.accel_diff[1]
            self.throttle[3] -= self.accel_diff[1]

            #Pad-Motor-Steuerung
            self.throttle[0] += self.gamepad_axis[1]*10
            self.throttle[1] += self.gamepad_axis[1]*10
            self.throttle[2] -= self.gamepad_axis[1]*10
            self.throttle[3] -= self.gamepad_axis[1]*10
    
            self.throttle[0] += self.gamepad_axis[0]*10
            self.throttle[1] -= self.gamepad_axis[0]*10
            self.throttle[2] -= self.gamepad_axis[0]*10
            self.throttle[3] += self.gamepad_axis[0]*10

            print(self.accel.getResult(0))
            print(self.accel.getCalibrationValues())
            print(self.accel_diff)

            print (self.main_throttle)
            print (self.throttle)
        
            for i in range(4):
                if self.main_throttle > 0:
                    mthrottle = int(self.main_throttle+self.throttle[i])
                else:
                    mthrottle = int(0)
                print(mthrottle)
                self.motors[i].setW(mthrottle)
            self.throttle = [0,0,0,0]
        self.idle()

go = Main()

# coding: utf-8

##########################################
# gamepad.py - Gamepad-Klasse
##########################################

import pygame

class Gamepad():
    def __init__(self):
        #pygame.init()
        #self.clock = pygame.time.Clock()
        self.pad = pygame.joystick.Joystick(0)
        self.pad.init()
        
        self.calibrationValues = [0,0,0]
        
        self.isStart = 0
        self.isCalib = 0
        self.isHoldHeight = 0
        self.isHoldPosition = 0
        self.isAccel = 0
        self.throttle = 0
        self.axis = [0,0,0]
        
        self.bCalibFront = 4
        self.bCalibRear = 6
        self.bCalibRight =5
        self.bCalibLeft = 7
        self.bCalib = 0
        self.aXAxis = 0
        self.aYAxis = 1
        
        self.bStart = 3
        self.bHome = 16
        self.bHoldHeight = 12
        self.bHoldPosition = 13
        self.bAccel = 15
        self.aThrottle = 13
    
    def handleButtonDown(self, button):
        if button == self.bStart:
            self.toggleStart()
        elif button == self.bHoldHeight:
            self.toggleHoldHeight()
            #print("holdHeight: "+str(self.isHoldHeight))
        elif button == self.bHoldPosition:
            self.toggleHoldPosition()
            #print("holdPosition: "+str(self.isHoldPosition))
        elif button == self.bCalib:
            self.toggleCalib()
            #print("calib: "+str(self.isCalib))
        elif button == self.bHome:
            pygame.event.post(pygame.event.Event(pygame.QUIT))
        elif button == self.bAccel:
            self.toggleAccel()
        elif button == self.bCalibFront:
            self.calibrationValues[0] += 1
        elif button == self.bCalibRear:
            self.calibrationValues[0] -= 1
        elif button == self.bCalibRight:
            self.calibrationValues[1] += 1
        elif button == self.bCalibLeft:
            self.calibrationValues[1] -= 1
    
    def handleButtonUp(self, button):
        if button == self.bCalib:
            self.toggleCalib()
            #print("calib: "+str(self.isCalib))
    
    def toggleAccel(self):
        self.isAccel = not self.isAccel
    
    def toggleStart(self):
        self.isStart = not self.isStart
    
    def toggleHoldHeight(self):
        self.isHoldHeight = not self.isHoldHeight
        
    def toggleHoldPosition(self):
        self.isHoldPosition = not self.isHoldPosition
    
    def toggleCalib(self):
        self.isCalib = not self.isCalib
    
    def getThrottle(self):
        self.throttle = (self.pad.get_axis(self.aThrottle)+1)/2*100
        return self.throttle
    
    def getAxis(self):
        self.axis = [-self.pad.get_axis(self.aYAxis),self.pad.get_axis(self.aXAxis),0]
        return self.axis

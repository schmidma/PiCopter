# coding: utf-8

##########################################
# gamepad.py - Gamepad-Klasse
##########################################

import pygame

class Gamepad():
    def __init__(self):
        pygame.init()
        self.pad = pygame.joystick.Joystick(0)
        self.pad.init()
        
        self.start = 0
        self.holdHeight = 0
        self.holdPosition = 0
        self.throttle = 0
        self.axis = [0,0,0]
        
        self.bCalibFront = 4
        self.bCalibRear = 6
        self.bCalibRight =5
        self.bCalibLeft = 7
        
        self.bStart = 3
        self.bHoldHeight = 12
        self.bHoldPosition = 13
        self.bThrottle = 13
    
    def isCalibFront(self):
        pygame.event.pump()
        return self.pad.get_button(self.bCalibFront)
    
    def isCalibRear(self):
        pygame.event.pump()
        return self.pad.get_button(self.bCalibRear)
    
    def isCalibRight(self):
        pygame.event.pump()
        return self.pad.get_button(self.bCalibRight)
    
    def isCalibLeft(self):
        pygame.event.pump()
        return self.pad.get_button(self.bCalibLeft)
    
    def isStart(self):
        pygame.event.pump()
        start = self.pad.get_button(self.bStart)
        if start==1:
            self.start = not self.start
        return self.start
    
    def isHoldHeight(self):
        pygame.event.pump()
        if self.pad.get_button(self.bHoldHeight):
            self.holdHeight = not self.holdHeight
        return self.holdHeight
    
    def isHoldPosition(self):
        pygame.event.pump()
        if self.pad.get_button(self.bHoldPosition):
            self.holdPosition = not self.holdPosition
        return self.holdPosition
    
    def getThrottle(self):
        pygame.event.pump()
        self.throttle = (self.pad.get_axis(self.bThrottle)+1)/2*100
        return self.throttle
    
    def getAxis(self):
        pass

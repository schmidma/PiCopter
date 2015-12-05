# coding: utf-8

##########################################
# gamepad.py - Gamepad-Klasse
##########################################

import pygame

class Gamepad():
    def __init__(self):
        self.pad = pygame.joystick.Joystick(0)
        self.pad.init()
        
        self.calibrationValues = [0,0,0]
        
        self.isStart = 0
        self.isCalib = 0
        self.isHoldHeight = 0
        self.isHoldPosition = 0
        self.isGyro = 0
        self.throttle = 0
        self.axis = [0,0,0]
        
        self.mapping = {"select":0, "start":3, "up":4, "right":5, "down":6, "left":7, "l2":10, "r2":13, "r1":11, "l1":10, "triangle":12, "circle":13, "x":14, "square":15, "PS":16, "l-stick-x":0, "l-stick-y":1, "r-stick-x":2, "r-stick-y":3}
    
    def handleButtonDown(self, button):
        if button == self.mapping["start"]:
            self.toggleStart()
        elif button == self.mapping["triangle"]:
            self.toggleHoldHeight()
        elif button == self.mapping["circle"]:
            self.toggleHoldPosition()
        elif button == self.mapping["select"]:
            self.toggleCalib()
        elif button == self.mapping["PS"]:
            pygame.event.post(pygame.event.Event(pygame.QUIT))
        elif button == self.mapping["square"]:
            self.toggleGyro()
        elif button == self.mapping["up"]:
            self.calibrationValues[0] += 0.2
        elif button == self.mapping["down"]:
            self.calibrationValues[0] -= 0.2
        elif button == self.mapping["right"]:
            self.calibrationValues[1] += 0.2
        elif button == self.mapping["left"]:
            self.calibrationValues[1] -= 0.2
        elif button == self.mapping["l1"]:
            self.calibrationValues[2] += 0.5
        elif button == self.mapping["r1"]:
            self.calibrationValues[2] -= 0.5
    
    def handleButtonUp(self, button):
        if button == self.mapping["select"]:
            self.toggleCalib()
    
    def toggleGyro(self):
        self.isGyro = not self.isGyro
    
    def toggleStart(self):
        self.isStart = not self.isStart
    
    def toggleHoldHeight(self):
        self.isHoldHeight = not self.isHoldHeight
        
    def toggleHoldPosition(self):
        self.isHoldPosition = not self.isHoldPosition
    
    def toggleCalib(self):
        self.isCalib = not self.isCalib
    
    def getThrottle(self):
        self.throttle = (self.pad.get_axis(self.mapping["r2"])+1)/2*100
        return self.throttle
    
    def getAxis(self):
        self.axis = [-self.pad.get_axis(self.mapping["l-stick-y"]),self.pad.get_axis(self.mapping["l-stick-x"]),0]
        return self.axis

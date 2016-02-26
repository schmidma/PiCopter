# coding: utf-8

##########################################
# gamepad.py - Gamepad-Klasse
##########################################

import pygame

class Gamepad():
    def __init__(self):
        self.pad = pygame.joystick.Joystick(0)
        self.pad.init()
        
        self.offset = [0,0,0]
        
        self.isStart = 0
        self.isCalib = 0
        self.isBNO = 0
        self.isSave = 0
        self.throttle = 0
        self.axis = [0,0,0]
        
        self.mapping = {"select":0, "start":3, "up":4, "right":5, "down":6, "left":7, "l2":10, "r2":13, "r1":11, "l1":10, "triangle":12, "circle":13, "x":14, "square":15, "PS":16, "l-stick-x":0, "l-stick-y":1, "r-stick-x":2, "r-stick-y":3}
    
    def handleButtonDown(self, button):
        if button == self.mapping["start"]:
            self.toggleStart()
        elif button == self.mapping["triangle"]:
            self.toggleSave()
        elif button == self.mapping["circle"]:
            pass
        elif button == self.mapping["select"]:
            self.toggleCalib()
        elif button == self.mapping["PS"]:
            pygame.event.post(pygame.event.Event(pygame.QUIT))
        elif button == self.mapping["square"]:
            self.toggleBNO()
        elif button == self.mapping["up"]:
            self.offset[0] += 0.2
        elif button == self.mapping["down"]:
            self.offset[0] -= 0.2
        elif button == self.mapping["right"]:
            self.offset[1] += 0.2
        elif button == self.mapping["left"]:
            self.offset[1] -= 0.2
        elif button == self.mapping["l1"]:
            self.offset[2] += 0.5
        elif button == self.mapping["r1"]:
            self.offset[2] -= 0.5
    
    def handleButtonUp(self, button):
        if button == self.mapping["select"]:
            self.isCalib = False
        if button == self.mapping["triangle"]:
            self.isSave = False
    
    def toggleBNO(self):
        self.isBNO = not self.isBNO
    
    def toggleSave(self):
        self.isSave = not self.isSave
    
    def toggleStart(self):
        self.isStart = not self.isStart
    
    def toggleCalib(self):
        self.isCalib = not self.isCalib
    
    def getThrottle(self):
        self.throttle = (self.pad.get_axis(self.mapping["r2"])+1)/2*100
        return self.throttle
    
    def getAxis(self):
        self.axis = [-self.pad.get_axis(self.mapping["l-stick-y"]),self.pad.get_axis(self.mapping["l-stick-x"]),0]
        return self.axis

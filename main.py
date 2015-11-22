#!/usr/bin/env python3
# coding: utf-8

##########################################
# MAIN.py - Hauptklasse
##########################################

from gamepad import Gamepad
from accel import Accel
from motor import Motor
from gui import Gui

from pygame.locals import *
import sys, os, time, pygame, curses

class Main():
    def __init__(self, DEBUG = False):
        self.DEBUG = DEBUG
        
        pygame.init()
        self.clock = pygame.time.Clock()
        self.max_fps = 120
        
        self.backgroundColor = (250,250,250)
    
        self.run = True
        self.started = False
    
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
        self.accel_throttle = [0,0,0]
        
        self.m1 = Motor(15)
        self.m2 = Motor(27)
        self.m3 = Motor(10)
        self.m4 = Motor(7)
        
        self.motors = [self.m1, self.m2, self.m3, self.m4]
        
        if self.DEBUG:
            self.gui = Gui()
        
        #print("Press 'Start' to start!")
        
        self.loop()
        
    def eventHandler(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                if self.DEBUG:
                    curses.endwin()
                sys.exit()
            elif event.type == JOYBUTTONDOWN:
                self.gamepad.handleButtonDown(event.button)
            elif event.type == JOYBUTTONUP:
                self.gamepad.handleButtonUp(event.button)
        
    def getGamepadValues(self):
        self.gamepad_axis = self.gamepad.getAxis()
        
        if self.gamepad.isCalib:
            self.accel.calibrateAccel()
        self.gamepad_throttle = self.gamepad.getThrottle()
 
    def getAccelValues(self):
        accel_result = self.accel.getResult(1)
        calibrationValues = self.accel.getCalibrationValues()
        self.accel_axis = [accel_result[i]+calibrationValues[i] for i in range(3)]
        
    def start_motors(self):
        #print("Throttle to min 50")
        self.gui.hideMessage()
        self.gui.showMessage("Calibrate Throttle!")
        
        while self.gamepad.getThrottle()<=50:
            pygame.event.pump()
        
        while self.gamepad.getThrottle()!=0:
            pygame.event.pump()
        
        for m in self.motors:
            m.start()
        
        self.started = True
        
        self.gui.hideMessage()
    
    def stop_motors(self):
        for m in self.motors:
            m.stop()
        self.started = False
        
    def accelCalculation(self):
        self.accel_diff = [(self.accel.getResult(1)[i]+self.accel.getCalibrationValues()[i])/260*100 for i in range (3)]
        
        #Beschränkung auf maximal 10% Einfluss
        for i in range(3):
            if self.accel_diff[i] > 10:
                self.accel_diff[i] = 10
            elif self.accel_diff[i] < -10:
                self.accel_diff[i] = -10
                
            if self.accel_diff[i] > 0:
                if self.accel_diff[i] > self.accel_throttle[i]:
                    self.accel_throttle[i] += 1
                else:
                    self.accel_throttle[i] -= 1
            elif self.accel_diff[i] < 0:
                if self.accel_diff[i] < self.accel_throttle[i]:
                    self.accel_throttle[i] -= 1
                else:
                    self.accel_throttle[i] += 1
        
    def changeMotorSpeed(self):
        self.throttle = [0,0,0,0]
        self.getGamepadValues()
        self.getAccelValues()
        
        if (self.gamepad.isHoldHeight):
            pass
        
        if (self.gamepad.isHoldPosition):
            pass
        
        if (self.gamepad.isAccel):
            self.accelCalculation()
            
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
        self.throttle[0] -= self.gamepad_axis[0]*10+self.gamepad.calibrationValues[0]
        self.throttle[1] -= self.gamepad_axis[0]*10+self.gamepad.calibrationValues[0]
        self.throttle[2] += self.gamepad_axis[0]*10+self.gamepad.calibrationValues[0]
        self.throttle[3] += self.gamepad_axis[0]*10+self.gamepad.calibrationValues[0]

        self.throttle[0] += self.gamepad_axis[1]*10+self.gamepad.calibrationValues[1]
        self.throttle[1] -= self.gamepad_axis[1]*10+self.gamepad.calibrationValues[1]
        self.throttle[2] -= self.gamepad_axis[1]*10+self.gamepad.calibrationValues[1]
        self.throttle[3] += self.gamepad_axis[1]*10+self.gamepad.calibrationValues[1]
        
        self.throttle = [int(self.gamepad_throttle+self.throttle[i]) for i in range(4)]
        
        for i in range(4):
            if self.throttle[i] > 100:
                self.throttle[i] = 100
            self.motors[i].setW(self.throttle[i])
            
    def loop(self):
        while self.run:
            self.clock.tick(self.max_fps)
            
            if self.DEBUG:
                self.gui.guiTick(self.clock.get_fps(), self.throttle, self.gamepad.isStart, self.gamepad.isHoldHeight, self.gamepad.isHoldPosition, self.gamepad.isAccel)
            pygame.event.pump()
            self.eventHandler()
            
            if self.gamepad.isStart:
                if not self.started:
                    self.start_motors()
                self.changeMotorSpeed()
            else:
                self.gui.showMessage("Press 'start'-Button to start!")
                if self.started:
                    self.stop_motors()


if len(sys.argv) > 1:
    if sys.argv[1] == "--debug":
        go = Main(True)
else:
    go = Main()
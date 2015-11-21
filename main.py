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
        self.gui.win_message.addstr(0, 0, "                              ", curses.A_BLINK)
        self.gui.win_message.addstr(0, 8, "Calibrate Throttle!", curses.A_BLINK)
        self.gui.win_message.refresh()
        while self.gamepad.getThrottle()<=50:
            pygame.event.pump()
        #print("Throttle to 0 to start!")
        while self.gamepad.getThrottle()!=0:
            pygame.event.pump()
        for m in self.motors:
            m.start()
        self.started = True
        self.gui.win_message.clear()
        self.gui.win_message.refresh()
        
        #print("STARTED!!!")
    
    def stop_motors(self):
        for m in self.motors:
            m.stop()
        self.started = False
        #print("STOPPED!!!")
        
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
        
    def guiSetup(self):
        self.screen = curses.initscr()
        self.dimensions = self.screen.getmaxyx()
        curses.start_color()
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        
        # Fenster und Hintergrundfarben
        self.screen.bkgd(curses.color_pair(1))
        self.screen.addstr(0,1,"==============", curses.A_BOLD)
        self.screen.addstr(1,1,"PiCopter - TUI", curses.A_BOLD)
        self.screen.addstr(2,1,"==============", curses.A_BOLD)
        self.screen.refresh()
        
        self.win_fps = curses.newwin(3, 4, 0, self.dimensions[1]-6)
        self.win_fps.box()
        
        
        self.win_m1 = curses.newwin(3, 6, 4, 2)
        self.win_m2 = curses.newwin(3, 6, 4, 10)
        self.win_m3 = curses.newwin(3, 6, 8, 10)
        self.win_m4 = curses.newwin(3, 6, 8, 2)
        
        self.win_motors = [self.win_m1, self.win_m2, self.win_m3, self.win_m4]
        
        self.win_isStart = curses.newwin(3,14, 3, 50)
        self.win_isStart.addstr(1,4, "Start")
        self.win_isHoldHeight = curses.newwin(3,14, 7, 50)
        self.win_isHoldHeight.addstr(1,2, "HoldHeight")
        self.win_isHoldPosition = curses.newwin(3,14, 11, 50)
        self.win_isHoldPosition.addstr(1,1, "HoldPosition")
        self.win_isAccel = curses.newwin(3,14, 15, 50)
        self.win_isAccel.addstr(1,4, "Accel")
        
        
        self.win_bools = [self.win_isStart, self.win_isHoldHeight, self.win_isHoldPosition, self.win_isAccel]
        
        self.windows = [[self.win_fps], self.win_motors, self.win_bools]
        
        for w in self.windows:
            for i in w:
                i.box()
                i.bkgd(curses.color_pair(1))
        
    def guiTick(self, fps):
        self.win_fps.addstr(1, 1, str(int(fps)))
        
        for m in range(4):
            self.win_motors[m].addstr(1,1, "    ")
            string = str(self.throttle[m])+"%"
            self.win_motors[m].addstr(1,5-len(string), string)
        
        if self.gamepad.isStart:
            self.win_isStart.bkgd(curses.color_pair(2))
        else:
            self.win_isStart.bkgd(curses.color_pair(3))
            
        if self.gamepad.isHoldHeight:
            self.win_isHoldHeight.bkgd(curses.color_pair(2))
        else:
            self.win_isHoldHeight.bkgd(curses.color_pair(3))
            
        if self.gamepad.isHoldPosition:
            self.win_isHoldPosition.bkgd(curses.color_pair(2))
        else:
            self.win_isHoldPosition.bkgd(curses.color_pair(3))
            
        if self.gamepad.isAccel:
            self.win_isAccel.bkgd(curses.color_pair(2))
        else:
            self.win_isAccel.bkgd(curses.color_pair(3))
        
        for w in self.windows:
            for i in w:
                i.refresh()
        
        
    def loop(self):
        while self.run:
            self.clock.tick(120)
            
            if self.DEBUG:
                self.gui.guiTick(self.clock.get_fps(), self.throttle, self.gamepad.isStart, self.gamepad.isHoldHeight, self.gamepad.isHoldPosition, self.gamepad.isAccel)
            pygame.event.pump()
            self.eventHandler()
            if self.gamepad.isStart:
                #print("started")
                if not self.started:
                    self.start_motors()
                self.changeMotorSpeed()
            else:
                #print("notStarted")
                self.gui.win_message.addstr(0, 0, "Press 'start'-Button to start!", curses.A_BLINK)
                self.gui.win_message.refresh()
                if self.started:
                    self.stop_motors()


if len(sys.argv) > 1:
    if sys.argv[1] == "--debug":
        go = Main(True)
else:
    go = Main()
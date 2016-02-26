#!/usr/bin/env python3
# coding: utf-8

##########################################
# MAIN.py - Hauptklasse
##########################################

from gamepad import Gamepad
from motor import Motor
from gui import Gui

from pygame.locals import *
import sys, os, time, pygame, curses, getopt

class Main():
    def __init__(self, GUI, DEBUG, fps, stick_sens, saveFile):
        self.GUI = GUI
        self.DEBUG = DEBUG
        self.max_fps = fps
        self.stick_sens = stick_sens
        self.saveFile = saveFile
        
        pygame.init()
        
        self.clock = pygame.time.Clock()
    
        self.run = True
        self.started = False
    
        self.main_throttle = 0
        self.throttle = [0,0,0,0]

        self.holdPosition = 0
        self.holdHeight = 0
        self.isGamepad = 1
        
        self.gamepad = Gamepad()
        self.gamepad_axes = [0,0,0]
        self.gamepad_throttle = 0
        
        self.bno = BNO()
        
        self.m1 = Motor(15)
        self.m2 = Motor(27)
        self.m3 = Motor(10)
        self.m4 = Motor(7)
        
        self.motors = [self.m1, self.m2, self.m3, self.m4]
        
        if self.GUI:
            self.gui = Gui()
        
        if self.GUI:
            self.gui.showMessage("Press 'start'-Button to start!")
        
        if self.DEBUG:
            # Print system status and self test result.
            status, self_test, error = self.bno.get_system_status()
            print("DEBUG: System status: {0}".format(status))
            print("DEBUG: Self test result (0x0F is normal): 0x{0:02X}".format(self_test))
            # Print out an error if system status is in error mode.
            if status == 0x01:
                print("DEBUG: System error: {0}".format(error))
                print("DEBUG: See datasheet section 4.3.59 for the meaning.")
            
            # Print BNO055 software revision and other diagnostic data.
            sw, bl, accel, mag, gyro = self.bno.get_revision()
            print("DEBUG: Software version:   {0}".format(sw))
            print("DEBUG: Bootloader version: {0}".format(bl))
            print("DEBUG: Accelerometer ID:   0x{0:02X}".format(accel))
            print("DEBUG: Magnetometer ID:    0x{0:02X}".format(mag))
            print("DEBUG: Gyroscope ID:       0x{0:02X}\n".format(gyro))
            
        self.load()
        
        if self.DEBUG:
            print("DEBUG: READY!")
        
        self.loop()
        
    def eventHandler(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                if self.DEBUG:
                    print("DEBUG: SHUTDOWN")
                pygame.quit()
                if self.GUI:
                    curses.endwin()
                sys.exit()
            elif event.type == JOYBUTTONDOWN:
                self.gamepad.handleButtonDown(event.button)
            elif event.type == JOYBUTTONUP:
                self.gamepad.handleButtonUp(event.button)
        
    def getGamepadValues(self):
        self.gamepad_throttle = self.gamepad.getThrottle()
        self.gamepad_axes = self.gamepad.getAxis()
        
        
    def checkCalibButtons(self):
        if self.gamepad.isSave:
            if self.DEBUG:
                print("DEBUG: Save Calibration-Data")
            self.save()
            if self.DEBUG:
                print("DEBUG: Data saved")
        
        if self.gamepad.isCalib:
            if self.DEBUG:
                print("DEBUG: calibrate BNO")
            
            self.bno.calibrateBNO()
            
            if self.DEBUG:
                print("DEBUG: new offset: {0}".format(self.bno.offset))
        
    def save(self):
        if self.DEBUG:
            print("DEBUG: Open File: "+self.saveFile)
        f = open(os.path.abspath(self.saveFile), "w")
        f.write(str(self.bno.offset))
        f.write("\n")
        f.write(str(self.gamepad.offset))
        f.close()
        self.gamepad.isSave = False
        
    def load(self):
        if self.DEBUG:
            print("DEBUG: Open File: "+self.saveFile)
        try:
            f = open(os.path.abspath(self.saveFile), "r")
        except IOError:
            if self.DEBUG:
                print("DEBUG: No SaveFile - Nothing to load")
            return
        
        if self.DEBUG:
            print("DEBUG: Loading...")
        
        loaded = f.read().replace(" ", "").split("\n")
        loaded = [loaded[0][1:-1].split(","), loaded[1][1:-1].split(",")]
        
        self.bno.offset = [float(loaded[0][0]), float(loaded[0][1]), float(loaded[0][2])]
        self.gamepad.offset = [float(loaded[1][0]), float(loaded[1][1]), float(loaded[1][2])]
        
        if self.DEBUG:
            print("Loaded! - bno-offset: {0} - gamepad-offset: {1}".format(self.bno.offset, self.gamepad.offset))
        
        f.close()
        
    def start_motors(self):
        if self.DEBUG:
            print("DEBUG: Calibrate Throttle!")
            
        if self.GUI:
            self.gui.hideMessage()
            self.gui.showMessage("Calibrate Throttle!")
        
        while self.gamepad.getThrottle()<=50:
            pygame.event.pump()
        
        while self.gamepad.getThrottle()!=0:
            pygame.event.pump()
        
        if self.DEBUG:
            print("DEBUG: Initializing motors")
            
        for m in self.motors:
            m.start()
        
        self.started = True
        
        if self.DEBUG:
            print("DEBUG: STARTED!")
        
        if self.GUI:
            self.gui.hideMessage()
    
    def stop_motors(self):
        if self.DEBUG:
            print("DEBUG: stopping motors")
            
        for m in self.motors:
            m.stop()
        
        self.started = False
        
        if self.DEBUG:
            print("DEBUG: STOPPED!")
            print("DEBUG: READY!")
            
        if self.GUI:
            self.gui.showMessage("Press 'start'-Button to start!")
        
    def changeMotorSpeed(self):
        self.throttle = [0,0,0,0]
        self.getGamepadValues()
        
        self.bno.tick()
        
        if (self.gamepad.isBNO):
            if self.DEBUG:
                print('DEBUG: Heading={0:0.2F} Roll={1:0.2F} Pitch={2:0.2F}'.format(self.bno.heading, self.bno.roll, self.bno.pitch))
            pitch = self.bno.pitch
            roll = self.bno.roll
            
            if pitch > 10:
                pitch = 10
            elif pitch < -10:
                pitch = -10
            if roll > 10:
                roll = 10
            elif roll < -10:
                roll = -10
                
            self.throttle[0] += pitch-roll
            self.throttle[1] += pitch+roll
            self.throttle[2] += -pitch+roll
            self.throttle[3] += -pitch-roll

        #Pad-Motor-Steuerung
        self.throttle[0] += -self.gamepad_axes[0]*self.stick_sens+self.gamepad.offset[0] + self.gamepad_axes[1]*self.stick_sens+self.gamepad.offset[1] - self.gamepad.offset[2]
        self.throttle[1] += -self.gamepad_axes[0]*self.stick_sens+self.gamepad.offset[0] - self.gamepad_axes[1]*self.stick_sens-self.gamepad.offset[1] + self.gamepad.offset[2]
        self.throttle[2] += +self.gamepad_axes[0]*self.stick_sens-self.gamepad.offset[0] - self.gamepad_axes[1]*self.stick_sens-self.gamepad.offset[1] - self.gamepad.offset[2]
        self.throttle[3] += +self.gamepad_axes[0]*self.stick_sens-self.gamepad.offset[0] + self.gamepad_axes[1]*self.stick_sens+self.gamepad.offset[1] + self.gamepad.offset[2]
        
        self.throttle = [int(self.gamepad_throttle+self.throttle[i]) for i in range(4)]
        
        for i in range(4):
            if self.throttle[i] > 100:
                self.throttle[i] = 100
            elif self.throttle[i] < 0:
                self.throttle[i] = 0
            self.motors[i].setW(self.throttle[i])
            
    def loop(self):
        while self.run:
            self.clock.tick(self.max_fps)
            
            pygame.event.pump()
            self.eventHandler()
            
            if self.GUI:
                self.gui.guiTick(self.clock.get_fps(), self.throttle, self.gamepad.isStart, self.gamepad.isBNO, [self.bno.heading, self.bno.pitch, self.bno.roll])
            
            if self.gamepad.isStart:
                if not self.started:
                    self.start_motors()
                self.changeMotorSpeed()
            else:
                self.checkCalibButtons()
                if self.started:
                    self.stop_motors()
                    

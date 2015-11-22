import curses


class Gui():
    def __init__(self):
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
        
        self.win_message = curses.newwin(1, 32, 1, 24)
        self.win_message.bkgd(curses.color_pair(1))
        
        self.win_bools = [self.win_isStart, self.win_isHoldHeight, self.win_isHoldPosition, self.win_isAccel]
        
        self.windows = [[self.win_fps], self.win_motors, self.win_bools]
        
        for w in self.windows:
            for i in w:
                i.box()
                i.bkgd(curses.color_pair(1))
                
    def showMessage(self, message):
        self.win_message.addstr(0, 0, str(message), curses.A_BLINK)
        self.win_message.refresh()
        
    def hideMessage(self):
        self.win_message.clear()
        self.win_message.refresh()
    
    def guiTick(self, fps, throttle, isStart, isHoldHeight, isHoldPosition, isAccel):
        self.win_fps.addstr(1, 1, str(int(fps)))
        
        for m in range(4):
            self.win_motors[m].addstr(1,1, "    ")
            string = str(throttle[m])+"%"
            self.win_motors[m].addstr(1,5-len(string), string)
        
        if isStart:
            self.win_isStart.bkgd(curses.color_pair(2))
        else:
            self.win_isStart.bkgd(curses.color_pair(3))
            
        if isHoldHeight:
            self.win_isHoldHeight.bkgd(curses.color_pair(2))
        else:
            self.win_isHoldHeight.bkgd(curses.color_pair(3))
            
        if isHoldPosition:
            self.win_isHoldPosition.bkgd(curses.color_pair(2))
        else:
            self.win_isHoldPosition.bkgd(curses.color_pair(3))
            
        if isAccel:
            self.win_isAccel.bkgd(curses.color_pair(2))
        else:
            self.win_isAccel.bkgd(curses.color_pair(3))
        
        for w in self.windows:
            for i in w:
                i.refresh()
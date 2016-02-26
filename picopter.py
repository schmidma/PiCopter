#!/usr/bin/env python3
# coding: utf-8

import getopt, sys

if __name__ == "__main__":
    fps = 120
    debug = False
    gui = False
    stick_sens = 5
    saveFile = "data.sav"
    
    parameter = getopt.getopt(sys.argv[1:], "", ["gui", "debug", "fps=", "stick-sens=", "saveFile="])
    
    for opt, arg in parameter[0]:
        if opt == "--debug":
            debug = True
        elif opt == "--gui":
            gui = True
        elif opt == "--fps":
            fps = arg
        elif opt == "--stick-sens":
            stick_sens = arg
        elif opt == "--saveFile":
            saveFile = arg
        
    if debug:
        print("DEBUG: Parameter: gui={0} debug={1} fps={2} stick-sens={3} saveFile={4}".format(gui, debug, fps, stick_sens, saveFile))
        
    if debug and gui:
        print("Can't use DEBUG and GUI at same time!")
        
    else:
        if debug:
            print("DEBUG: Importing...")
        
        from main import Main
        
        if debug:
            print("DEBUG: Initializing Main...")
        
        MAIN = Main(gui, debug, float(fps), float(stick_sens), saveFile)
    
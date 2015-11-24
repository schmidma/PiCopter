#!/usr/bin/env python3
# coding: utf-8

from main import Main

if __name__ == "__main__":
    fps = 120
    debug = False
    stick_sens = 5
    
    parameter = getopt.getopt(sys.argv[1:], "", ["debug", "fps=", "stick-sens="])
    
    for opt, arg in parameter:
        if opt == "--debug":
            debug = True
        elif opt == "--fps":
            fps = arg
        elif opt == "--stick-sens":
            stick_sens = 5
    
    MAIN = Main(debug, fps, stick_sens)
    
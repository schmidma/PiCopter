#!/usr/bin/env python3
# coding: utf-8

from main import Main
import getopt, sys

if __name__ == "__main__":
    fps = 120
    debug = False
    stick_sens = 5
    
    parameter = getopt.getopt(sys.argv[1:], "", ["debug", "fps=", "stick-sens="])
    
    print (parameter[0])
    for opt, arg in parameter[0]:
        if opt == "--debug":
            debug = True
        elif opt == "--fps":
            fps = arg
        elif opt == "--stick-sens":
            stick_sens = 5
    
    MAIN = Main(debug, float(fps), float(stick_sens))
    
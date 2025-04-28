# USE BUTTON 6 TO CONFIRM HOMING AND HATS FOR MOVEMENT
import os
import pygame as p
import serial
from src.config import *

class controller:
    def __init__(self, debug=False):
        #use dummy video driver
        os.environ["SDL_VIDEODRIVER"] = "dummy"

        self.p = p.init()
        p.joystick.init()
        self.joysticks = p.joystick.get_count()

        if self.joysticks == 0 and debug:
            print("\ncontroller: no joysticks detected")
        else:
            self.myController = p.joystick.Joystick(0)
            self.myController.init()
            if debug:
                print("\ncontroller: controller found and initialized")
    
    def findGantryInput(self, debug=False):
        p.event.pump()
        gantryDir = self.myController.get_hat(MOVEMENT_INPUT)

        command = None

        if gantryDir[0] == -1:
            command = "L"
        elif gantryDir[0] == 1:
            command = "R"
        elif gantryDir[1] == -1:
            command = "D"
        elif gantryDir[1] == 1:
            command = "U"

        if self.myController.get_button(6) == 1:
            if debug:
                print("Exiting Manual Mode")
            quit()

        return command

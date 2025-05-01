# USE BUTTON 6 TO CONFIRM HOMING AND HATS FOR MOVEMENT
# NEEDS DOCSTRINGS
import os
import pygame as p
from src.config import *

class controller:
    def __init__(self, debug=False):
        """Create a controller object that reads off of a USB game controller for manual mode and calibration
        
            ### Args:
                debug (bool): Enter debug mode

            ### Returns:
                None
        
        """
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
        """Using the hat control on the remote, check for movement in manual mode. Also check to see if program terminated
        
            ### Args:
                debug (bool): Enter debug mode

            ### Returns:
                command (str): translated command based on input. Want more commands? Add more interpretations to this function
                terminatorCheck (int): input from button 6. Currently used to exit manual mode
        
        """

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

        terminatorCheck = self.myController.get_button(6)

        return command, terminatorCheck

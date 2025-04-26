# Sample test for purposes of isolating Hat 1 movement in controller for manual homing / movement
# USE BUTTON 6 TO CONFIRM HOMING AND HATS FOR MOVEMENT
import os
import pygame as p
from src.vision.config import DEBUG

#use dummy video driver
os.environ["SDL_VIDEODRIVER"] = "dummy"

p.init()
p.joystick.init()
joysticks = p.joystick.get_count()

if joysticks == 0 and DEBUG:
    print("\ncontrollerInput: no joysticks detected")

else:
    # Use joystick #0 and initialize it
    myController = p.joystick.Joystick(0)
    myController.init()

while joysticks != 0:
    p.event.pump()
    move = myController.get_hat(0)
    print(move)

    quitProgram = myController.get_button(6)
    if quitProgram == 1:
        quit()

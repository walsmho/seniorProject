# USE BUTTON 6 TO CONFIRM HOMING AND HATS FOR MOVEMENT
import os
import pygame as p
import serial
from src.config import *

#use dummy video driver
os.environ["SDL_VIDEODRIVER"] = "dummy"

serialComm = serial.Serial('COM7', 9600) #Com subject to change right now 
serialComm.timeout = 1

p.init()
p.joystick.init()
joysticks = p.joystick.get_count()

if joysticks == 0 and DEBUG:
    print("\nbasicCommands: no joysticks detected")
    quit()

else:
    # Use joystick #0 and initialize it
    myController = p.joystick.Joystick(0)
    myController.init()

while MANUAL:
    p.event.pump()
    #Gantrydir is a tuple
    command = None
    gantryDir = myController.get_hat(0)
    if gantryDir[0] == -1:
        print("MOVE LEFT")
        command = "L"
    elif gantryDir[0] == 1:
        print("MOVE RIGHT")
        command = "R"
    elif gantryDir[1] == -1:
        print("MOVE DOWN")
        command = "D"
    elif gantryDir[1] == 1:
        print("MOVE UP")
        command = "U"

    if command is not None:
        serialComm.write(command.encode())
        print(f"Sent command: {command}")

    if serialComm.in_waiting > 0:
        print(serialComm.read(serialComm.in_waiting).decode())

    quitProgram = myController.get_button(6)
    if quitProgram == 1:
        if DEBUG:
            print("\nbasicCommands: exiting manual mode")
        command = "Q"
        serialComm.write(str(command).encode())
        MANUAL = False

while not MANUAL:
    if DEBUG:
        print("\nAutomonous mode now entered")
    quit()

from src.config import *
from src.motorControl.controller import controller
from src.comms.bridge import communicator

def main():
    # If ! calibrated, calibrate
    # Begin vision loop
    # Respond accordingly
    joystick = controller()
    bridge = communicator()

    while MANUAL:
        command = joystick.findGantryInput(DEBUG)
        bridge.issueCommand(command, DEBUG)
        arduinoResponse = bridge.receiveMessage(DEBUG)
        if arduinoResponse is not None:
            print(arduinoResponse)

if __name__ == "__main__":
    main()
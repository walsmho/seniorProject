from src.config import *
from src.motorControl.controller import controller
from src.motorControl.homing import homingSequence
from src.comms.bridge import communicator

def main():
    # If ! calibrated, calibrate
    # Begin vision loop
    # Respond accordingly
    joystick = controller()
    bridge = communicator()

    robotCoords = homingSequence(joystick, bridge, DEBUG)

if __name__ == "__main__":
    main()

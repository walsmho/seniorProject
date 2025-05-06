from src.config import *
from src.motorControl.controller import controller
from src.motorControl.robotPaddle import paddle
from src.comms.bridge import communicator

def main():
    # If ! calibrated, calibrate
    # Begin vision loop
    # Respond accordingly
    joystick = controller()
    bridge = communicator()
    roboPaddle = paddle()
    
    
    roboPaddle.homingSequence(joystick, bridge, DEBUG)

    for _ in range(5):
        roboPaddle.getUserCoords()
        roboPaddle.gotoBresenham(bridge, DEBUG) #Big problemo - entire code stops here as it issues commands to get to coordinate
        roboPaddle.update()

if __name__ == "__main__":
    main()

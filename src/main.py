from src.config import *
from src.motorControl.controller import controller
#from src.motorControl.homing import homingSequence
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
        roboPaddle.gotoLinear(bridge, DEBUG)
        roboPaddle.update()

if __name__ == "__main__":
    main()

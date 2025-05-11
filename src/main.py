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

    for i in range(10):
        roboPaddle.getUserCoords()
        roboPaddle.giveArduinoCoords(bridge, DEBUG)
        bridge.findMessage()
        roboPaddle.update()
        print(f"Succesful coordinate update, iteration {i+1}")

if __name__ == "__main__":
    main()

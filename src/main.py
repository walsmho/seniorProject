from src.config import *
from src.motorControl.controller import controller
from src.motorControl.robotPaddle import paddle
from src.comms.bridge import communicator
from src.vision.visionUtil import pixelToStep

def main():
    # If ! calibrated, calibrate
    # Begin vision loop
    # Respond accordingly
    joystick = controller()
    bridge = communicator()
    roboPaddle = paddle()

    roboPaddle.homingSequence(joystick, bridge, DEBUG)
    stepCoords = pixelToStep([400,65]) # Coords (370 < x < 640) and (0 < y < 360) will be the only valid inputs

    roboPaddle.goto(bridge, stepCoords, DEBUG)
    bridge.waitForMessage()
    roboPaddle.update()

if __name__ == "__main__":
    main()

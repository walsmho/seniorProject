from src.config import *
from src.motorControl.controller import controller
from src.motorControl.robotPaddle import paddle
from src.comms.bridge import communicator
from src.vision.visionUtil import pixelToStep
from src.vision.visionSystem import overheadVision

def main():
    # If ! calibrated, calibrate
    # Begin vision loop
    # Respond accordingly
    joystick = controller()
    bridge = communicator()
    roboPaddle = paddle()
    camera = overheadVision()

    roboPaddle.homingSequence(joystick, bridge, DEBUG)
    running = True
    while running:
        camera.processFrame()
        camera.visualizeFrame()

        # #stepCoords = pixelToStep([400,65]) # Coords (370 < x < 640) and (0 < y < 360) will be the only valid inputs
        # roboPaddle.goto(bridge, [0, 0], DEBUG)
        # bridge.waitForMessage()
        # roboPaddle.update()

        running = camera.checkStatus()

if __name__ == "__main__":
    main()

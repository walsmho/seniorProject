from src.config import *
from src.motorControl.controller import controller
from src.motorControl.robotPaddle import paddle
from src.comms.bridge import communicator
from src.vision.visionUtil import pixelToStep
from src.vision.visionSystem import overheadVision

def main():
    joystick = controller()
    bridge = communicator()
    roboPaddle = paddle()
    camera = overheadVision()

    roboPaddle.homingSequence(joystick, bridge)

    # #Delete this after done with ramp tests
    # for _ in range(5):
    #     roboPaddle.getUserCoords()
    #     roboPaddle.goto(bridge)
    #     roboPaddle.update()

    roboPaddle.goto(bridge, [500,500])
    print("GOTO complete")
    roboPaddle.update()
    
    running = True
    while running:
        puckChanges = camera.processFrame()
        camera.visualizeFrame()
        status, response = roboPaddle.statusCheck(puckChanges)
        #If status = 0, no change
        if status == 1:
            stepCoords = pixelToStep(response)
            roboPaddle.goto(bridge, stepCoords)
    
        elif status == 2:
            stepCoords = pixelToStep(response)
            roboPaddle.goto(bridge, stepCoords)
            roboPaddle.update()

        roboPaddle.update()
        running = camera.checkStatus()

if __name__ == "__main__":
    main()

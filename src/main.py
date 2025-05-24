from src.config import *
from src.motorControl.controller import controller
from src.motorControl.robotPaddle import paddle
from src.comms.bridge import communicator
from src.vision.visionUtil import pixelToStep, stepToPixel
from src.vision.visionSystem import overheadVision

def main():
    joystick = controller()
    bridge = communicator()
    roboPaddle = paddle()
    camera = overheadVision()

    roboPaddle.homingSequence(joystick, bridge)

    running = True
    while running:
        puckChanges = camera.processFrame()
        # print(puckChanges)
        camera.visualizeFrame()
        status, response = roboPaddle.statusCheck(puckChanges)
        
        if status == 0: #0 = home
            roboPaddle.goto(bridge, [0, 0])

        elif status == 1: #1 = puck on robo side, hit
            stepCoords = pixelToStep(response)
            roboPaddle.goto(bridge, stepCoords)
        
        elif status == 9: #9 = do nothing
            pass

        roboPaddle.update()
        running = camera.checkStatus()

if __name__ == "__main__":
    main()

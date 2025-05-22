### CLASS VERSION OF detectPuck.py file
import cv2
from src.vision.visionUtil import getLimits, createMask, createBoundingBox, beginVideoCapture
from src.vision.puck import puckObject
from src.config import *
import numpy as np

class overheadVision:
    def __init__(self, camIndex = WEBCAM, debug=False):
        self.capture = beginVideoCapture(WEBCAM)
        self.puck = puckObject()
        self.captureHeight = None
        self.captureWidth = None

    def processFrame(self, debug=False):
        ret, view = self.capture.read()
        self.view = view

        if not ret and debug:
            print("\nvisionSystem.processFrame error: Can't recieve frame. (steam end?) exiting...")
            return None
        
        self.view = cv2.pyrDown(self.view)
        self.captureHeight, self.captureWidth = self.view.shape[:2]
        lowerLimit, upperLimit = getLimits(PUCK_COLOR, debug)
        colorMaskPuck = createMask(self.view, lowerLimit, upperLimit, PUCK_MASK, debug)

        boundingInitial = colorMaskPuck.getbbox()

        if boundingInitial is not None:
            newCoordBottom, newCoordTop = createBoundingBox(self.view, colorMaskPuck, debug=DEBUG)

            centerCoord = (((newCoordBottom[0] + newCoordTop[0]) / 2), ((newCoordBottom[1] + newCoordTop[1]) / 2))
            #print(centerCoord)
            moved, direction, speed = self.puck.currentVector(centerCoord, FPS, debug)
            if moved:
                lineStart, lineEnd, danger = self.puck.reboundPrediction(self.view, self.captureHeight, self.captureWidth, centerCoord, direction, speed, (0, 255, 0), 3, debug)
                if DEBUG:
                    print(f"\noverheadVision.processFrame: Puck heading to {lineEnd} at {speed} pixels / second")

            else:
                if DEBUG:
                    print(f"\noverheadVision.processFrame: no significant movement detected")
                return [False]

            self.puck.update(newCoordBottom, newCoordTop, debug)
            return [moved, direction, speed, centerCoord, lineEnd, danger]

        elif boundingInitial is None:
            if debug:
                print("\nvisionSystem.processFrame: WARNING: No puck exists in frame")
                return [False]
            
        return [False]

    def visualizeFrame(self, debug=False):
        #Draw Goals
        cv2.rectangle(self.view, ROBOGOAL[0], ROBOGOAL[1], BOUNDARY_COLOR, 3)

        #Draw puck
        cv2.imshow(FRAME_NAME, self.view)

    def checkStatus(self):
        if cv2.waitKey(1) & 0xFF == ord('q'):
            runStatus = False
            self.capture.release()
            cv2.destroyAllWindows()
            return runStatus
        return True
    
import numpy as np
import cv2
from PIL import Image

class puckObject:
    def __init__(self, coordBottom=(0,0), coordTop=(0,0)):
        self.coordBottom = coordBottom
        self.coordTop = coordTop

    def update(self, newCoord1, newCoord2):
        self.coordBottom = newCoord1
        self.coordTop = newCoord2

    def hasMoved(self, coordNew, tolerance, debug=True):
        #USES bottom left coord (coordBottom)
        #Check x-axis coords
        if np.abs(self.coordBottom[0]-coordNew[0]) > tolerance:
            movedX = True

            if self.coordBottom > coordNew:
                if debug:
                    print("objMoved: Moved Left")
                trajectoryX = "left"
            elif self.coordBottom < coordNew:
                if debug:
                    print("objMoved: Moved Right")
                trajectoryX = "right"

        elif np.abs(self.coordBottom[0]-coordNew[0] <= tolerance):
            if debug:
                print("objMoved: No x-axis movement")
            movedX = False
            trajectoryX = None

        #Check y-axis coords
        if np.abs(self.coordBottom[1]-coordNew[1]) > tolerance:
            movedY = True

            if self.coordBottom > coordNew:
                if debug:
                    print("objMoved: Moved Up")
                trajectoryY = "up"
            elif self.coordBottom < coordNew:
                if debug:
                    print("objMoved: Moved Down")
                trajectoryY = "down"

        elif np.abs(self.coordBottom[1]-coordNew[1] <= tolerance):
            if debug:
                print("objMoved: No y-axis movement")
            movedY = False
            trajectoryY = None

        else:
            movedX = False
            movedY = False
            trajectoryX = None
            trajectoryY = None
        
        return movedX, movedY, trajectoryX, trajectoryY

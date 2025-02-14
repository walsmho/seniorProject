import numpy as np
import cv2
from PIL import Image

class puckObject:
    def __init__(self, coordBottom=(0,0), coordTop=(0,0)):
        self.coordBottom = coordBottom
        self.coordTop = coordTop

    def update(self, newCoord1, newCoord2, debug=False):
        """Update self coords used in boundingbox to new position
        
            ### Args:
                newCoord1 (tuple): bottom left box coordinate
                newCoord2 (tuple): top right box coordinate
                debug (bool): enter debug mode

            ### Returns:
                None

        """

        self.coordBottom = newCoord1
        self.coordTop = newCoord2
        if debug:
            print("\npuck.update: Succesful coordinate update")

    def hasMoved(self, coordNew, tolerance, debug=False):
        """Uses the bottom left coordinate provided and a tolerance to determine if object has changed position
        
            ### Args:
                coordNew (tuple): new coordinate to compare with self coord
                tolerance (int): Number for +- pixels to account for noise
                debug (bool): enter debug mode

            ### Returns:
                movedX, trajectoryX
        
        """

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

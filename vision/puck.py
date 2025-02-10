import numpy as np
import cv2
from PIL import Image

class puckObject:
    def __init__(self, view, mask, debug=False):
        self.view = view
        self.mask = mask
        self.debug = debug

        boundingInitial = mask.getbbox()

        if boundingInitial is not None:
            if debug:
                print("bounding succesful")

        else:
            return None

    
    def createBoundingBox(camera, colorMask, boundingBoxThickness=3, debug=False):
        """Create a rectangle around input colorMask
        
            Args:
                view (cv object): Camera view
                colorMask (PIL object): PIL image with desired color
                boundingBoxColor (tuple): BRG value of bbox color
                boundingBoxThickness (int): pixel width of bbox
                debug (bool): Enter deubg mode

            Returns:
                x1, y1 (tuple): first corner of bbox coords
                x2, y2 (tuple): oppositi corner of bbox coords
        
        """

        boundingBox = colorMask.getbbox()
        if debug and boundingBox is not None:
            print("createBoundingBox: boundingBox coordinates {}".format(boundingBox))
        if boundingBox is not None:
            x1, y1, x2, y2 = boundingBox
            cv2.rectangle(camera, (x1, y1), (x2, y2), colorMask, boundingBoxThickness)
        elif boundingBox == None:
            x1, y1, x2, y2 = None

        if x1 is not None:
            return (x1, y1), (x2, y2)
        else:
            return None
        
    def puckMoved(coordPrev, coordNew, tolerance, debug=False):
        """Check to see if object in bounding box moved and where, given some tolerance

            Args:
                coordPrev (tuple): Previous coordinate set from last frame
                coordNew (tuple): Current coordinate set from existing frame
                tolerance (int): Tolerance of pixels for movement
                debug (bool): Enter debug mode

            Returns:
                moved (bool): Whether object moved or not
                trajectoryX (string): If moved, vector of direction. Else, returns none. Currently returning a string of "left, right" for testing
                trajectoryY (string): If moved, vector of direction. Else, returns none. Currently returning a string of "up, down" for testing
        
        """
        #Check x-axis coords
        if np.abs(coordPrev[0]-coordNew[0]) > tolerance:
            movedX = True

            if coordPrev > coordNew:
                if debug:
                    print("objMoved: Moved Left")
                trajectoryX = "left"
            elif coordPrev < coordNew:
                if debug:
                    print("objMoved: Moved Right")
                trajectoryX = "right"

        elif np.abs(coordPrev[0]-coordNew[0] <= tolerance):
            if debug:
                print("objMoved: No x-axis movement")
            movedX = False
            trajectoryX = None

        #Check y-axis coords
        if np.abs(coordPrev[1]-coordNew[1]) > tolerance:
            movedY = True

            if coordPrev > coordNew:
                if debug:
                    print("objMoved: Moved Up")
                trajectoryY = "up"
            elif coordPrev < coordNew:
                if debug:
                    print("objMoved: Moved Down")
                trajectoryY = "down"

        elif np.abs(coordPrev[1]-coordNew[1] <= tolerance):
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

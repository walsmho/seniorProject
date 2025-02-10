import numpy as np
import cv2
from PIL import Image

def getLimits(color, debug=False):
    #Docstrings are being weird rn
    """Get upper and lower bounds of desired color for detection.

        Args:
            color (list): Desired color to get limits of
            debug (bool): Enter debug mode

        Returns:
            lowerLimit (np.array): lower bound for color
            upperLimit (np.array): upper bound for color

    """

    c = np.uint8([[color]]) #insert BGR values to convert to hsv
    hsvC = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)

    # Can experiment with adjusting limits if needed based on lighting
    lowerLimit = hsvC[0][0][0] - 10, 100, 100
    upperLimit = hsvC[0][0][0] + 10, 255, 255

    lowerLimit = np.array(lowerLimit, dtype=np.uint8)
    upperLimit = np.array(upperLimit, dtype=np.uint8)

    return lowerLimit, upperLimit

def createMask(view, lowerLimit, upperLimit, debug=False):
    """Create a mask for given color

        Args:
            view (cv object): Camera view
            lowerLimit (np.array): lower bound for color
            upperLimit (np.array): upper bound for color
            debug (bool): enter debug mode

        Returns:
            colorMaskP (PIL object): colorMask image in PIL format
    
    """
    hsvImage = cv2.cvtColor(view, cv2.COLOR_BGR2HSV)
    if debug:
        print("createMask: succesfully converted image to hsv")
    colorMask = cv2.inRange(hsvImage, lowerLimit, upperLimit)

    #Visualize mask
    if debug:
        cv2.imshow('mask', colorMask)

    #Convert colorMask to PIL format
    colorMaskP = Image.fromarray(colorMask)
    if debug:
        print("createMask: succesfully converted mask to PIL format")

    return colorMaskP

def createBoundingBox(view, colorMask, boundingBoxColor=(0,0,255), boundingBoxThickness=3, debug=False):
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
        cv2.rectangle(view, (x1, y1), (x2, y2), boundingBoxColor, boundingBoxThickness)
    elif boundingBox == None:
        x1, y1, x2, y2 = None

    if x1 is not None:
        return (x1, y1), (x2, y2)
    else:
        return None

def objMoved(coordPrev, coordNew, tolerance, debug=False):
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

import numpy as np
import cv2
from PIL import Image

def getLimits(color, debug=False):
    #Docstrings are being weird rn
    """Get upper and lower bounds of desired color for detection.

        ### Args:
            color (list): Desired color to get limits of
            debug (bool): Enter debug mode

        ### Returns:
            lowerLimit (np.array): Lower bound for color
            upperLimit (np.array): Upper bound for color

    """

    c = np.uint8([[color]]) #insert BGR values to convert to hsv
    hsvC = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)

    # Can experiment with adjusting limits if needed based on lighting
    lowerLimit = hsvC[0][0][0] - 10, 100, 100
    upperLimit = hsvC[0][0][0] + 10, 255, 255

    lowerLimit = np.array(lowerLimit, dtype=np.uint8)
    upperLimit = np.array(upperLimit, dtype=np.uint8)

    if debug:
        print(f"\ngetLimits: lowerLimit: {lowerLimit}")
        print(f"\ngetLimits: upperLimit: {upperLimit}")

    return lowerLimit, upperLimit

def createMask(view, lowerLimit, upperLimit, debug=False):
    """Create a mask for given color

        ### Args:
            view (cv object): Camera view
            lowerLimit (np.array): Lower bound for color
            upperLimit (np.array): Upper bound for color
            debug (bool): Enter debug mode

        ### Returns:
            colorMaskP (PIL object): colorMask image in PIL format
    
    """

    hsvImage = cv2.cvtColor(view, cv2.COLOR_BGR2HSV)
    if debug:
        print("\ncreateMask: succesfully converted image to hsv")
    colorMask = cv2.inRange(hsvImage, lowerLimit, upperLimit)

    #Visualize mask
    if debug:
        cv2.imshow('mask', colorMask)

    #Convert colorMask to PIL format
    colorMaskP = Image.fromarray(colorMask)
    if debug:
        print("\ncreateMask: succesfully converted mask to PIL format")

    return colorMaskP

def createBoundingBox(view, colorMask, boundingBoxColor=(0,0,255), boundingBoxThickness=3, debug=False):
    """Create a rectangle around input colorMask
    
        ### Args:
            view (cv object): Camera view
            colorMask (PIL object): PIL image with desired color
            boundingBoxColor (tuple): BRG value of bbox color
            boundingBoxThickness (int): Pixel width of bbox
            debug (bool): Enter deubg mode

        ### Returns:
            x1, y1 (tuple): First corner of bbox coords
            x2, y2 (tuple): Opposite corner of bbox coords
    
    """

    boundingBox = colorMask.getbbox()
    if debug and boundingBox is not None:
        print(f"\ncreateBoundingBox: boundingBox coordinates {boundingBox}")
    if boundingBox is not None:
        x1, y1, x2, y2 = boundingBox
        cv2.rectangle(view, (x1, y1), (x2, y2), boundingBoxColor, boundingBoxThickness)
    elif boundingBox == None:
        x1, y1, x2, y2 = None

    if x1 is not None:
        return (x1, y1), (x2, y2)
    else:
        return None

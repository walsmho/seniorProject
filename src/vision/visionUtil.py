import numpy as np
import cv2
from PIL import Image

def beginVideoCapture(webcam, debug=False):
    """Initiate video capture from cv.
    
        ### Args:
            webcam (int): Camera input. 0 for built-in, 1 for external
            debug (bool): Enter debug mode

        ### Returns:
            capture (cv2 object): Webcam object for further use

    """
    
    capture = cv2.VideoCapture(webcam, cv2.CAP_DSHOW)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    return capture

def getLimits(color, debug=False):
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

def createMask(view, lowerLimit, upperLimit, maskName, debug=False):
    """Create a mask for given color

        ### Args:
            view (cv object): Camera view
            lowerLimit (np.array): Lower bound for color
            upperLimit (np.array): Upper bound for color
            maskName (str): Name for mask window if debug is on
            debug (bool): Enter debug mode

        ### Returns:
            colorMaskP (PIL object): colorMask image in PIL format
    
    """

    hsvImage = cv2.cvtColor(view, cv2.COLOR_BGR2HSV)
    if debug:
        print("\ncreateMask: succesfully converted image to hsv")
    colorMask = cv2.inRange(hsvImage, lowerLimit, upperLimit)
    #Reduce effect of noisy lighting
    colorMask = cv2.GaussianBlur(colorMask, (5, 5), 0)

    #Remove specks and fill holes in puck
    kernel = np.ones((5, 5), np.uint8)
    colorMask = cv2.morphologyEx(colorMask, cv2.MORPH_OPEN, kernel)  # removes noise
    colorMask = cv2.morphologyEx(colorMask, cv2.MORPH_CLOSE, kernel) # fills holes

    #Visualize mask
    if debug:
        cv2.imshow(maskName, colorMask)

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

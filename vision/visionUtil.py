import numpy as np
import cv2

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


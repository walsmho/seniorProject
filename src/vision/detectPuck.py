### Must run file from bash as "py -m src.vision.detectPuck"

import cv2
from src.vision.visionUtil import getLimits, createMask, createBoundingBox, beginVideoCapture
#from src.comms.communicator import response
from src.vision.puck import puckObject
from src.vision.config import *

#Turn capture into its own class as well?
capture = beginVideoCapture(WEBCAM)

puck = puckObject()

while True:
    #Capture frame, create mask
    ret, view = capture.read()
    captureHeight, captureWidth = view.shape[:2]
    if not ret and DEBUG:
        print("detectPuck.py error: Can't recieve frame. (stream end?) exiting...")
        break
    lowerLimit, upperLimit = getLimits(PUCK_COLOR, DEBUG)
    colorMaskPuck = createMask(view, lowerLimit, upperLimit, PUCK_MASK, DEBUG)

    #check if object exists
    boundingInitial = colorMaskPuck.getbbox()

    #When seeing puck:
    if boundingInitial is not None:
        newCoordBottom, newCoordTop = createBoundingBox(view, colorMaskPuck, debug=DEBUG)

        centerCoord = (((newCoordBottom[0] + newCoordTop[0]) / 2), ((newCoordBottom[1] + newCoordTop[1]) / 2))
        moved, direction, speed = puck.currentVector(centerCoord, FPS, debug=DEBUG)

        #Draw prediction line
        if moved:
            lineStart, lineEnd = puck.reboundPrediction(view, captureHeight, captureWidth, centerCoord, direction, speed, debug=DEBUG)
            if DEBUG:
                print("\nPuck heading to {} at {} pixels / second".format(lineEnd, speed))

        #msg = response(moved, direction, speed)

        puck.update(newCoordBottom, newCoordTop, DEBUG)

    #When not seeing puck:
    elif boundingInitial is None:
        if DEBUG:
            print("\ndetectPuck.py WARNING: No puck exists in frame")

    #Visualize frame
    cv2.imshow(FRAME_NAME, view)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()

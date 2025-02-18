import cv2
from visionUtil import getLimits, createMask, createBoundingBox, beginVideoCapture
from puck import puckObject
from config import *

#Turn capture into its own class as well?
capture = beginVideoCapture(WEBCAM)

puck = puckObject()

while True:
    #Capture frame, create mask
    ret, view = capture.read()
    if not ret and DEBUG:
        print("detectPuck.py error: Can't recieve frame. (stream end?) exiting...")
        break
    lowerLimit, upperLimit = getLimits(PUCK_COLOR, DEBUG)
    lowerLimitRail, upperLimitRail = getLimits(BOUNDARY_COLOR, DEBUG)
    colorMaskPuck = createMask(view, lowerLimit, upperLimit, PUCK_MASK, DEBUG)
    colorMaskRails = createMask(view, lowerLimitRail, upperLimitRail, BOUNDARY_MASK, DEBUG)

    #check if object exists
    boundingInitial = colorMaskPuck.getbbox()

    #When seeing puck:
    if boundingInitial is not None:
        newCoordBottom, newCoordTop = createBoundingBox(view, colorMaskPuck, debug=DEBUG)

        centerCoord = (((newCoordBottom[0] + newCoordTop[0]) / 2), ((newCoordBottom[1] + newCoordTop[1]) / 2))
        moved, direction, speed = puck.currentVector(centerCoord, TOLERANCE, FPS, debug=DEBUG)

        if moved:
            lineStart, lineEnd = puck.linePrediction(view, centerCoord, direction, debug=DEBUG)
            if DEBUG:
                print("\nPuck heading to {} at {} pixels / second".format(lineEnd, speed))

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

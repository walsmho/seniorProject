import cv2
from visionUtil import getLimits, createMask, createBoundingBox
from puck import puckObject

capture = cv2.VideoCapture(0) # for external webcam hookup in setup

#Temp until permanent setting with good lighting exists
puckColor = [0,255,255] #BGR orange value
puck = puckObject()
debug = False

while True:
    #Capture frame, create mask
    ret, view = capture.read()
    if not ret and debug:
        print("detectPuck.py error: Can't recieve frame. (stream end?) exiting...")
        break
    lowerLimit, upperLimit = getLimits(puckColor, debug)
    colorMaskP = createMask(view, lowerLimit, upperLimit, debug)

    #check if object exists
    boundingInitial = colorMaskP.getbbox()

    #When seeing puck:
    if boundingInitial is not None:
        newCoordBottom, newCoordTop = createBoundingBox(view, colorMaskP, debug)

        centerCoord = (((newCoordBottom[0] + newCoordTop[0]) / 2), ((newCoordBottom[1] + newCoordTop[1]) / 2))
        moved, direction, speed = puck.currentVector(centerCoord, debug=debug)

        if moved:
            lineStart, lineEnd = puck.linePrediction(view, centerCoord, direction, debug=debug)
            if debug:
                print("\nPuck heading to {} at {} pixels / second".format(lineEnd, speed))

        puck.update(newCoordBottom, newCoordTop, debug)

    #When not seeing puck:
    elif boundingInitial is None:
        if debug:
            print("\ndetectPuck.py WARNING: No puck exists in frame")

    #Visualize frame
    cv2.imshow("Overhead Table View", view)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()

import cv2
from visionUtil import getLimits, createMask, createBoundingBox
from puck import puckObject

capture = cv2.VideoCapture(1) # for external webcam hookup in setup

#Temp until permanent setting with good lighting exists
puckColor = [0,255,255] #BGR orange value
puck = puckObject()
debug = True

while True:
    #Capture frame, create mask
    ret, view = capture.read()
    if not ret and debug:
        print("detectPuck error: Can't recieve frame. (stream end?) exiting...")
        break
    lowerLimit, upperLimit = getLimits(puckColor)
    colorMaskP = createMask(view, lowerLimit, upperLimit)

    #check if object exists
    boundingInitial = colorMaskP.getbbox()

    #When seeing puck:
    if boundingInitial is not None:
        newCoordBottom, newCoordTop = createBoundingBox(view, colorMaskP)
        centerCoord = ([(newCoordBottom[0]+newCoordTop[0])/2, (newCoordBottom[1]+newCoordTop[1]/2)])

        direction, speed = puck.currentVector(centerCoord, 1)

        print(f"Direction: {direction}")
        print(f"Speed: {speed}")

        puck.update(newCoordBottom, newCoordTop)

    #When not seeing puck:
    elif boundingInitial is None:
        if debug:
            print("WARNING: No puck exists in frame")

    #Visualize frame
    if debug:
        cv2.imshow('Camera View', view)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()

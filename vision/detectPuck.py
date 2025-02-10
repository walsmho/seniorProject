import cv2
from PIL import Image
from visionUtil import getLimits, createMask, createBoundingBox, objMoved

capture = cv2.VideoCapture(0) # for external webcam hookup in setup

#Temp until permanent setting with good lighting exists
puckColor = [0,165,255] #BGR orange value

(x1,y1), (x2,y2) = (0,0), (0,0)

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
        (x1_,y1_), (x2, y2) = createBoundingBox(view, colorMaskP)

        movedX, movedY, trajectoryX, trajectoryY = objMoved((x1,y1),(x1_,y1_), 20, debug)

    #When not seeing puck:
    elif boundingInitial is None:
        if debug:
            print("WARNING: No puck exists in frame")

    #Visualize frame
    if debug:
        cv2.imshow('Camera View', view)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    #Prev coord now = new coord
    (x1,y1) = (x1_,y1_)

capture.release()
cv2.destroyAllWindows()

import cv2
from PIL import Image
from visionUtil import getLimits

capture = cv2.VideoCapture(1) # for external webcam hookup in setup
puckColor = [0, 165, 255] # BGR. Using orange for testing
debug = True

while True:
    #Capture frame
    ret, view = capture.read()

    if not ret and debug:
        print("detectPuck error: Can't recieve frame. (stream end?) exiting...")
        break

    #Convert image and get limits
    hsvImage = cv2.cvtColor(view, cv2.COLOR_BGR2HSV)
    lowerLimit, upperLimit = getLimits(puckColor)

    colorMask = cv2.inRange(hsvImage, lowerLimit, upperLimit)
    #Convert colorMask to PIL format
    colorMaskP = Image.fromarray(colorMask)

    #Create bounding box
    boundingBox = colorMaskP.getbbox()
    if debug and boundingBox is not None:
        print("detectPuck: boundingBox coordinates {}".format(boundingBox))
    if boundingBox is not None:
        x1, y1, x2, y2 = boundingBox
        boundingBoxColor = (0, 0, 255)
        boundingBoxThickness = 3
        cv2.rectangle(view, (x1, y1), (x2, y2), boundingBoxColor, boundingBoxThickness)

    #Visualize frame
    if debug:
        cv2.imshow('Camera View', view)

    #Visualize mask
    if debug:
        cv2.imshow('mask', colorMask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()

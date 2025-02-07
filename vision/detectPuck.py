import cv2
from PIL import Image
from visionUtil import getLimits, createMask, createBoundingBox

capture = cv2.VideoCapture(1) # for external webcam hookup in setup
puckColor = [0, 165, 255] # BGR. Using orange for testing
debug = True

while True:
    #Capture frame
    ret, view = capture.read()

    if not ret and debug:
        print("detectPuck error: Can't recieve frame. (stream end?) exiting...")
        break

    lowerLimit, upperLimit = getLimits(puckColor)
    colorMaskP = createMask(view, lowerLimit, upperLimit)

    (x1,y1), (x2, y2) = createBoundingBox(view, colorMaskP)

    #Visualize frame
    if debug:
        cv2.imshow('Camera View', view)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()

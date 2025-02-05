import numpy as np
import cv2 as cv

debug = True

cap = cv.VideoCapture(0)
if not cap.isOpened() and debug:
    print("camera error: cannot open camera")
    exit()

while True:
    #Capture frames
    ret, frame = cap.read()

    #if frame is read correctly, ret = True
    if not ret:
        print("can't recieve frame (stream end?) exiting...")
        break

    gray = cv.cvtColor(frame, cv.COLOR_RGB2BGR)
    cv.imshow('LIVE CAMERA!!', gray)
    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
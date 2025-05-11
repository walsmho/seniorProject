import cv2 as cv
import sys

debug = True

#load image, run test
testImg = cv.imread("src\\learningTests\\theSun.jpg")
if testImg is None and debug == True:
    sys.exit("cameraTests error: could not read image {}".format(testImg))

cv.imshow("Press to close", testImg)
#0 = wait forever
key = cv.waitKey(0)

#Save if s key is pressed
if key == ord("s"):
    cv.imwrite("theSun.jpg", testImg)

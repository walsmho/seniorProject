# VISION VARS
FRAME_NAME = "Overhead Table View"
PUCK_MASK = "Puck Mask"
WEBCAM = 1
PUCK_TOLERANCE = 1
TOLERANCE = 10
FPS = 30
FRICTION = .4
PUCK_COLOR = [0,255,255] #BGR yellow value
BOUNDARY_COLOR = [110,80,255] #BGR Hot Pink for goal zones

# ROBOT VARS
ROBOGOAL = [(0, 140), (40, 220)]
PLAYERGOAL = [(600, 140), (640, 220)]
COORDINATE_THRESHOLD = 5 # Threshold, in pixels, of how far away a coordinate

CONVERTER = 0.5249343832 #Ratio of pixels:millimeters on both axis'
DSTEP = .2 #Distance per step of motor. Calculated by ((pulley teeth * mm pitch of belt)/(360/step degree of motor))
BUFFERX = 24.094499999992635 #pixel buffer to account for width of chassis rails still in camera view on x-axis

# CONTROLLER VARS
CALIBRATED = False
MOVEMENT_INPUT = 0

DEBUG = True

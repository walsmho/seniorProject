from src.config import *
from src.vision.visionUtil import stepToPixel
import time

class paddle:
    def __init__(self, coords=[0,0], newCoords=[0,0], debug=False):
        """Create a paddle object controlled by computer.
        
            ### Args:
                coords (list): current paddle coords
                newCoords (list): future coordinates for paddle. Defaults to [0,0]
                debug (bool): Enter debug mode

            ### Returns:
                None
        
        """
        self.cooldownDur = 0  # Cooldown in seconds
        self.lastAction = 0 
        self.currentCoords = coords
        self.newCoords = newCoords
        if debug:
            print("\npaddle.init: succesful initialization of paddle object")

    def homingSequence(self, controller, communicator, debug=False):
        """Homing function to re-calibrate robot coords using remote control. May be good to look into how to make gantry move slower, its not precise rn
        
            ### Args:
                paddle (class object): paddle class that hits the puck
                controller (class object): remote controller for manual mode
                communicator (class object): communication bridge between arduino and python

            ### Returns:
                None
        
        """

        # Do I keep MANUAL in config? Im worried about how im assinging globals in that file then using them
        print("\nGHOST HOMING INITIATED: PLEASE USE CONTROLLER TO ALLIGN PADDLE WITH GOAL. PRESS BUTTON 7 TO CONTINUE")
        HOMED = False
        MANUAL = False

        joystick = controller
        bridge = communicator

        while not HOMED:
            command, terminatorCheck = joystick.findGantryInput(DEBUG)
            if terminatorCheck == 1:
                HOMED = True

            bridge.issueCommand(command, DEBUG)
            arduinoResponse = bridge.receiveMessage(DEBUG)

            if arduinoResponse is not None and DEBUG:
                print(f"\npaddle.homingSequence: Message from arduino: {arduinoResponse}")

        while HOMED:
            self.currentCoords = [0,0]
            if DEBUG:
                manualCheck = str(input(("\npaddle.homingSequence: Homing complete. Would you like to verify coords? y/n: ")).lower())
                if manualCheck == "y":
                    MANUAL = True
                    while MANUAL:
                        command, terminatorCheck = joystick.findGantryInput(DEBUG)

                        okayX, okayY = self.coordCheck(self.currentCoords)

                        if okayX == "inBounds":
                            # Carry robot in normal dir
                            if command == "L":
                                self.currentCoords[0] -= 1
                            elif command == "R":
                                self.currentCoords[0] += 1

                        if okayY == "inBounds":
                            if command == "U":
                                self.currentCoords[1] += 1
                            elif command == "D":
                                self.currentCoords[1] -= 1
                        
                        print(self.currentCoords)
                
                        if okayY == "inBounds" and okayX == "inBounds":
                            bridge.issueCommand(command, False)
                            arduinoResponse = bridge.receiveMessage(False)

                        else:
                            if okayX == "LBound":
                                command = "R"
                                self.currentCoords[0] +=1
                            elif okayX == "RBound":
                                command = "L"
                                self.currentCoords[0] -= 1
                            if okayY == "UBound":
                                command = "D"
                                self.currentCoords[1] -= 1
                            elif okayY == "DBound":
                                command = "U"
                                self.currentCoords[1] += 1

                            bridge.issueCommand(command, False)
                            arduinoResponse = bridge.receiveMessage(False)

                        if terminatorCheck == 1:
                            MANUAL = False

                else:
                    MANUAL = False

            while not MANUAL:
                print("\nGHOST HOMING COMPLETED.")
                return

    def getUserCoords(self, debug=False):
        """Function for testing purposes only. Allow user to input their own coords for manual movement. These are stored into self.newCoords var
        
            ### Args:
                debug (bool): Enter debug mode

            ### Returns:
                None

        """

        try:
            x = int(input("Go to coord x: "))
            y = int(input("Go to coord y: "))
        except ValueError:
            x=0
            y=0
            print("\npaddle.getUserCoords: VALUE ERROR. Invalid input. Defaulting to 0,0")
        newCoords = [x, y]
        self.newCoords = newCoords
        if debug:
            print(f"\npaddle.getUserCoords: retrieved {newCoords} from user")
    
    def coordCheck(self, coords, debug=False):
        """Failsafe coordcheck based on previous testing. Gantry should NOT OVERREACH THESE NUMBERS. If it does, big uh oh
        
            ### Args:
                coords (list): [x,y] coords of robot paddle

            ### Returns:
                okieDokieX (str): inBounds, RBound, or LBound, respectively, for where gantry is
                okieDokieY (str): inBounds, UBound, or DBound, respectively, for where gantry is
        
        """

        #Current x bounds: 1400 and -1400
        #Current y bounds: 2800
        #Tape or make a jig on table for consistent calibration

        if coords[0] > 1400:
            okieDokieX = "RBound"
            print("R")
        elif coords[0] < -1400:
            okieDokieX = "LBound"
            print("L")
        elif coords[0] <= 1400 and self.currentCoords[0] >= -1400:
            okieDokieX = "inBounds"
        else:
            print(coords)
            okieDokieX = False

        if coords[1] >= 2800:
            okieDokieY = "UBound"
            print("U")
        elif coords[1] < 0:
            okieDokieY = "DBound"
            print("D")
        elif coords[1] <= 2800 and self.currentCoords[1] >= 0:
            okieDokieY = "inBounds"
        else:
            print(coords)
            okieDokieY = False

        if debug:
            print(f"paddle.coordCheck: Coord check X: {okieDokieX}")
            print(f"paddle.coordCheck: Coord check Y: {okieDokieY}")

        return okieDokieX, okieDokieY

    def gotoLinear(self, communicator, debug=False):
        """Travel to any coordinate within hockey table bounds, one axis at a time
        
            ### Args:
                communicator (class object): communication bridge between arduino and python
                debug (bool): Enter debug mode
                
            ### Returns:
                None
        
        """

        xOld, yOld = self.currentCoords
        xNew, yNew = self.newCoords

        xCheck, yCheck = self.coordCheck(self.newCoords)

        if xCheck != "inBounds" or yCheck != "inBounds":
            if debug:
                print(f"\ngotoLinear: invalid coordinate entry. {self.newCoords} out of bounds")
                self.newCoords = self.currentCoords
            return

        deltaX = xNew - xOld
        deltaY = yNew - yOld

        if debug:
            print(f"\ngotoLinear: current coords: [{xOld}, {yOld}]")
            print(f"\ngotoLinear: new coords: [{xNew}, {yNew}]")
            print(f"\ngotoLinear: delta coords: [{deltaX}, {deltaY}]")

        if (xCheck == "inBounds" and yCheck == "inBounds"):
            if deltaX > 0:
                directionX = "R"
            elif deltaX < 0:
                directionX = "L"
            
            if deltaY > 0:
                directionY = "U"
            elif deltaY < 0:
                directionY = "D"

        for _ in range(abs(deltaX)):
            communicator.issueCommand(directionX, False)

        for _ in range(abs(deltaY)):
            communicator.issueCommand(directionY, False)

    def pyendBresenham(self, communicator, debug=False):
        """Python based iterative style movement function. Go to any coordinate within hockey table bounds in a straight line
        
            ### Args:
                communicator (class object): communication bridge between arduino and python
                debug (bool): Enter debug mode
                
            ### Returns:
                None
        
        """
    
        xOld, yOld = self.currentCoords
        xNew, yNew = self.newCoords

        xCheck, yCheck = self.coordCheck(self.newCoords)

        if xCheck != "inBounds" or yCheck != "inBounds":
            if debug:
                print(f"\ngotoBresenham: invalid coordinate entry. {self.newCoords} out of bounds")
                self.newCoords = self.currentCoords
            return

        deltaX = abs(xNew - xOld)
        deltaY = -abs(yNew - yOld)
        sx = 1 if xOld < xNew else -1
        sy = 1 if yOld < yNew else -1
        err = deltaX + deltaY

        dirMap = {
            (1, 0): "R", (-1, 0): "L",
            (0, 1): "U", (0, -1): "D"
        }

        while True:
            if xOld == xNew and yOld == yNew:
                break

            e2 = 2 * err
            if e2 >= deltaY:
                xOld += sx
                communicator.issueCommand(dirMap[(sx, 0)], False)
                err += deltaY
            if e2 <= deltaX:
                yOld += sy
                communicator.issueCommand(dirMap[(0, sy)], False)
                err += deltaX

    def goto(self, communicator, newCoords=None, debug=False):
        """Arduino end iterative movement function. Go to any coordinate within hockey table bounds in a straight line
        
            ### Args:
                communicator (class object): communication bridge between arduino and python
                newCoords (list): [x,y] coords to go to. If None, uses internal
                debug (bool): Enter debug mode
                
            ### Returns:
                None
        
        """

        xOld, yOld = self.currentCoords
        print(f"CURRENT COORDS {self.currentCoords}")
        if newCoords is not None:
            # Check to see if coords passed wants to say same as previous, else, update simply with new
            if newCoords[0] == "self":
                self.newCoords[0] = self.currentCoords[0]
                self.newCoords[1] = newCoords[1]
            if newCoords[1] == "self":
                self.newCoords[1] = self.currentCoords[1]
                self.newCoords[0] = newCoords[0]
            else:
                self.newCoords = newCoords[0], newCoords[1]
        xNew, yNew = self.newCoords
        print(f"NEW COORDS {self.newCoords}")

        xCheck, yCheck = self.coordCheck(self.newCoords)
        print(f"STATUS CHECK {xCheck}, {yCheck}")

        if xCheck != "inBounds" or yCheck != "inBounds":
            #This is not a debug only message because otherwise it just won't move and it leaves lil Ryan scratching his head like a madman
            print(f"\ngiveArduinoCoords: invalid coordinate entry. {self.newCoords} out of bounds")
            self.newCoords = self.currentCoords
            return

        deltaX = abs(xNew - xOld)
        deltaY = abs(yNew - yOld)
        print(f"DELTAS: x {deltaX}, y {deltaY}")
        if xOld < xNew:
            sx = 1
        else:
            sx = -1
        if yOld < yNew:
            sy = 1
        else:
            sy = -1

        err = deltaX + deltaY

        infoPackage = [deltaX, deltaY, sx, sy, err]
        print(f"\nsending package {infoPackage}")
        communicator.issueCoordinate(infoPackage)
        communicator.waitForMessage()
        print("\ninfoPackage succesfully sent")
        return
    
    def statusCheck(self, puckPackage, debug=False):
        #DOUBLE CHECK TYPES OF PUCKPACKAGE CONTENTS FOR DOCSTRING
        """Meat and potatoes of the robotPaddle algorithm. Given data of puck, determine neccesary status
        
            ### Args:
                puckPackage (list): package containing:
                    moved (bool): If puck has moved significantly
                    direction (list): vector dir
                    speed (float): pixels/second speed calculation
                    lineStart (list): coord point of beginning of puck trajectory
                    lineEnd (list): coord point of end of puck trajectory, based on speed
                    danger (bool): If puck trajectory will go to robot goal

            ### Returns:
                status (int): Numerical status signifying action to take:
                    status=0: Passive response, do nothing
                    status=1: Emergency response, puck headed to goal -> return home to block
                    status=2: Defensive response, passively match puck y-axis positoin and block at closest intercept
                    status=3: Return response, hit back to player side
                    status=4: Attack response, hit towards player goal

                response (list): [x,y] PIXEL coordinates to return to, NONE if status=0
        
        """
        # Is this the most effective way to unpack a list into separate vars?
        currentTime = time.time()
        # Check cooldown
        if currentTime - self.lastAction < self.cooldownDur:
            if debug:
                print("Cooldown active - skipping response")
            return 0, None  # Passive status during cooldown

        #unpack
        moved = puckPackage[0]

        #Status for handling no movement in puck
        if not moved and (len(puckPackage) == 1): #If no movement and no puck data (off of board):
            print("NO MOVEMENT. PUCK NOT DETECTED")
            status = 9
            return status, None
        
        elif not moved and (len(puckPackage) == 2): #If no movement and puck exists
            moved = puckPackage[0]
            lineStart = puckPackage[1]

            print(lineStart)
            print(self.currentCoords)
            print(stepToPixel(self.currentCoords))

            if not moved and lineStart[0] > 300:
                print("PUCK IS IMMOBILE AT USER SIDE")
                status = 0
                return status, None
            
            elif not moved and lineStart[0] < 300:
                impact = 5
                if (stepToPixel(self.currentCoords)[1]) < lineStart[0]:
                    #print("PUCK IS IMMOBILE ON ROBOT SIDE AND IN FRONT OF GANTRY. HITTING")
                    status = 1
                    lineStart = list(lineStart)
                    # Give the paddle a little more oomf as it hits the puck (overshoot by 5 pixels)
                    if lineStart[0] < 0:
                        lineStart[0] = -abs(lineStart[0]+impact)
                    else:
                        lineStart[0] += impact
                    if lineStart[1] < 0:
                        lineStart[1] = -abs(lineStart[1]+impact)
                    else:
                        lineStart[1] +=5
                
                    response = [lineStart[0]+5, lineStart[1]+5]
                    return status, response
                
                else:
                    #print("PUCK IS IMMOBILE ON ROBOT SIDE BUT NOT HITTABLE. MOVING BEHIND IT")
                    status = 2
                    response = [lineStart[0]-50, lineStart[1]]
                    return status, response
            else:
                print("EDGE CASE UNKNOWN")
                status = 9
                response = None
                return status, response

        ### BELOW WORKS KIND OF
        # # If movement, things get more complex
        # else:
        #     direction = puckPackage[1]
        #     speed = puckPackage[2]
        #     lineStart = puckPackage[3]
        #     lineEnd = puckPackage[4]
        #     danger = puckPackage[5]

        #     print(puckPackage)

        #     if danger: #Later change to "if danger and speed > responseThreshold"
        #         status = "PUCK GOING TOWARDS GOAL"
        #         response = [0, 180]

        #         self.lastAction = currentTime
        #         return status, response
            
            # elif speed < 500:
            #     print("PUCK AT TRACKABLE SPEED")
            #     status = 2
            #     # Match the camera's y-axis so that the paddle is generally in the way, preventing the puck from going into the goal
            #     yResponse = max(ROBOGOAL[0][1], min(lineEnd[1], ROBOGOAL[1][1]))
            #     response = [60, yResponse]

            #     self.lastAction = currentTime
            #     return status, response

        else:
            return 0, None
        
        """
        
        Current thoughts / psuedocode for each status:
        1) If danger and speed > response threshold: Move to (0,0)
        Could also experiment with matching the PIXEL y-axis to the same as the puck, so it won't miss when it comes in from the corner (paddle[1] = lineEnd[1])
        Note: The pixel y-axis is really the robot x-axis

        2) If (danger and speed < response threshold) or (lineEnd is within bounds of robot side and speed < response threshold):
        If lineEnd[1] > robotCoord[1]: #if puck Y is in front of robot Y
            Find time it will take for puck to reach end point of line given pixels / sec
            Find time it will take gantry to reach any given point on line given max speed and current location

        
        """

    def update(self):
        """Make self.currentCoords update to the newCoords"""
        self.currentCoords = self.newCoords

"""
Purpose of file:
- Test: Have a function that allows user input of coordinates and then x and y travel to them
- Step 2: Upgrade function so that it travels directly. 
    - Update motorMove.cpp for joint stepper function
    - Allow bridge.py to send coord commands
    - Submit coords, check to make sure they're within bounds, travel directly

    Eventually, a separate function will do this instead of the user, after calculating the optimal intercept point

"""

from src.config import *

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

        self.currentCoords = coords
        self.newCoords = newCoords
        if debug:
            print("\npaddle.init: succesful initialization of paddle object")

    def homingSequence(self, controller, communicator, debug):
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
                print(f"\nhomingSequence: Message from arduino: {arduinoResponse}")

        while HOMED:
            self.currentCoords = [0,0]
            if DEBUG:
                manualCheck = str(input(("\nhomingSequence: Homing complete. Would you like to verify coords? y/n: ")).lower())
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
            print("\nrobotPaddle.getUserCoords: VALUE ERROR. Invalid input. Defaulting to 0,0")
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

        #Current x bounds: 900 and -900
        #Current y bounds: 1700
        #Tape or make a jig on table for consistent calibration

        if coords[0] > 900:
            okieDokieX = "RBound"
            print("R")
        elif coords[0] < -900:
            okieDokieX = "LBound"
            print("L")
        elif coords[0] <= 900 and self.currentCoords[0] >= -900:
            okieDokieX = "inBounds"
        else:
            print(coords)
            okieDokieX = False

        if coords[1] >= 1700:
            okieDokieY = "UBound"
            print("U")
        elif coords[1] < 0:
            okieDokieY = "DBound"
            print("D")
        elif coords[1] < 1700 and self.currentCoords[1] >= 0:
            okieDokieY = "inBounds"
        else:
            print(coords)
            okieDokieY = False

        print(okieDokieX)
        print(okieDokieY)

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

    def gotoBresenham(self, communicator, debug=False):
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
        sx = 1 if x0 < xNew else -1
        sy = 1 if y0 < yNew else -1
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
                x0 += sx
                communicator.issueCommand(dirMap[(sx, 0)], False)
                err += deltaY
            if e2 <= deltaX:
                y0 += sy
                communicator.issueCommand(dirMap[(0, sy)], False)
                err += deltaX

    def update(self):
        """Make self.currentCoords update to the newCoords"""
        self.currentCoords = self.newCoords

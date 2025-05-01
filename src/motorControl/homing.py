from src.config import *

def coordCheck(robotCoords, debug=False):
    """Failsafe coordcheck based on previous testing. Gantry should NOT OVERREACH THESE NUMBERS. If it does, big uh oh
    
        ### Args:
            robotCoords (list): [x,y] coords of robot paddle

        ### Returns:
            okieDokieX (bool): if okieDokieX is True, things are okieDokie with x-axis!
            okieDokieY (bool): if okieDokieY is True, things are okieDokie with y-axis!
    
    """
    #Current x bounds: 920 and -920
    #Current y bounds: 1780

    # Need to check logic and also account that some axis' might be okie while others are very NOT okie

    if robotCoords[0] > 920:
        okieDokieX = "RBound"
        print("R")
    elif robotCoords[0] < -920:
        okieDokieX = "LBound"
        print("L")
    elif robotCoords[0] <= 920 and robotCoords[0] >= -920:
        okieDokieX = "inBounds"
    else:
        print("idk man")
        okieDokieX = None

    if robotCoords[1] >= 1780:
        okieDokieY = "UBound"
        print("U")
    elif robotCoords[1] < 0:
        okieDokieY = "DBound"
        print("D")
    elif robotCoords[1] < 1780 and robotCoords[1] >= 0:
        okieDokieY = "inBounds"
    else:
        print("idk man")
        okieDokieY = None

    return okieDokieX, okieDokieY
    

def homingSequence(controller, communicator, debug):
    """Homing function to re-calibrate robot coords using remote control. May be good to look into how to make gantry move slower, its not precise rn
    
        ### Args:
            controller (class object): remote controller for manual mode
            communicator (class object): communication bridge between arduino and python

        ### Returns:
            robotCoords (list): centered [0,0] coords of robot for future use
    
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
        robotCoords = [0,0]
        if DEBUG:
            manualCheck = str(input(("\nhomingSequence: Homing complete. Would you like to verify coords? y/n: ")).lower())
            if manualCheck == "y":
                MANUAL = True
                while MANUAL:
                    command, terminatorCheck = joystick.findGantryInput(DEBUG)

                    okayX, okayY = coordCheck(robotCoords)

                    if okayX == "inBounds":
                        # Carry robot in normal dir
                        if command == "L":
                            robotCoords[0] -= 1
                        elif command == "R":
                            robotCoords[0] += 1

                    if okayY == "inBounds":
                        if command == "U":
                            robotCoords[1] += 1
                        elif command == "D":
                            robotCoords[1] -= 1
                       
                    print(robotCoords)
            
                    if okayY == "inBounds" and okayX == "inBounds":
                        bridge.issueCommand(command, False)
                        arduinoResponse = bridge.receiveMessage(False)

                    else:
                        if okayX == "LBound":
                            command = "R"
                            robotCoords[0] +=1
                        elif okayX == "RBound":
                            command = "L"
                            robotCoords[0] -= 1
                        if okayY == "UBound":
                            command = "D"
                            robotCoords[1] -= 1
                        elif okayY == "DBound":
                            command = "U"
                            robotCoords[1] += 1

                        bridge.issueCommand(command, False)
                        arduinoResponse = bridge.receiveMessage(False)

                    if terminatorCheck == 1:
                        MANUAL = False

            else:
                MANUAL = False

        while not MANUAL:
            print("\nGHOST HOMING COMPLETED.")
            return robotCoords

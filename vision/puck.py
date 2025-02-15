import numpy as np
import cv2

# TODO: Make this coord system utilize the center of the bbox instead of bottom left throughout

class puckObject:
    def __init__(self, coordBottom=(0,0), coordTop=(0,0)):
        self.coordBottom = coordBottom
        self.coordTop = coordTop

    def update(self, newCoord1, newCoord2, debug=False):
        """Update self coords used in boundingbox to new position
        
            ### Args:
                newCoord1 (tuple): bottom left box coordinate
                newCoord2 (tuple): top right box coordinate
                debug (bool): enter debug mode

            ### Returns:
                None

        """

        self.coordBottom = newCoord1
        self.coordTop = newCoord2
        if debug:
            print("\npuck.update: Succesful coordinate update")

    def hasMoved(self, coordNew, tolerance, debug=False):
        """Uses the center coord provided and a tolerance to determine if object has changed position
        
            ### Args:
                coordNew (tuple): new coordinate to compare with self coord
                tolerance (int): Number for +- pixels to account for noise
                debug (bool): enter debug mode

            ### Returns:
                movedX, trajectoryX
        
        """

        #Check x-axis coords
        if np.abs(self.coordBottom[0]-coordNew[0]) > tolerance:
            movedX = True

            if self.coordBottom > coordNew:
                if debug:
                    print("objMoved: Moved Left")
                trajectoryX = "left"
            elif self.coordBottom < coordNew:
                if debug:
                    print("objMoved: Moved Right")
                trajectoryX = "right"

        elif np.abs(self.coordBottom[0]-coordNew[0] <= tolerance):
            if debug:
                print("objMoved: No x-axis movement")
            movedX = False
            trajectoryX = None

        #Check y-axis coords
        if np.abs(self.coordBottom[1]-coordNew[1]) > tolerance:
            movedY = True

            if self.coordBottom > coordNew:
                if debug:
                    print("objMoved: Moved Up")
                trajectoryY = "up"
            elif self.coordBottom < coordNew:
                if debug:
                    print("objMoved: Moved Down")
                trajectoryY = "down"

        elif np.abs(self.coordBottom[1]-coordNew[1] <= tolerance):
            if debug:
                print("objMoved: No y-axis movement")
            movedY = False
            trajectoryY = None

        else:
            movedX = False
            movedY = False
            trajectoryX = None
            trajectoryY = None
        
        return movedX, movedY, trajectoryX, trajectoryY

    def currentVector(self, currentCenter, fps=30, debug=False):
        """Finds vector of puck based on recent coordinates
        
            ### Args:
                currentCenter (tuple): Coordinates of center of bbox
                fps (int): Frames Per Second of camera in use
                debug (bool): Enter debug mode
        
            ### Returns:
                moved (bool): If moved above threshold
                direction (np.array()): coord points for direction
                speed (float): speed in pixels/second
        """

        #Calculate center of puck from bbox coords
        oldCenter = np.array([(self.coordBottom[0]+self.coordTop[0])/2, ((self.coordBottom[1]+self.coordTop[1])/2)])
        deltaTime = 1/fps
        if debug:
            print("currentVector: previous puck center coord designated as {}".format(oldCenter))
        
        displacement = np.array(currentCenter) - oldCenter

        if debug:
            print("currentVector: displacement at {}".format(displacement))

        if np.linalg.norm(displacement) > 0:
            direction = displacement / np.linalg.norm(displacement)
        else:
            direction = np.array([0,0])

        speed = np.linalg.norm(displacement) / deltaTime

        # If movement above threshold
        if np.linalg.norm(displacement) > 1:
            moved = True
        else:
            moved = False

        return moved, direction, speed
    
    def linePrediction(self, view, currentCenter, direction, lineColor=(0,255,0), lineThickness=3, lineScale=250, debug=False):
        currentCenter = (int(currentCenter[0]), int(currentCenter[1]))
        lineEnd = currentCenter + direction * lineScale
        lineEnd = (int(lineEnd[0]), int(lineEnd[1]))

        if debug:
            print(currentCenter)
            print(lineEnd)

        cv2.line(view, currentCenter, lineEnd, lineColor, lineThickness)

        return currentCenter, lineEnd

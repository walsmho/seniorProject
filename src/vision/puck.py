import numpy as np
import cv2
from src.config import *

# TODO: Make this coord system utilize the center of the bbox instead of bottom left throughout

class puckObject:
    def __init__(self, coordBottom=(0,0), coordTop=(0,0)):
        """Create a new puck object with given coordinates. If none given, coords are set at 0.
        
            ### Args:
                coordBottom (tuple): coordinate for bottom left of puck
                coordTop (tuple): coordinate for top right of puck

            ### Returns:
                None
        
        """

        self.coordBottom = coordBottom
        self.coordTop = coordTop

    def update(self, newCoord1, newCoord2, debug=False):
        """Update self coords used in boundingbox to new position
        
            ### Args:
                newCoord1 (tuple): Bottom left box coordinate
                newCoord2 (tuple): Top right box coordinate
                debug (bool): enter Debug mode

            ### Returns:
                None

        """

        array1 = np.array(newCoord1)
        array2 = np.array(newCoord2)
        oldBottom = np.array(self.coordBottom)
        oldTop = np.array(self.coordTop)

        # smooth
        bottomChange = np.linalg.norm(array1 - oldBottom) >= PUCK_TOLERANCE
        topChange = np.linalg.norm(array2 - oldTop) >= PUCK_TOLERANCE

        if bottomChange:
            self.coordBottom = newCoord1
        if topChange:
            self.coordTop = newCoord2

        if debug:
            print("\npuck.update: Succesful coordinate update")

    def currentVector(self, currentCenter, fps, debug=False):
        """Finds vector of puck based on recent coordinates
        
            ### Args:
                currentCenter (tuple): Coordinates of center of bbox
                fps (int): Frames Per Second of camera in use
                debug (bool): Enter debug mode
        
            ### Returns:
                moved (bool): If moved above threshold
                direction (np.array()): Coord points for direction
                speed (float): Speed in pixels/second
        """

        #Calculate center of puck from bbox coords
        oldCenter = np.array([(self.coordBottom[0]+self.coordTop[0])/2, ((self.coordBottom[1]+self.coordTop[1])/2)])
        deltaTime = 1/fps 
        if debug:
            print(f"\npuck.currentVector: previous puck center coord designated as {oldCenter}")
        
        displacement = np.array(currentCenter) - oldCenter

        if debug:
            print(f"\npuck.currentVector: displacement at {displacement}")

        if np.linalg.norm(displacement) > TOLERANCE:
            direction = displacement / np.linalg.norm(displacement)
        else:
            direction = np.array([0,0])

        speed = np.linalg.norm(displacement) / deltaTime

        # If movement above threshold - TRY USING SOME SMOOTHING ALGORITHM LATER
        if np.linalg.norm(displacement) > TOLERANCE:
            moved = True
        else:
            moved = False
            if debug:
                print("\ncurrentVector: no movement detected")

        if moved and debug:
            print(f"\ncurrentVector: speed of {speed} pixels/sec")
            print(f"\ncurrentVector: direction {direction}")

        return moved, direction, speed

    def reboundPrediction(self, view, height, width, currentCenter, direction, speed, lineColor=(0,255,0), lineThickness=3, debug=False):
        """Predicts the trajectory of the puck given its current position, direction, and table perimeter, then visualizes with a line.
        
            ### Args:
                view (cv2 object): Frame window to draw line in
                height
                currentCenter (np.array): Centered coordinates of tracked puck
                direction (np.array): Numpy vector of direction
                speed (thingy):
                lineColor (tuple): BGR value for line color in cv2 window
                lineThickness (int): Thickness of line on cv2 screen
                debug (bool): Enter debug mode

            ### Returns:
                currentCenter (tuple): Coords of puck center
                pathPts (tuple): Coords of line end 

        """

        # Calculate line length based on speed
        speed = speed/15
        print(f"speed: {speed}")
        lineScale = min(((speed**2) / (2 * FRICTION)/10), 1000)

        print(f"line length: {lineScale}")

        pos = np.array(currentCenter, dtype=float)
        remainingDistance = lineScale
        pathPts = [tuple(pos.astype(int))]

        # Calculate bounces
        while remainingDistance > 0:
            if direction[0] > 0:
                distRight = (width - pos[0]) / direction[0]
            elif direction[0] < 0:
                distRight = -pos[0] / direction[0]
            else:
                distRight = float('inf')

            if direction[1] > 0:
                distBottom = (height - pos[1]) / direction[1]
            elif direction[1] < 0:
                distBottom = -pos[1] / direction[1]
            else:
                distBottom = float('inf')

            # Find the shortest distance to a wall
            minDist = min(distRight, distBottom, remainingDistance)

            # Move along the direction vector
            if debug:
                print(f"\nreboundPrediction: DIRECTION: {direction}")
                print(f"\nreboundPrediction: minDist: {minDist}")
            pos += direction * minDist
            pathPts.append(tuple(pos.astype(int)))
            remainingDistance -= minDist

            # Reflect direction if a wall was hit
            if minDist == distRight:
                direction[0] *= -1  # Reflect X
            if minDist == distBottom:
                direction[1] *= -1  # Reflect Y

        # Draw Path
        for i in range(len(pathPts)-1):
            pt1 = tuple(map(int, pathPts[i]))
            pt2 = tuple(map(int, pathPts[i+1]))
            if debug:
                print(type(pt1))
                print(pt1)
                print(type(pt2))
                print(pt2)
            cv2.line(view, pt1, pt2, lineColor, lineThickness)

        if debug:
            print(f"reboundPrediction: Trajectory Points: {pathPts}")

        return tuple(currentCenter), pathPts[-1]

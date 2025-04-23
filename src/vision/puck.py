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
                newCoord1 (tuple): Bottom left box coordinate
                newCoord2 (tuple): Top right box coordinate
                debug (bool): enter Debug mode

            ### Returns:
                None

        """

        self.coordBottom = newCoord1
        self.coordTop = newCoord2
        if debug:
            print("\npuck.update: Succesful coordinate update")

    def currentVector(self, currentCenter, tolerance, fps, debug=False):
        """Finds vector of puck based on recent coordinates
        
            ### Args:
                currentCenter (tuple): Coordinates of center of bbox
                tolerance (int): Pixel tolerance before displacement is considered as movement
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

        if np.linalg.norm(displacement) > tolerance:
            direction = displacement / np.linalg.norm(displacement)
        else:
            direction = np.array([0,0])

        speed = np.linalg.norm(displacement) / deltaTime

        # If movement above threshold
        if np.linalg.norm(displacement) > 5:
            moved = True
        else:
            moved = False

        if moved and debug:
            print(f"\ncurrentVector: speed of {speed} pixels/sec")
            print(f"\ncurrentVector: direction {direction}")

        return moved, direction, speed
    
    def linePrediction(self, view, currentCenter, direction, lineColor=(0,255,0), lineThickness=3, lineScale=500, debug=False):
        """Predicts the trajectory of the puck given its current position and direction and draws a line for it. DOES NOT ACCOUNT FOR SPEED OR RAILS IN CURRENT VERSION
        
            ### Args:
                view (cv2 object): Frame window to draw line in
                currentCenter (np.array): Centered coordinates of tracked puck
                direction (np.array): Numpy vector of direction
                lineColor (tuple): BGR value for line color in cv2 window
                lineThickness (int): Thickness of line on cv2 screen
                lineScale (int): Line length in pixels. This will not be a variable in future iterations, as length will be determined on speed and reflections off the walls
                debug (bool): Enter debug mode

            ### Returns:
                currentCenter (tuple): Coords of puck center
                lineEnd (tuple): Coords of line end
        
        """
    
        currentCenter = (int(currentCenter[0]), int(currentCenter[1]))
        lineEnd = currentCenter + direction * lineScale
        lineEnd = (int(lineEnd[0]), int(lineEnd[1]))

        if debug:
            print(f"\nlinePrediction: puck center at {currentCenter}")
            print(f"\nlinePrediction: puck ending at {lineEnd}")
            print(f"\nlinePrediction: start and end coords are type {type(currentCenter)}, {type(lineEnd)}. Should both be tuples")

        cv2.line(view, currentCenter, lineEnd, lineColor, lineThickness)

        return currentCenter, lineEnd
    
    def reboundPrediction(self, view, height, width, currentCenter, direction, lineColor=(0,255,0), lineThickness=3, lineScale=500, debug=False):
        """Boojier linePrediction that accounts for rebounds off air hockey rails.
        
        """

        direction = direction / np.linalg.norm(direction)

        pos = np.array(currentCenter, dtype=float)
        remainingDistance = lineScale
        pathPts = [tuple(pos.astype(int))]

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
            print(f"DIRECTION: {direction}")
            print(f"minDist: {minDist}")
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
            print(pathPts)
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

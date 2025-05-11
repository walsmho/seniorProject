// BASIC MOTOR DIRECTIONS
// Look into c++ docstrings?

// NOTE: LABELING MOTORS STEPX AND STEPY INNACURATE WITH HBOT SYSTEM. RENAME TO MOTORLEFT AND MOTORRIGHT
// CURRENT PROBLEM: PASS COORDINATES 255 AND YOU HAVE A BIT PROBLEM. SOME VARIABL
#include <Arduino.h>
#include "motorMove.h"

int currentX = 0;
int currentY = 0;

const int StepX = 2;
const int DirX = 5;
const int StepY = 3;
const int DirY = 6;

void yForward(int steps, int delay) {
    digitalWrite(DirX, LOW);
    digitalWrite(DirY, HIGH);

    for (int i = 0; i < steps; i++) {
        // Step both motors HIGH
        digitalWrite(StepX, HIGH);
        digitalWrite(StepY, HIGH);
        delayMicroseconds(delay);

        // Step both motors LOW
        digitalWrite(StepX, LOW);
        digitalWrite(StepY, LOW);
        delayMicroseconds(delay);
    }
}

void yBackward(int steps, int delay) {
    digitalWrite(DirX, HIGH);
    digitalWrite(DirY, LOW);

    for (int i = 0; i < steps; i++) {
        // Step both motors HIGH
        digitalWrite(StepX, HIGH);
        digitalWrite(StepY, HIGH);
        delayMicroseconds(delay);

        // Step both motors LOW
        digitalWrite(StepX, LOW);
        digitalWrite(StepY, LOW);
        delayMicroseconds(delay);
    }
}

void xRight(int steps, int delay) {
    digitalWrite(DirX, LOW);
    digitalWrite(DirY, LOW);

    for (int i = 0; i < steps; i++) {
        // Step both motors HIGH
        digitalWrite(StepX, HIGH);
        digitalWrite(StepY, HIGH);
        delayMicroseconds(delay);

        // Step both motors LOW
        digitalWrite(StepX, LOW);
        digitalWrite(StepY, LOW);
        delayMicroseconds(delay);
    }
}

void xLeft(int steps, int delay) {
    digitalWrite(DirX, HIGH);
    digitalWrite(DirY, HIGH);

    for (int i = 0; i < steps; i++) {
        // Step both motors HIGH
        digitalWrite(StepX, HIGH);
        digitalWrite(StepY, HIGH);
        delayMicroseconds(delay);

        // Step both motors LOW
        digitalWrite(StepX, LOW);
        digitalWrite(StepY, LOW);
        delayMicroseconds(delay);
    }
}

// deltaX, deltaY: absolute step counts along X and Y
// sx, sy: +1 or -1 for X and Y directions
void bresenhamMove(long deltaX, long deltaY, int sx, int sy) {
    /*    plotLine(x0, y0, x1, y1)
        dx = abs(x1 - x0)
        sx = x0 < x1 ? 1 : -1
        dy = -abs(y1 - y0)
        sy = y0 < y1 ? 1 : -1
        error = dx + dy
        
        while true
            plot(x0, y0)
            e2 = 2 * error
            if e2 >= dy
                if x0 == x1 break
                error = error + dy
                x0 = x0 + sx
            end if
            if e2 <= dx
                if y0 == y1 break
                error = error + dx
                y0 = y0 + sy
            end if
        end while*/

    long dx = labs(deltaX);
    long dy = labs(deltaY);
    long err = dx + dy;

    // Loop until we've exhausted both X and Y steps
    while (dx > 0 || dy > 0) {
        int e2 = 2 * err;

        // X step?
        if (dx > 0 && e2 > dy) {
            if (sx > 0) {
                xRight(1, 500);
            } else {
                xLeft(1, 500);
            }
            err += dy;
            dx--;

            currentX += sx;
        }

        // Y step?
        if (dy > 0 && e2 < dx) {
            if (sy > 0) {
                yForward(1, 500);
            } else {
                yBackward(1, 500);
            }
            err += dx;
            dy--;

            currentY += sy;
        }
    }
}

void parseAndMove(String command) {
    // Parse the deltas and other parameters
    int indexDx = command.indexOf("dx");
    int indexDy = command.indexOf("dy");
    int indexSx = command.indexOf("sx");
    int indexSy = command.indexOf("sy");
    int indexErr = command.indexOf("er");

    if (indexDx == -1 || indexDy == -1 || indexSx == -1 || indexSy == -1 || indexErr == -1) {
        return;
    }

    // Extract the values from the command string
    // Housekeeping: switch from strtol to toint
    long deltaX = strtol(command.substring(indexDx + 2, indexDy).c_str(), NULL, 10);
    long deltaY = strtol(command.substring(indexDy + 2, indexSx).c_str(), NULL, 10);
    int stepDirX = strtol(command.substring(indexSx + 2, indexSy).c_str(), NULL, 10);
    int stepDirY = strtol(command.substring(indexSy + 2, indexErr).c_str(), NULL, 10);

    // Perform movement using Bresenham's algorithm or similar
    bresenhamMove(abs(deltaX), abs(deltaY), stepDirX, stepDirY);

    Serial.println("X: ");
    Serial.print(currentX);   
    Serial.print("Y: ");
    Serial.print(currentY);

}

// BASIC MOTOR DIRECTIONS
// Look into c++ docstrings?

// NOTE: LABELING MOTORS STEPX AND STEPY INNACURATE WITH HBOT SYSTEM. RENAME TO MOTORLEFT AND MOTORRIGHT
// CURRENT PROBLEM: PASS COORDINATES 255 AND YOU HAVE A BIT PROBLEM. SOME VARIABL
#include <Arduino.h>
#include "motorMove.h"

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
    long dx = labs(deltaX);
    long dy = labs(deltaY);

    long currentX = 0;
    long currentY = 0;

    long err = dx - dy;

    while (labs(currentX) < dx || labs(currentY) < dy) {
        long e2 = 2 * err;

        if (e2 > -dy && labs(currentX) < dx) {
            err -= dy;
            currentX += sx;

            if (sx > 0) xRight(1, 500);
            else xLeft(1, 500);
        }

        if (e2 < dx && labs(currentY) < dy) {
            err += dx;
            currentY += sy;

            if (sy > 0) yForward(1, 500);
            else yBackward(1, 500);
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

    // Extract the values from the command string
    // Housekeeping: switch from strtol to toint
    long deltaX = strtol(command.substring(indexDx + 2, indexDy).c_str(), NULL, 10);
    long deltaY = strtol(command.substring(indexDy + 2, indexSx).c_str(), NULL, 10);
    int stepDirX = strtol(command.substring(indexSx + 2, indexSy).c_str(), NULL, 10);
    int stepDirY = strtol(command.substring(indexSy + 2, indexErr).c_str(), NULL, 10);

    // Perform movement using Bresenham's algorithm or similar
    bresenhamMove(abs(deltaX), abs(deltaY), stepDirX, stepDirY);
}

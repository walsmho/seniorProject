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

void stepMotor(int stepPin, int dirPin, bool dir, int steps) {
    digitalWrite(dirPin, dir); // Set direction: LOW or HIGH
    for(int x = 0; x < steps; x++) {
        digitalWrite(stepPin, HIGH);
        delayMicroseconds(500);
        digitalWrite(stepPin, LOW);
        delayMicroseconds(500);
    }
}

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
void bresenhamMove(long deltaX, long deltaY, int sx, int sy, int currentX, int currentY) {
    long dx = labs(deltaX);
    long dy = labs(deltaY);
    long err = dx - dy;

    // Loop until we've exhausted both X and Y steps
    while (dx > 0 || dy > 0) {
        long e2 = err;

        // X step?
        if (dx > 0 && e2 > -dy) {
            if (sx > 0) {
                xRight(1, 500);
                currentX += 1;
            } else {
                xLeft(1, 500);
                currentX -= 1;
            }
            err -= dy;
            dx--;
        }

        // Y step?
        if (dy > 0 && e2 < dx) {
            if (sy > 0) {
                yForward(1, 500);
                currentY += 1;
            } else {
                yBackward(1, 500);
                currentY -= 1;
            }
            err += dx;
            dy--;
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
    long deltaX = strtol(command.substring(indexDx + 2, indexDy).c_str(), NULL, 10);
    long deltaY = strtol(command.substring(indexDy + 2, indexSx).c_str(), NULL, 10);
    int stepDirX = strtol(command.substring(indexSx + 2, indexSy).c_str(), NULL, 10);
    int stepDirY = strtol(command.substring(indexSy + 2, indexErr).c_str(), NULL, 10);

    // Perform movement using Bresenham's algorithm or similar
    bresenhamMove(abs(deltaX), abs(deltaY), stepDirX, stepDirY, currentX, currentY);

}


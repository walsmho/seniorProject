// BASIC MOTOR DIRECTIONS
// Look into c++ docstrings?

// NOTE: LABELING MOTORS StepA AND StepB INNACURATE WITH HBOT SYSTEM. RENAME TO MOTORLEFT AND MOTORRIGHT
// CURRENT PROBLEM: PASS COORDINATES 255 AND YOU HAVE A BIT PROBLEM. SOME VARIABL
#include <Arduino.h>
#include "motorMove.h"

const int StepA = 2;
const int DirA = 5;
const int StepB = 3;
const int DirB = 6;

int motorSpeed = 500;

void yForward(int steps, int delay) {
    digitalWrite(DirA, LOW);
    digitalWrite(DirB, HIGH);

    for (int i = 0; i < steps; i++) {
        // Step both motors HIGH
        digitalWrite(StepA, HIGH);
        digitalWrite(StepB, HIGH);
        delayMicroseconds(delay);

        // Step both motors LOW
        digitalWrite(StepA, LOW);
        digitalWrite(StepB, LOW);
        delayMicroseconds(delay);
    }
}

void yBackward(int steps, int delay) {
    digitalWrite(DirA, HIGH);
    digitalWrite(DirB, LOW);

    for (int i = 0; i < steps; i++) {
        // Step both motors HIGH
        digitalWrite(StepA, HIGH);
        digitalWrite(StepB, HIGH);
        delayMicroseconds(delay);

        // Step both motors LOW
        digitalWrite(StepA, LOW);
        digitalWrite(StepB, LOW);
        delayMicroseconds(delay);
    }
}

void xLeft(int steps, int delay) {
    digitalWrite(DirA, LOW);
    digitalWrite(DirB, LOW);

    for (int i = 0; i < steps; i++) {
        // Step both motors HIGH
        digitalWrite(StepA, HIGH);
        digitalWrite(StepB, HIGH);
        delayMicroseconds(delay);

        // Step both motors LOW
        digitalWrite(StepA, LOW);
        digitalWrite(StepB, LOW);
        delayMicroseconds(delay);
    }
}

void xRight(int steps, int delay) {
    digitalWrite(DirA, HIGH);
    digitalWrite(DirB, HIGH);

    for (int i = 0; i < steps; i++) {
        // Step both motors HIGH
        digitalWrite(StepA, HIGH);
        digitalWrite(StepB, HIGH);
        delayMicroseconds(delay);

        // Step both motors LOW
        digitalWrite(StepA, LOW);
        digitalWrite(StepB, LOW);
        delayMicroseconds(delay);
    }
}

// deltaX, deltaY: absolute step counts along X and Y
// sx, sy: +1 or -1 for X and Y directions
void bresenhamMove(long deltaX, long deltaY, int sx, int sy) {
    long dx = labs(deltaX);
    long dy = -labs(deltaY);

    long currentX = 0;
    long currentY = 0;

    long err = dx + dy;

    while (labs(currentX) < dx || labs(currentY) < -dy) {
        long e2 = 2 * err;

        if (e2 > dy && labs(currentX) < dx) {
            err += dy;
            currentX += sx;
            if (sx > 0) xRight(1, motorSpeed);
            else xLeft(1, motorSpeed);
        }

        if (e2 < dx && labs(currentY) < -dy) {
            err += dx;
            currentY += sy;
            if (sy > 0) yForward(1, motorSpeed);
            else yBackward(1, motorSpeed);
        }
    }
}

void rampMove(long deltaX, long deltaY, int sx, int sy) {
    long dx = labs(deltaX);
    long dy = labs(deltaY);
    long totalSteps = max(dx, dy);

    long currentX = 0;
    long currentY = 0;
    long err = dx - dy;

    // int minDelay = 160;   // fastest speed
    // int maxDelay = 500;   // slowest (starting) speed
    int minDelay = 300;
    int maxDelay = 500;
    int rampSteps = totalSteps / 4;

    for (long i = 0; labs(currentX) < dx || labs(currentY) < dy; ++i) {
        int stepDelay;
        if (i < rampSteps) {
            stepDelay = maxDelay - ((maxDelay - minDelay) * i / rampSteps); // accelerate
        // } else if (i > totalSteps - rampSteps) {
        //     stepDelay = maxDelay - ((maxDelay - minDelay) * (totalSteps - i) / rampSteps); // decelerate
        } else {
            stepDelay = minDelay;
        }

        long e2 = 2 * err;

        if (e2 > -dy && labs(currentX) < dx) {
            err -= dy;
            currentX += 1;
            if (sx > 0) xRight(1, stepDelay);
            else xLeft(1, stepDelay);
        }

        if (e2 < dx && labs(currentY) < dy) {
            err += dx;
            currentY += 1;
            if (sy > 0) yForward(1, stepDelay);
            else yBackward(1, stepDelay);
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
    int stepDirA = strtol(command.substring(indexSx + 2, indexSy).c_str(), NULL, 10);
    int stepDirB = strtol(command.substring(indexSy + 2, indexErr).c_str(), NULL, 10);

    // Perform movement using Bresenham's algorithm or similar
    bresenhamMove(abs(deltaX), abs(deltaY), stepDirA, stepDirB);
}

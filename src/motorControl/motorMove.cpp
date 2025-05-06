// BASIC MOTOR DIRECTIONS
// Look into c++ docstrings?

// NOTE: LABELING MOTORS STEPX AND STEPY INNACURATE WITH HBOT SYSTEM. RENAME TO MOTORLEFT AND MOTORRIGHT

#include <Arduino.h>
#include "motorMove.h"

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

// void moveToCoord(int currentX, int currentY, int targetX, int targetY, int delayMicros) {
//     int dx = targetX - currentX;
//     int dy = targetY - currentY;

//     int steps = max(abs(dx), abs(dy));
//     if (steps == 0) return;  // No movement needed

//     float stepX = (float)dx / steps;
//     float stepY = (float)dy / steps;

//     float posX = currentX;
//     float posY = currentY;

//     for (int i = 0; i < steps; i++) {
//         posX += stepX;
//         posY += stepY;

//         int roundedX = round(posX);
//         int roundedY = round(posY);

//         int deltaX = roundedX - currentX;
//         int deltaY = roundedY - currentY;

//         if (deltaX == 0 && deltaY == 0) continue;

//         currentX = roundedX;
//         currentY = roundedY;

//         // Determine motor directions for H-bot
//         int dirA, dirB;
//         if (deltaX != 0 && deltaY == 0) {
//             // Pure X movement: both motors same direction
//             dirA = (deltaX > 0) ? HIGH : LOW;
//             dirB = dirA;
//         } else if (deltaY != 0 && deltaX == 0) {
//             // Pure Y movement: motors opposite direction
//             dirA = (deltaY > 0) ? HIGH : LOW;
//             dirB = (deltaY > 0) ? LOW : HIGH;
//         } else {
//             // Diagonal movement (combined X and Y)
//             int xSign = (deltaX > 0) ? 1 : -1;
//             int ySign = (deltaY > 0) ? 1 : -1;

//             // Diagonal: set directions based on vector sum
//             dirA = (xSign + ySign > 0) ? HIGH : LOW;
//             dirB = (xSign - ySign > 0) ? HIGH : LOW;
//         }

//         digitalWrite(DirX, dirA); // Motor A
//         digitalWrite(DirY, dirB); // Motor B

//         // Pulse both motors
//         digitalWrite(StepX, HIGH);
//         digitalWrite(StepY, HIGH);
//         delayMicroseconds(delayMicros);
//         digitalWrite(StepX, LOW);
//         digitalWrite(StepY, LOW);
//         delayMicroseconds(delayMicros);
//     }
// }

// bool findIncomingCoords(const String& input, Coord& from, Coord& to) {
//     String data = input;
//     if (!data.endsWith("\n")) {
//         data += '\n';
//     }

//     int sep = data.indexOf('|');
//     if (sep == -1) return false;

//     String first = data.substring(2, sep);  // Skip "G:"
//     String second = data.substring(sep + 1);
//     second.trim();  // Remove newline and extra spaces

//     int comma1 = first.indexOf(',');
//     int comma2 = second.indexOf(',');

//     if (comma1 == -1 || comma2 == -1) return false;

//     from.x = first.substring(0, comma1).toInt();
//     from.y = first.substring(comma1 + 1).toInt();

//     to.x = second.substring(0, comma2).toInt();
//     to.y = second.substring(comma2 + 1).toInt();

//     return true;
// }

#ifndef MOTOR_MOVE_H
#define MOTOR_MOVE_H

struct Coord {
    int x;
    int y;
};

void yForward(int steps, int delay);
void yBackward(int steps, int delay);
void xRight(int steps, int delay);
void xLeft(int steps, int delay);

void moveToCoord(int currentX, int currentY, int targetX, int targetY, int delayMicros);
bool findIncomingCoords(const String& input, Coord& from, Coord& to);

#endif

#ifndef MOTOR_MOVE_H
#define MOTOR_MOVE_H

extern long currentX;
extern long currentY;

void yForward(int steps, int delay);
void yBackward(int steps, int delay);
void xRight(int steps, int delay);
void xLeft(int steps, int delay);

void bresenhamMove(long deltaX, long deltaY, int sx, int sy, long &currentX, long &currentY);
void parseAndMove(String command);

#endif

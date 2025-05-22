#ifndef MOTOR_MOVE_H
#define MOTOR_MOVE_H

void yForward(int steps, int delay);
void yBackward(int steps, int delay);
void xRight(int steps, int delay);
void xLeft(int steps, int delay);

void bresenhamMove(long deltaX, long deltaY, int sx, int sy);
void rampMove(long deltaX, long deltaY, int sx, int sy);
void parseAndMove(String command);

#endif

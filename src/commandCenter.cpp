#include <Arduino.h>
#include "motorControl/motorMove.h"

bool DEBUG;
// init vars
int currentX = 0;
int currentY = 0;

// NOTE: LABELING MOTORS STEPX AND STEPY INNACURATE WITH HBOT SYSTEM. RENAME TO MOTORLEFT AND MOTORRIGHT

void setup() {
    //Open Serial for comms
    Serial.begin(9600);
    String incMessage;

    //Set pins for CNC shield
    const int StepX = 2;
    const int DirX = 5;
    const int StepY = 3;
    const int DirY = 6;
    pinMode(StepX,OUTPUT);
    pinMode(DirX,OUTPUT);
    pinMode(StepY,OUTPUT);
    pinMode(DirY,OUTPUT);

    DEBUG = false;
}

void loop() {
    static String input = "";

    while (Serial.available() > 0) {
        char inChar = Serial.read();

        // Ignore carriage return
        if (inChar == '\r') continue;

        // End of line -> process input
        if (inChar == '\n') {
            input.trim();  // Remove any leading/trailing whitespace

            if (input.startsWith("G:")) {
                Coord from;
                Coord to;
                if (findIncomingCoords(input, from, to)) {
                    moveToCoord(from.x, from.y, to.x, to.y, 500);
                } else {
                    Serial.println("Invalid input. Use format: G:x1,y1|x2,y2");
                }
            } 
            else if (input.length() == 1) {
                char command = input.charAt(0);
                if (command == 'U') {
                    yForward(1, 500); currentY++;
                } else if (command == 'D') {
                    yBackward(1, 500); currentY--;
                } else if (command == 'L') {
                    xLeft(1, 500); currentX--;
                } else if (command == 'R') {
                    xRight(1, 500); currentX++;
                } else if (command == 'Q') {
                    Serial.println("Quit program");
                } else {
                    Serial.println("Unknown command");
                }
            } 
            else {
                Serial.println("Invalid input:");
                Serial.println(input);
            }

            input = "";  // Clear buffer
        } 
        else {
            input += inChar;  // Accumulate
        }
    }
}

#include <Arduino.h>
#include "motorControl/motorMove.h"

bool DEBUG;

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
    if (Serial.available()>0) {
        char incMessage = Serial.read();

        // Ignore newline and carriage return characters
        if (incMessage == '\n' || incMessage == '\r') {
            return;
        }

        if (incMessage == 'U') {   
            yForward(100, 500);
            }
        else if (incMessage == 'D') {   
            yBackward(100, 500);
            }
        else if (incMessage == 'L') {
            xLeft(100, 500);
            }
        else if (incMessage == 'R') {
            xRight(100, 500);
            }
        else if (incMessage == 'Q') {
            Serial.print("Quit program");
            }

        else {
            Serial.print("Unknown command");
        }
    }
}

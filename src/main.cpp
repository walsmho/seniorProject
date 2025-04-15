#include <Arduino.h>
#include "motorControl/motorMove.h"

void setup() {
    //Open Serial for comms
    Serial.begin(9600);

    //Set pins for CNC shield
    const int StepX = 2;
    const int DirX = 5;
    const int StepY = 3;
    const int DirY = 6;
    pinMode(StepX,OUTPUT);
    pinMode(DirX,OUTPUT);
    pinMode(StepY,OUTPUT);
    pinMode(DirY,OUTPUT);

}

void loop() {
    //LIL ROBO DANCE 
    yForward(600, 500);
    delay(1000);
    //TEST TO MOVE BACKWARD
    yBackward(600, 500);
    delay(1000);
    //TEST TO MOVE RIGHT
    xRight(600, 500);
    delay(1000);
    //TEST TO MOVE LEFT
    xLeft(1200, 500);
    delay(1000);
    xRight(600, 500);
    delay(1000);
    yBackward(700, 500);
    delay(1000);
    yForward(700, 500);

}

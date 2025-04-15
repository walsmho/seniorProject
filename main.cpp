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
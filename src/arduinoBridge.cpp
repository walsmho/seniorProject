#include <Arduino.h>

int light = LED_BUILTIN;
String incomingMessage;
bool debug = true;

void setup() {
    Serial.begin(9600);
    pinMode(light, OUTPUT);
}

void loop() {
    // If receiving data from Serial via python:
    if (Serial.available()>0) {
        incomingMessage = Serial.readStringUntil('\n');
        if (debug == true) {
            Serial.print("r: "); Serial.print(incomingMessage); Serial.print("\n");
            // Forgot that low level language like C++ means bytes matter. R=received
        }

        if (incomingMessage == "T") {
            // Invert value of LED if movement detected
            digitalWrite(light, !digitalRead(light));
            }
        }
    }

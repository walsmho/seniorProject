// PLEASE READ: This file has been used for tests only. Eventually it will be redesigned only for
// helper functions to communicate with OpenCV's vision system and get commands.

//#include <Arduino.h>

// int light = LED_BUILTIN;
// String incomingMessage;
// bool debug = true;

// void setup() {
//     Serial.begin(9600);
//     pinMode(light, OUTPUT);
// }

// void loop() {
//     // If receiving data from Serial via python:
//     if (Serial.available()>0) {
//         char incomingMessage = Serial.read();
//         if (debug == true) {
//             Serial.print("r: "); Serial.print(incomingMessage); Serial.print("\n");
//             // Forgot that low level language like C++ means bytes matter. R=received
//         }

//         if (incomingMessage == 'T') {   
//             // Invert value of LED if movement detected
//             digitalWrite(light, !digitalRead(light));
//             }
//         }
//     }

#include <Arduino.h>

// // put function declarations here:
// int myFunction(int, int);
String incomingBytes;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available()>0) {
    incomingBytes = (Serial.readStringUntil('\n')); // Read until py endstring format
    if (incomingBytes == "ON") {
      digitalWrite(LED_BUILTIN, HIGH);
      Serial.write("Arduino Comm: Builtin LED is ON");
    }
    if (incomingBytes == "OFF") {
      digitalWrite(LED_BUILTIN, LOW);
      Serial.write("Arduino Comm: Builtin LED is OFF");
    }

    else  {
      Serial.write("Arduino Comm: Sorry, invalid input...");
    }
  }
}

// // put function definitions here:
// int myFunction(int x, int y) {
//   return x + y;
// }
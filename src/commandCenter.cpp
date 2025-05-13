#include <Arduino.h>
#include "motorControl/motorMove.h"

bool DEBUG = true;
int homeSpeed = 1000; //switch back to 1000 after testing

void setup() {
  Serial.begin(115200);  // Use a consistent and fast baud rate

  pinMode(2, OUTPUT); // STEP_PIN_A
  pinMode(5, OUTPUT); // DIR_PIN_A
  pinMode(3, OUTPUT); // STEP_PIN_B
  pinMode(6, OUTPUT); // DIR_PIN_B
}

void loop() {
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');
    
    if (input.startsWith("GOTO")) {
      parseAndMove(input);
      Serial.print(input);
    }

    else if (input.length() == 1) {
      char command = input.charAt(0);

      if (command == 'U') {
        yForward(1, homeSpeed);
      } else if (command == 'D') {
        yBackward(1, homeSpeed);
      } else if (command == 'L') {
        xLeft(1, homeSpeed);
      } else if (command == 'R') {
        xRight(1, homeSpeed);
      } else if (command == 'Q') {
        Serial.println("Quit program");
      } else {
        Serial.println("Unknown command");
      }
    } 
  Serial.flush();
  }

  else {
      Serial.println("Invalid input:");
  }
}

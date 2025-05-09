#include <Arduino.h>
#include "motorControl/motorMove.h"
#include <motorControl/hBot.h>

bool DEBUG = true;
long currentX;
long currentY;

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
    input.trim();

    if (input.startsWith("GOTO")) {
      parseAndMove(input);
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
  }
  Serial.flush();
}

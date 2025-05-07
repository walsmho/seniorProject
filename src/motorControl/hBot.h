// #include <Arduino.h>

// #ifndef MOTION_HELPERS_H
// #define MOTION_HELPERS_H

// #define STEP_PIN_A 2
// #define DIR_PIN_A  5
// #define STEP_PIN_B 3
// #define DIR_PIN_B  6

// int feedrate = 500;  // delay in µs between steps

// void bresenhamMove(long stepsA, long stepsB) {
//   long dx = stepsA;
//   long dy = stepsB;

//   long absA = abs(dx);
//   long absB = abs(dy);

//   long err = absA - absB;
//   absA *= 2;
//   absB *= 2;

//   while (absA > 0 || absB > 0) {
//     if (absA > 0) {
//       digitalWrite(STEP_PIN_A, HIGH);
//       delayMicroseconds(500);
//       digitalWrite(STEP_PIN_A, LOW);
//     }

//     if (absB > 0) {
//       digitalWrite(STEP_PIN_B, HIGH);
//       delayMicroseconds(500);
//       digitalWrite(STEP_PIN_B, LOW);
//     }

//     long e2 = err;
//     if (e2 > -absB && absA > 0) {
//       err -= absB;
//       absA--;
//     }
//     if (e2 < absA && absB > 0) {
//       err += absA;
//       absB--;
//     }

//     delayMicroseconds(feedrate);
//   }
// }

// void parseAndMove(String command) {
//   command.trim();
//   if (!command.startsWith("GOTO")) return;

//   int indexA = command.indexOf('A');
//   int indexB = command.indexOf('B');
//   int indexF = command.indexOf('F');

//   // Basic error check: ensure all parts exist and are in correct order
//   if (indexA == -1 || indexB == -1 || indexF == -1 ||
//       indexA >= indexB || indexB >= indexF) {
//     return; // malformed command
//   }

//   long moveA = command.substring(indexA + 1, indexB).toInt();
//   long moveB = command.substring(indexB + 1, indexF).toInt();
//   int fr = command.substring(indexF + 1).toInt();

//   feedrate = (fr > 0) ? fr : feedrate;

//   // Set motor directions
//   digitalWrite(DIR_PIN_A, (moveA >= 0) ? HIGH : LOW);
//   digitalWrite(DIR_PIN_B, (moveB >= 0) ? HIGH : LOW);

//   bresenhamMove(abs(moveA), abs(moveB));
// }

// #endif

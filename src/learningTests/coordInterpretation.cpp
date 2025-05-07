/*

Purpose of file: I hate c++ and need to figure out how to:
 1) Interpret sent coordinates from python
 2) Determine dx and dy
 3) Bresenham crap
 4) Step motors accordingly

*/

#include "learningTests/coordInterpretation.h"
#include "motorControl/motorMove.h"

bool parseCoordinates(const String &data, Coordinates &coords) {
  int index1 = data.indexOf(',');
  int index2 = data.indexOf(',', index1 + 1);
  int index3 = data.indexOf(',', index2 + 1);

  if (index1 > 0 && index2 > index1 && index3 > index2) {
    coords.oldX = data.substring(0, index1).toInt();
    coords.oldY = data.substring(index1 + 1, index2).toInt();
    coords.newX = data.substring(index2 + 1, index3).toInt();
    coords.newY = data.substring(index3 + 1).toInt();
    return true;
  }

  return false;
}

Delta calculateDelta(const Coordinates &coords) {
  Delta delta;
  delta.deltaX = coords.newX - coords.oldX;
  delta.deltaY = coords.newY - coords.oldY;
  return delta;
}

bool readSerialLine(String &result) {
  static String inputBuffer = "";
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    if (inChar == '\n') {
      result = inputBuffer;
      inputBuffer = "";
      return true;
    } else {
      inputBuffer += inChar;
    }
  }
  return false;
}

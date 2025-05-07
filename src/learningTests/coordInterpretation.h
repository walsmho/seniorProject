#ifndef COORDINATE_HELPER_H
#define COORDINATE_HELPER_H

#include <Arduino.h>

// Structure to store coordinates
struct Coordinates {
  int oldX;
  int oldY;
  int newX;
  int newY;
};

// Structure to store delta values
struct Delta {
  int deltaX;
  int deltaY;
};

// Parses a string like "10,20,15,25" and fills a Coordinates struct
bool parseCoordinates(const String &data, Coordinates &coords);

// Calculates delta from a Coordinates struct
Delta calculateDelta(const Coordinates &coords);

// Reads serial input until newline is encountered
bool readSerialLine(String &result);

#endif

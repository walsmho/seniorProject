# seniorProject
Welcome to G.H.O.S.T - a Gantry Hockey Opponent System Table

This project uses an algorithm and overhead vision system to control a gantry that can play air hockey with a live opponent. One player air hockey - so you no longer need to make friends to play this game!

This code uses Python and OpenCV for all computer vision and computation. It then defers the appropriate commands through the Serial monitor to an Arduino leonardo, which then relays these commands to a CNC shield controlling two stepper motors for a gantry. This project is based off of an old instructables project by JJrobots, which is a business now nonexistent. This code and its implementation is unique.

## Table of Contents 
- [Hardware]
- [Installation]
- [Usage]
- [Links]

## Hardware

The following components are uitilized in this project:
- Arduino Lenoardo
- CNC Shield for Arduino
- 2x NEMA 17 Stepper Motors
- 12V 4a Power Supply
- Logitech 1080p webcam

## Installation

This program uses Python 3.13 and C++ through the PlatformIO extension in VSCode. 

## Usage

Open the config.py file and ensure that WEBCAM is set correctly. If you are using a computer with a built-in webcam, it will need to be switched to 1.

## Links

- Instructables project with 3D printed parts: https://www.instructables.com/Air-Hockey-Robot-EVO/
- JJRobots github: https://github.com/jjrobots/Air_Hockey_Robot_EVO/blob/master/Arduino/AHRobot_EVO/Robot.ino
- CNC Shield: https://www.amazon.com/Shield-Expansion-Stepper-Engraver-Printer/dp/B07DXNZ9PS/ref=asc_df_B07DXNZ9PS?mcid=57d1184c4d1b3bfa8894c7ec1b457f00&tag=hyprod-20&linkCode=df0&hvadid=693270340452&hvpos=&hvnetw=g&hvrand=16431001300624411400&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9194781&hvtargid=pla-524786093705&psc=1

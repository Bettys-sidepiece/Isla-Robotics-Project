# Project-Isla
Source files for the Software and Hardware (PCB) designs of the ISLA Project. All these files are free to use and modify:).

The ISLA Project is a DIY friendly autonomous robot using only mostly through hole components making this design very easy to implement for anyone with some money, a Raspberry Pi Pico and a soldering iron. I decided to make this because I wanted to create something that would be easy to make even for people who do not have access to specific equipment such as a reflow oven or a scope. The Design is powered by 4 AAA batteries, which are used to power the various sensors and the microcontroller. The microcontroller control the battery sensor, motors, proximity sensor and line sensor on the device.

Indicators
----------

- Power LED
- Sensor LED
- Buzzer
- OLED Display

Sensors
--------

- 4x Infrared Proximity sensors
- 4x Infrared Line Sensors
- Battery Sensor
- 2x Motor Encoders

Power Management 
-----------------

The ISLA robot uses a simple latching circuit to power off and on by the press of a button. The circuit has the following features

- Quick startup
- 3 second power off delay
- 1 second hard reset


In order to reduce the power draw by the sensors while Idle the the sensors are powered on and off using BJT load switches embedded on the board.


Making the most of the Raspberry Pi Pico
------------------------------------------

To fully utilize all the pins off the Pico the load switches and buzzer are controlled using the MCP23008 GPIO Extender which provides 8 GPIO pins to use for low priority operations such as button input. This frees up the pico to be used for SPI,I2C or PWM as ALL but 1 of its GPIO pins can be used for high priority functions

Programming
------------

- MicroPython
-Thonny IDE

The firmware of this robot is fairly easy to follow and reverse engineer, feel from to view it in the repository : https://github.com/Bettys-sidepiece/Project-Isla

The device firmware is still under development therefore there are several features that are not enabled such as,

Line Tracking
Maze Solving (Line)
Maze Solving (Proximity)
Path Retracing
Maze Solving (Reverse)


Shortcomings
-------------

Most the shortcomings of this project are in the PCB design, these have been corrected for in the two PCB schematics using notes please. However, This project can be done in various ways many of which are better and more efficient, I chose to do it this way to maximise the space being used.

#!/usr/bin/env python
# ----------------------------------------------------------------------------
# MIT License
# moves the roomba through a simple sequence

from __future__ import print_function
import pycreate2
import time

port = 10
# port = '/dev/ttyUSB0'  # this is the serial port on my raspberry pi
baud = {
    'default': 115200,
    'alt': 19200  # shouldn't need this unless you accidentally set it to this
}

bot = pycreate2.Create2(port=port, baud=baud['default'])

#base velocity
vel = 200

#base rotation
rot = 2

#range of acceptable z pos
zRange = [2, 3]

#range of acceptable x pos from center
xRange = 1

#defines center
center = 0

#takes in xpos (distance to the object) and zpos (distance from the center of the screen)
def alterTraject(xpos, zpos):
    while(abs(xpos - xrange) < xRange):
        if(zpos > zRange[1]):
            vel = 500
        else if(zpos < zrange[0]):
            vel = 0
        else:
            vel = 200
        bot.drive_straight(vel)
    if(xpos < center):
        bot.drive_turn(vel, -1)
    else:
        bot.drive_turn(vel, 1)

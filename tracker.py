#!/usr/bin/env python
# ----------------------------------------------------------------------------
# MIT License
# moves the roomba through a simple sequence

from __future__ import print_function
import pycreate2
import time

if __name__ == "__main__":
    print("hello")
    port = 'COM10'
    print('hekkjwf')

    # port = '/dev/ttyUSB0'  # this is the serial port on my raspberry pi
    baud = {
        'default': 115200,
        'alt': 19200  # shouldn't need this unless you accidentally set it to this
        }

    bot = pycreate2.Create2(port, baud['default'])
    width = 640
    height = 480
    print('hrljkvh')

    #base velocity
    vel = 200
    #base rotation

    #range of acceptable x pos from center
    zRangemax = 56

    #defines center
    zRangemin = 44

    #takes in leftCorner and right corner (distance from left of image to left and right corner)
    #returns distance from the center of the image


    #takes in zSize (pixel size of the right edge of the box)
    #takes in xPos (distance from the center of the image) (x pos = getxPos)
    def getxPos():
        return 300
    def getzPos():
        return 50
    def getAccuracy():
        return True

    def alterTraject():
        accurate = getAccuracy()
        zSize = getzPos()
        xPos = getxPos()
        while(True):
            while(accurate):
                while(abs(xPos) < 200):
                    if(zSize > zRangemax):
                        vel = 0
                    elif(zSize < zRangemin):
                        vel = 500
                    else:
                        vel = 200
                    bot.drive_straight(vel)
                    print(vel)
                    xPos = getxPos()
                    zSize = getzPos()
                    accurate = getAccuracy()
                    if(not accurate):
                        break
                if(abs(xPos) > 200):
                    vel = 200
                    if(xPos < 0):
                        bot.drive_turn(vel, -1)
                    else:
                        bot.drive_turn(vel, 1)
                    accurate = getAccuracy()
    bot.start()
    bot.safe()
    zSize = 100
    alterTraject()

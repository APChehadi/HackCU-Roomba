#!/usr/bin/env python
# ----------------------------------------------------------------------------
# MIT License
# moves the roomba through a simple sequence

from __future__ import print_function
import pycreate2
from roombacv import RoombaCV
import time
import os

if __name__ == "__main__":
    if(os.name == 'nt'):
        port = 'COM10'
    else:
        port = '/dev/ttyUSB0'
    # port = '/dev/ttyUSB0'  # this is the serial port on my raspberry pi
    baud = {
        'default': 115200,
        'alt': 19200  # shouldn't need this unless you accidentally set it to this
        }

    bot = pycreate2.Create2(port, baud['default'])
    width = 640
    height = 480

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
    rv = RoombaCV()

    def alterTraject():
        while (True):
            ret = rv.readFrame()
            if (ret[0]):
                zSize = ret[2]
                xPos = ret[1][0]
                print("zSize: " + str(ret[2]))
                print("xPos: " + str(ret[1][0]))
                if (abs(xPos - 320) < 200):
                    if(zSize > zRangemax):
                        vel = 0
                        if (zSize - 20) > zRangemax:
                            vel = -200
                    elif(zSize < zRangemin):
                        vel = 500
                    else:
                        vel = 200
                    bot.drive_straight(vel)
                    print(vel)
                elif(abs(xPos - 320) > 200):
                    vel = 200
                    if(xPos - 320 < 0):
                        print("left turn")
                        bot.drive_turn(vel / 1.5, 1)
                    else:
                        bot.drive_turn(vel / 1.5, -1)

        '''
        ret = rv.readFrame()

        accurate = ret[0]
        zSize = ret[2]
        xPos = ret[1][0]
        while(True):
            print("hello")
            ret = rv.readFrame()
            accurate = ret[0]
            xPos = ret[1][0]
            zSize = ret[2]
            print(xPos)
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
                    ret = rv.readFrame()
                    xPos = ret[1][0]
                    print(xPos)
                    zSize = ret[2]
                    accurate = ret[0]
                    if(not accurate):
                        break
                if(abs(xPos) > 200):
                    vel = 200
                    if(xPos < 0):
                        bot.drive_turn(vel, -1)
                    else:
                        bot.drive_turn(vel, 1)
                    ret = rv.readFrame()
                    accurate = ret[0]
         '''
    

    bot.start()
    bot.safe()
    zSize = 100
    alterTraject()

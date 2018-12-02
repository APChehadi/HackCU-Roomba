#!/usr/bin/env python
# ----------------------------------------------------------------------------
# MIT License

from __future__ import print_function
import pycreate2
from app.roombacv import RoombaCV
#from app.routes import getWebTrue
import time
import os

width = 640
height = 480

#base velocity
vel = 200
#base rotation

#range of acceptable x pos from center
zRangemax = 56

#defines center
zRangemin = 44

def alterTraject(rv):
    webTrue = getWebTrue()
    while (True and webTrue):
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
        webTrue = getWebTrue()
from app import app
import pycreate2
from flask import render_template
import os
import cv2
from app.roombacv import RoombaCV
import time
from app.active import alterTraject


webTrue = False

def getWebTrue():
    return webTrue
port = '/dev/ttyUSB0'

if(os.name == 'nt'):
    port = 'COM10'
else:
    port = '/dev/tty0'
baud = {
    'default': 115200,
    'alt': 19200  # shouldn't need this unless you accidentally set it to this
    }

bot = pycreate2.Create2(port=port, baud=baud['default'])


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")




@app.route("/setup/", methods=['POST'])
def setup():
    bot.start()
    bot.safe()
    forward_message = "set up"
    return render_template('index.html',scrollToAnchor='controls', message=forward_message)

@app.route("/turnRight/", methods=['POST'])
def turn_right():
    bot.drive_turn(-100, 1)
    forward_message = "turning right"
    return render_template('index.html',scrollToAnchor='controls', message=forward_message)

@app.route("/turnLeft/", methods=['POST'])
def turn_left():
    bot.drive_turn(100, 1)
    forward_message = "turning left"
    return render_template('index.html',scrollToAnchor='controls', message=forward_message)

@app.route("/MoveForward/", methods=['POST'])
def move_forward():
    bot.drive_straight(100)
    forward_message = "moving forward"
    return render_template('index.html',scrollToAnchor='controls', message=forward_message)

@app.route("/MoveBackward/", methods=['POST'])
def move_backward():
    bot.drive_straight(-100)
    forward_message = "moving backward"
    return render_template('index.html',scrollToAnchor='controls', message=forward_message)

@app.route("/stop/", methods=['POST'])
def stop_moving():
    bot.drive_stop()
    forward_message = "stopped"
    return render_template('index.html',scrollToAnchor='controls', message=forward_message)


@app.route("/executeimagetrack/", methods=['POST'])
def execute_image_track():
    global webTrue
    webTrue = True
    alterTraject(bot)
    forward_message = "altering sequence"
    return render_template('index.html',scrollToAnchor='controls', message=forward_message)

@app.route("/stopimagetrack/", methods=['POST'])
def stop_moving():
    global webTrue
    webTrue = False
    forward_message = "stopping sequence"
    return render_template('index.html',scrollToAnchor='controls', message=forward_message)

from app import app
import pycreate2
from flask import render_template
port = "COM10"
baud = 115200
bot = pycreate2.Create2(port=port, baud=baud)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route("/setup/", methods=['POST'])
def setup():
    bot.start()
    bot.safe()
    forward_message = "setingup..."
    return render_template('index.html', message=forward_message)

@app.route("/turn/", methods=['POST'])
def move_forward():
    bot.drive_turn(100, 1)
    forward_message = "turning"
    return render_template('index.html', message=forward_message)
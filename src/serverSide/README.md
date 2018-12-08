# create virtual environment
    $python -m venv venv
    $source venv/bin/activate
  
# install packages

flask
pycreate2
opencv (not for virtual, but once code a directory above is in this one, we will need this)


main code is on routes.py

to run

    $flask run (in virtual env)

# ngrok

    $ngrok http 5000 (or whatever port it is running on)

url is the https on ngrok

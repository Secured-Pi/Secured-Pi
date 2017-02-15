# Secured-Pi
Code 401 (Python) - final project

## Description
Python web application for a smart lock powered by Raspberry Pi; features facial recognition for
security.  This code is for the main Django server.

The project consists of three components:  the raspberry pi, the django server, and the flask server.
The Django server is where a user can register an account along with their raspberry pi controlled
lock.

- From the Django site, they can control the lock with the press of a button, take pictures and train
the facial recognition software, and monitor who has attempted to enter.

- The flask server is responsible for two-way communication with the raspberry pi using a socketio
connection (which is essentially a connection that stays alive).  Most raspberry pi's will be
behind a firewall on a local network, and the flask server allows commands to be sent from the
Django server to the raspberry pi.

- The raspberry pi is connected to a motor (attached to a lock), a webcam, and an RFID scanner.

Once everything is set up, a user can open a lock by first scanning their RFID card, and then having
a picture of their face taken, which gets sent together to the Django server for authentication.
The raspberry pi uses facial detection to identify a human face, and the Django server is
responsible for actually recognizing the face and issuing commands to unlock the lock.

## Setup instructions:
After cloning this repo and cd into the project directory:

- Create a postgres database named 'securedpi'

Then:
```
python3 -m venv ENV
source ENV/bin/activate
pip install -r requirements.txt
```

Then, you need to install OpenCV3 with the additional facial recognition module.  There
re several ways of doing this, and I recommend researching it if you have not
done this before.

Then,
```
export DEBUG=True
./manage.py migrate
./manage.py runserver
```


## Contributors:
* Steven Than
* David Smith
* Tatiana Weaver
* Crystal Lessor

Demonstration (sorry, no sound):
https://www.youtube.com/watch?v=3Lnaw9H-Upg

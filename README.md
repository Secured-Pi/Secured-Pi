# Secured-Pi

This was a final project (week-long) for the Code Fellows Python 401 Advanced Software Development
course taught by Cris Ewing.  There are still many un-implemented features which may continue
to be worked on in the future, as this project is still in the somewhat 'early' stages.

## Description
Python web application for a smart lock powered by Raspberry Pi.  It features facial recognition for
security.  This code is for the main Django server.

The project consists of three components:  the Raspberry Pi, the django server, and the flask server.
The Django server is where a user can register an account along with their Raspberry Pi controlled
lock.

Here is a link to the porject on hackster.io:  https://www.hackster.io/secured-pi/facial-recognition-rfid-lock-with-raspberry-pi-e81f98

- From the Django site, a user can control the lock with the press of a button, take pictures, train
the facial recognition software, and monitor who has attempted to enter.

- The Flask server is responsible for two-way communication with the Raspberry Pi using a socketio
connection (which is essentially a connection that stays alive).  Most Raspberry Pi's will be
behind a firewall on a local network, and the flask server allows commands to be sent from the
Django server to the Raspberry Pi.

- The Raspberry Pi is connected to a motor (attached to a lock), a webcam, and an RFID scanner.

Once everything is set up, a user can open a lock by first scanning their RFID card, and then having
a picture of their face taken, which gets sent together to the Django server for authentication.
The Raspberry Pi uses facial detection to identify a human face, and the Django server is
responsible for actually recognizing the face and issuing commands to unlock the lock.

## Setup instructions:
After cloning this repo and cd into the project directory:

- Install postgres (if needed) and create a database named 'securedpi'

Then, create a virtual environment and install requirements:
```
python3 -m venv ENV
source ENV/bin/activate
pip install -U pip setuptools
pip install -r requirements.txt
```

Then, you need to install OpenCV3 with the additional facial recognition module.  There
are several ways of doing this, and I recommend researching it if you have not
done this before.  You can either install it in this virtual environment, or you can install it
globally and copy lib files into the virtual environment.

Then, create a superuser:
```
./manage.py createsuperuser
```

Then, set a DEBUG environment variable to False, and then migrate and runserver.
```
export DEBUG=True
./manage.py migrate
./manage.py runserver
```

Then, go ahead and create a user account for yourself on the site.  More instructions to come:

(Just a high level overview is here for now)

1) Setting up the Flask server
- Clone the flask-socketio-server repository
- Create a virtual environment, install by: pip install -r requirements.txt
- Run the server with ./src/server.py

2) Setting up Raspberry Pi
- Setup Raspberry Pi by connecting RFID, webcam, and updating the software.  Consider a breadboard.
- Clone the raspberry-pi-client repository on to the device.
- Create a virtual environment, activate it, install requirements.txt, and OpenCV.  OpenCV2 is
sufficient, since we only need it to take pictures of a face.
- Configure Django server location in the main.py code (more to come).
- Run ./main.py and use your Django server user credentials to register your lock and begin
listening to the Flask server.
- After this, if all went well, you should be able to control the lock manually from the website by
hitting the unlock button.

3) Training facial recognition
- Instructions to come...


## Contributors:
* Steven Than
* David Smith
* Tatiana Weaver
* Crystal Lessor

Demonstration (sorry, no sound):
https://www.youtube.com/watch?v=3Lnaw9H-Upg

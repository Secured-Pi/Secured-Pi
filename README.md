# Secured-Pi
Code 401 (Python) - final project

## Description
Python web application for a smart lock powered by Raspberry Pi; features facial recognition for security.
This code is for the main Django server.

## Setup instructions:
First, you need to install OpenCV3 with facial recognition packages.  There
re several ways of doing this, and I recommend researching it if you have not
done this before.
Then, after cloning this repo and cd into teh project directory:
```
python3 -m venv ENV
source ENV/bin/activate
pip install -r requirements.txt
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

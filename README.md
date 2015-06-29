# LUMA
LED User Manipulated Apparatus
------------------------------
LUMA at its core is a fancy area lighting system, with some LEDs at one end and a web interface at the other, and
a robust lighting protocol in the middle.

Features
--------
* **Simple extensability:** Want another completely independent light fixture? Just add a new strip to an existing 
LUMA client (Up to 5 fixtures per client), or an entirely new client.
* **Robust lighting definition:** Describe lighting color patterns as waveforms of brightness over time.
* **Easy-to-use interface:** Search for a light, and draw some waves.
* **For public and private use:** Permission to view/edit lights is whitelisted. If you want to have a client
for your room while your favorite dorm organization wants to string up some lights in the hall, you can
rest easy knowing that permission to control your room is not related to that of the hall.
* **RESTful API:** Interactions with the server are done with via a simple RESTful API. Write an app and control
your lights from a toilet or committee meeting. Or get creative!

Structure
---------
LUMA consists of three easily configured main components:
* Client
* Server
* Interface

Let's start with the client. Each client is a Raspberry Pi (The client code can be easily ported to your tiny 
computer of choice) with an attached PWM module. The PWM modules have 16 pins, and with one pin per color channel
and three channels per light, we can attach up to five lighting fixtures per client.

The server is a simple Flask machine that listens to requests and updates with a RESTful API. It also serves the
web interface as a matter of convienience.

The web interface is a Angular.JS application. It uses canvases to allow users to draw brightness waveforms.
Not much more to be said.

Hardware
--------
The client was written for a Raspberry Pi with an attached Adafruit PCA9685 PWM controller. (Support for the 
superior TLC5947 is coming). The codebase sans Adafruit PWM library is 100% Python, so porting it to another
platform should be relatively straightforward. I leave it to you to supply LEDs and power to those LEDs.
Don't let me down!

The server code can run anywhere that can serve up a webpage and juggle a bunch of TCP sockets on port 8641.
(Or whatever port, as long as you update the relevant constants accordingly.)

The web interface is a web interface. If you have an HTML5 browser it should be just dandy. HTML4 will tick it off.

Dependencies
------------
* **Client:** The client requires the Adafruit PWM library, and also that i2c be enabled. This is a bit of a chore,
and I'm trying to make it easier for you guys using LUMA. The client needs Python 2.7, and I'm using 2.7.10 since
it comes with pip.
* **Server:** The server uses Python 2.7 like the client. It also needs Flask. (0.10.1 should work.) Because of this
I recommend using Python 2.7.8 or later since it comes with pip and takes Flask installation from arduous and convoluted
to straightforward. (I'm using 2.7.10)
* **Web Interface:** The web interface uses Angular.JS (Truth be told the entire point of this project for me 
was to dirty my hands with Angular and Flask) being pulled down over AJAX from Google APIs. Should you want to 
serve Angular for the interface on your own watch, it will probably be best to stick with version 1.3.15. 

Configuration
-------------
I'll get back to you on this when LUMA is at a state to be used and I have a process documented for you.
